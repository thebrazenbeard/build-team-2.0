from __future__ import annotations

import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, normalize_relative_posix_path, sha256_hex
from .contracts import RecordEnvelope, parse_record
from ._store_helpers import _counts, _dependency_closure, _topological_records
from ._store_types import ConflictError, ValidationError


class PortabilityMixin:
    def export_bundle(self, destination: str | Path) -> dict[str, Any]:
        target = Path(destination)
        if target.exists() and any(target.iterdir()):
            raise ConflictError("Export destination must be absent or empty")
        target.mkdir(parents=True, exist_ok=True)
        rows = self._connection.execute("select canonical_json from records order by record_id").fetchall()
        records_path = target / "records.ndjson"
        records_bytes = b"".join(row["canonical_json"].encode("utf-8") + b"\n" for row in rows)
        records_path.write_bytes(records_bytes)
        exported_sources: list[dict[str, Any]] = []
        source_target = target / "sources"
        source_target.mkdir(exist_ok=True)
        for source in sorted(self.sources_path.glob("*")) if self.sources_path.exists() else []:
            if not source.is_file():
                continue
            digest = sha256_hex(source.read_bytes())
            if digest != source.name:
                raise ValidationError(f"Source blob path does not match digest: {source}")
            shutil.copy2(source, source_target / source.name)
            exported_sources.append({"sha256": digest, "size": source.stat().st_size})
        manifest = {
            "schema": "LANTERN_EXPORT_MANIFEST_V1",
            "project_manifest": self.manifest(),
            "record_count": len(rows),
            "records_path": normalize_relative_posix_path("records.ndjson"),
            "records_sha256": sha256_hex(records_bytes),
            "sources": exported_sources,
        }
        manifest_bytes = canonical_json_bytes(manifest) + b"\n"
        (target / "manifest.json").write_bytes(manifest_bytes)
        return {**manifest, "manifest_sha256": sha256_hex(manifest_bytes)}

    def import_bundle(self, source: str | Path) -> dict[str, Any]:
        bundle = Path(source)
        manifest_path = bundle / "manifest.json"
        records_path = bundle / "records.ndjson"
        if not manifest_path.exists() or not records_path.exists():
            raise ValidationError("Import bundle requires manifest.json and records.ndjson")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema") != "LANTERN_EXPORT_MANIFEST_V1":
            raise ValidationError("Unsupported export manifest")
        records_bytes = records_path.read_bytes()
        if sha256_hex(records_bytes) != manifest.get("records_sha256"):
            raise ValidationError("records.ndjson digest mismatch")
        parsed = [parse_record(line) for line in records_bytes.decode("utf-8").splitlines() if line]
        if any(record.project_id != self.project_id for record in parsed):
            raise ValidationError("Import project_id does not match target store")
        duplicate_ids = [record_id for record_id, count in _counts(r.record_id for r in parsed).items() if count > 1]
        if duplicate_ids:
            raise ValidationError(f"Duplicate record IDs in import bundle: {duplicate_ids}")
        by_id = {record.record_id: record for record in parsed}
        outcomes: dict[str, str] = {}
        conflict_ids: set[str] = set()
        for record in parsed:
            existing = self._connection.execute(
                "select canonical_json from records where record_id=?", (record.record_id,)
            ).fetchone()
            if existing is None:
                continue
            if existing["canonical_json"] == record.canonical_json:
                outcomes[record.record_id] = "VERIFIED"
            else:
                outcomes[record.record_id] = "CONFLICT"
                conflict_ids.add(record.record_id)
        skipped_ids = _dependency_closure(by_id, conflict_ids)
        for record_id in skipped_ids:
            if record_id not in outcomes:
                outcomes[record_id] = "SKIPPED"
        to_create = [
            record
            for record in _topological_records(parsed)
            if record.record_id not in outcomes
        ]
        with self.transaction():
            for record in to_create:
                self._insert_record_row(record)
                outcomes[record.record_id] = "CREATED"
            self._rebuild_projections()
        source_dir = bundle / "sources"
        for item in manifest.get("sources", []):
            digest = item.get("sha256")
            if not isinstance(digest, str):
                raise ValidationError("Invalid source manifest entry")
            source_path = source_dir / digest
            if not source_path.exists() or sha256_hex(source_path.read_bytes()) != digest:
                raise ValidationError(f"Missing or divergent source blob: {digest}")
            self.sources_path.mkdir(exist_ok=True)
            target = self.sources_path / digest
            if target.exists() and target.read_bytes() != source_path.read_bytes():
                raise ConflictError(f"Divergent source bytes for digest {digest}")
            if not target.exists():
                shutil.copy2(source_path, target)
        ordered_results = [
            {"record_id": record.record_id, "outcome": outcomes[record.record_id]}
            for record in parsed
        ]
        summary = defaultdict(int)
        for result in ordered_results:
            summary[result["outcome"]] += 1
        return {
            "schema": "LANTERN_IMPORT_RECEIPT_V1",
            "project_id": self.project_id,
            "results": ordered_results,
            "summary": dict(sorted(summary.items())),
        }

    def _rebuild_projections(self) -> None:
        self._connection.execute("delete from lineage_heads")
        self._connection.execute("delete from links")
        self._connection.execute("delete from state_heads")
        self._connection.execute("delete from state_events")
        rows = self._connection.execute("select * from records order by created_at, record_id").fetchall()
        records = [self._row_to_record(row) for row in rows]
        by_id = {record.record_id: record for record in records}
        lineage_groups: dict[tuple[str, str, str], list[RecordEnvelope]] = defaultdict(list)
        for record in records:
            if record.record_type != "StateEvent" and record.lineage_key is not None:
                lineage_groups[(record.project_id, record.record_type, record.lineage_key)].append(record)
        for key, group in lineage_groups.items():
            roots = [record for record in group if record.predecessor_record_id is None]
            if len(roots) != 1:
                raise ValidationError(f"Lineage {key} must have exactly one root")
            children: dict[str, list[RecordEnvelope]] = defaultdict(list)
            for record in group:
                if record.predecessor_record_id is not None:
                    predecessor = by_id.get(record.predecessor_record_id)
                    if predecessor is None:
                        raise ValidationError("Missing predecessor during projection rebuild")
                    if predecessor.record_type != record.record_type or predecessor.lineage_key != record.lineage_key:
                        raise ValidationError("Cross-lineage predecessor during projection rebuild")
                    children[record.predecessor_record_id].append(record)
            if any(len(values) > 1 for values in children.values()):
                raise ValidationError(f"Competing successors in lineage {key}")
            current = roots[0]
            visited = {current.record_id}
            while children.get(current.record_id):
                current = children[current.record_id][0]
                if current.record_id in visited:
                    raise ValidationError(f"Cycle in lineage {key}")
                visited.add(current.record_id)
            if len(visited) != len(group):
                raise ValidationError(f"Disconnected lineage {key}")
            self._connection.execute(
                "insert into lineage_heads(project_id, record_type, lineage_key, record_id) values (?, ?, ?, ?)",
                (*key, current.record_id),
            )
        for record in records:
            if record.record_type == "Link":
                self._project_link(record)
        state_records = [record for record in records if record.record_type == "StateEvent"]
        pending = {record.record_id: record for record in state_records}
        while pending:
            progressed = False
            for record_id, record in list(pending.items()):
                if record.predecessor_record_id is None or record.predecessor_record_id not in pending:
                    self._project_state_event(record)
                    del pending[record_id]
                    progressed = True
            if not progressed:
                raise ValidationError("StateEvent stream contains a cycle or missing predecessor")

