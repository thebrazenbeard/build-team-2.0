from __future__ import annotations

import json
import os
import shutil
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, normalize_relative_posix_path, sha256_hex, strict_json_loads
from .contracts import RecordEnvelope, parse_record
from .validation import manifest_bytes, validate_project_manifest, validate_record_semantics
from ._store_files import stage_source_blobs
from ._store_helpers import _counts, _dependency_closure, _topological_records
from ._store_types import ConflictError, ValidationError

_EXPORT_KEYS = {"schema", "project_manifest", "record_count", "records_path", "records_sha256", "sources"}
_SOURCE_ENTRY_KEYS = {"sha256", "size"}


class PortabilityMixin:
    def export_bundle(self, destination: str | Path) -> dict[str, Any]:
        self.verify_manifest_consistency()
        target = Path(destination)
        if target.exists() and any(target.iterdir()):
            raise ConflictError("Export destination must be absent or empty")
        target.mkdir(parents=True, exist_ok=True)
        rows = self._connection.execute("select canonical_json from records order by record_id").fetchall()
        records_bytes = b"".join(row["canonical_json"].encode("utf-8") + b"\n" for row in rows)
        (target / "records.ndjson").write_bytes(records_bytes)

        referenced: set[str] = set()
        source_rows = self._connection.execute(
            "select payload_json from records where record_type='SourceSnapshot' order by record_id"
        ).fetchall()
        for row in source_rows:
            payload = json.loads(row["payload_json"])
            if payload.get("custody_mode") in {"CAPTURED", "EMBEDDED"}:
                digest = payload.get("content_sha256")
                if isinstance(digest, str):
                    referenced.add(digest)
        source_target = target / "sources"
        source_target.mkdir(exist_ok=True)
        exported_sources: list[dict[str, Any]] = []
        for digest in sorted(referenced):
            source = self.sources_path / digest
            if not source.exists():
                raise ValidationError(f"Referenced source blob is missing: {digest}")
            content = source.read_bytes()
            if sha256_hex(content) != digest:
                raise ValidationError(f"Source blob path does not match digest: {source}")
            (source_target / digest).write_bytes(content)
            exported_sources.append({"sha256": digest, "size": len(content)})
        manifest = {
            "schema": "LANTERN_EXPORT_MANIFEST_V1",
            "project_manifest": self.manifest(),
            "record_count": len(rows),
            "records_path": normalize_relative_posix_path("records.ndjson"),
            "records_sha256": sha256_hex(records_bytes),
            "sources": exported_sources,
        }
        manifest_payload = canonical_json_bytes(manifest) + b"\n"
        (target / "manifest.json").write_bytes(manifest_payload)
        return {**manifest, "manifest_sha256": sha256_hex(manifest_payload)}

    @staticmethod
    def _read_bundle(bundle: Path) -> tuple[dict[str, Any], bytes, list[RecordEnvelope], dict[str, bytes]]:
        manifest_path = bundle / "manifest.json"
        if not manifest_path.exists():
            raise ValidationError("Import bundle requires manifest.json")
        raw_manifest = manifest_path.read_bytes()
        manifest = strict_json_loads(raw_manifest)
        if not isinstance(manifest, dict):
            raise ValidationError("Export manifest must be an object")
        if canonical_json_bytes(manifest) + b"\n" != raw_manifest:
            raise ValidationError("Export manifest must use exact canonical JSON plus one newline")
        if set(manifest) != _EXPORT_KEYS:
            raise ValidationError("Export manifest keys are incomplete or unknown")
        if manifest.get("schema") != "LANTERN_EXPORT_MANIFEST_V1":
            raise ValidationError("Unsupported export manifest")
        validate_project_manifest(manifest.get("project_manifest"))
        if manifest.get("records_path") != "records.ndjson":
            raise ValidationError("Unsupported records_path")
        records_path = bundle / "records.ndjson"
        if not records_path.exists():
            raise ValidationError("Import bundle requires records.ndjson")
        records_bytes = records_path.read_bytes()
        if sha256_hex(records_bytes) != manifest.get("records_sha256"):
            raise ValidationError("records.ndjson digest mismatch")
        parsed = [parse_record(line) for line in records_bytes.decode("utf-8").splitlines() if line]
        if manifest.get("record_count") != len(parsed):
            raise ValidationError("Export manifest record_count mismatch")
        duplicate_ids = [rid for rid, count in _counts(r.record_id for r in parsed).items() if count > 1]
        if duplicate_ids:
            raise ValidationError(f"Duplicate record IDs in import bundle: {duplicate_ids}")

        sources_value = manifest.get("sources")
        if not isinstance(sources_value, list):
            raise ValidationError("Export manifest sources must be a list")
        source_blobs: dict[str, bytes] = {}
        previous_digest = ""
        for item in sources_value:
            if not isinstance(item, dict) or set(item) != _SOURCE_ENTRY_KEYS:
                raise ValidationError("Invalid source manifest entry")
            digest = item.get("sha256")
            size = item.get("size")
            if not isinstance(digest, str) or len(digest) != 64 or not isinstance(size, int) or size < 0:
                raise ValidationError("Invalid source manifest digest or size")
            if digest <= previous_digest:
                raise ValidationError("Source manifest entries must be unique and sorted")
            previous_digest = digest
            source_path = bundle / "sources" / digest
            if not source_path.exists():
                raise ValidationError(f"Missing source blob: {digest}")
            content = source_path.read_bytes()
            if len(content) != size or sha256_hex(content) != digest:
                raise ValidationError(f"Divergent source blob: {digest}")
            source_blobs[digest] = content
        return manifest, records_bytes, parsed, source_blobs

    def _preflight_import(self, source: str | Path) -> dict[str, Any]:
        bundle = Path(source)
        manifest, records_bytes, parsed, source_blobs = self._read_bundle(bundle)
        project_manifest = manifest["project_manifest"]
        if project_manifest != self.manifest():
            raise ConflictError("Bundle ProjectManifest is incompatible with target store")
        if any(record.project_id != self.project_id for record in parsed):
            raise ValidationError("Import project_id does not match target store")

        by_id = {record.record_id: record for record in parsed}
        existing_cache: dict[str, RecordEnvelope | None] = {}

        def lookup(record_id: str) -> RecordEnvelope | None:
            if record_id in by_id:
                return by_id[record_id]
            if record_id not in existing_cache:
                existing_cache[record_id] = self._lookup_record(record_id)
            return existing_cache[record_id]

        for record in _topological_records(parsed):
            content = None
            if record.record_type == "SourceSnapshot":
                digest = record.payload.get("content_sha256")
                if isinstance(digest, str):
                    content = source_blobs.get(digest)
            validate_record_semantics(record, lookup, source_content=content)

        referenced = {
            record.payload["content_sha256"]
            for record in parsed
            if record.record_type == "SourceSnapshot"
            and record.payload.get("custody_mode") in {"CAPTURED", "EMBEDDED"}
        }
        if referenced != set(source_blobs):
            missing = sorted(referenced - set(source_blobs))
            undeclared = sorted(set(source_blobs) - referenced)
            raise ValidationError(f"Source manifest/reference mismatch; missing={missing}, undeclared={undeclared}")

        outcomes: dict[str, str] = {}
        conflicts: set[str] = set()
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
                conflicts.add(record.record_id)
        skipped = _dependency_closure(by_id, conflicts)
        for record_id in skipped:
            outcomes.setdefault(record_id, "SKIPPED")
        to_create = [record for record in _topological_records(parsed) if record.record_id not in outcomes]

        # Simulate lineage rules before any durable effect.
        heads = {
            (row["project_id"], row["record_type"], row["lineage_key"]): row["record_id"]
            for row in self._connection.execute("select * from lineage_heads").fetchall()
        }
        for record in to_create:
            if record.record_type == "StateEvent" or record.lineage_key is None:
                continue
            key = (record.project_id, record.record_type, record.lineage_key)
            current = heads.get(key)
            if record.predecessor_record_id is None:
                if current is not None:
                    raise ConflictError("A current lineage head already exists")
            elif current != record.predecessor_record_id:
                raise ConflictError("Stale predecessor or competing successor")
            heads[key] = record.record_id

        return {
            "bundle": bundle,
            "manifest": manifest,
            "records_bytes": records_bytes,
            "parsed": parsed,
            "source_blobs": source_blobs,
            "outcomes": outcomes,
            "to_create": to_create,
            "operation_id": f"import:{sha256_hex(canonical_json_bytes(manifest))}:{manifest['records_sha256']}",
        }

    def import_bundle(self, source: str | Path) -> dict[str, Any]:
        plan = self._preflight_import(source)
        file_op = stage_source_blobs(self.root, plan["operation_id"], plan["source_blobs"])
        outcomes: dict[str, str] = dict(plan["outcomes"])
        try:
            with self.transaction():
                for record in plan["to_create"]:
                    self._insert_record_row(record)
                    outcomes[record.record_id] = "CREATED"
                self._rebuild_projections()
                file_op.promote()
                hook = getattr(self, "_import_failure_hook", None)
                if hook is not None:
                    hook()
                self._connection.execute(
                    "insert or ignore into file_operations(operation_id,status,committed_at) values (?,?,?)",
                    (plan["operation_id"], "COMMITTED", datetime.now(UTC).isoformat().replace("+00:00", "Z")),
                )
        except Exception:
            file_op.rollback_files()
            raise
        file_op.cleanup_after_success()
        ordered_results = [{"record_id": record.record_id, "outcome": outcomes[record.record_id]}
                           for record in plan["parsed"]]
        summary: dict[str, int] = defaultdict(int)
        for result in ordered_results:
            summary[result["outcome"]] += 1
        return {"schema": "LANTERN_IMPORT_RECEIPT_V1", "project_id": self.project_id,
                "project_manifest_sha256": sha256_hex(manifest_bytes(self.manifest())),
                "results": ordered_results, "summary": dict(sorted(summary.items()))}

    @classmethod
    def import_bundle_new(cls, target_root: str | Path, source: str | Path, *, actor_id: str = "importer") -> dict[str, Any]:
        target = Path(target_root)
        if target.exists():
            raise ConflictError("Clean import target must not already exist")
        bundle = Path(source)
        manifest, _, _, _ = cls._read_bundle(bundle)
        project_manifest = manifest["project_manifest"]
        temp = target.with_name(f".{target.name}.lantern-import-{sha256_hex(str(target))[:12]}")
        if temp.exists():
            shutil.rmtree(temp)
        try:
            with cls.initialize(temp, manifest=project_manifest, actor_id=actor_id) as store:
                receipt = store.import_bundle(bundle)
                store.verify_manifest_consistency()
            os.replace(temp, target)
            return receipt
        except Exception:
            shutil.rmtree(temp, ignore_errors=True)
            raise

    def _rebuild_projections(self) -> None:
        rows = self._connection.execute("select * from records order by created_at,record_id").fetchall()
        records = [self._row_to_record(row) for row in rows]
        by_id = {record.record_id: record for record in records}
        lookup = by_id.get
        for record in _topological_records(records):
            validate_record_semantics(record, lookup)

        self._connection.execute("delete from lineage_heads")
        self._connection.execute("delete from links")
        self._connection.execute("delete from state_heads")
        self._connection.execute("delete from state_events")
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
                "insert into lineage_heads(project_id,record_type,lineage_key,record_id) values (?,?,?,?)",
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
