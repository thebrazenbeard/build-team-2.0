from __future__ import annotations

import json
from pathlib import Path

from lantern.canonical import canonical_json_bytes, sha256_hex
from lantern.contracts import build_record, parse_record
from lantern.store import LanternStore


def test_clean_export_import_reconstructs_exact_records(seeded_store, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    target_root = tmp_path / "target"
    target = LanternStore.initialize(target_root, project_id=seeded_store.project_id, actor_id="importer")
    try:
        receipt = target.import_bundle(bundle)
        assert receipt["summary"] == {"CREATED": len(receipt["results"])}
        second = target.import_bundle(bundle)
        assert second["summary"] == {"VERIFIED": len(second["results"])}
        roundtrip = tmp_path / "roundtrip"
        target.export_bundle(roundtrip)
        assert (bundle / "records.ndjson").read_bytes() == (roundtrip / "records.ndjson").read_bytes()
        assert target.status()["review_required"] == seeded_store.status()["review_required"]
    finally:
        target.close()


def test_divergent_same_id_import_never_overwrites(seeded_store, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    lines = (bundle / "records.ndjson").read_text(encoding="utf-8").splitlines()
    original = parse_record(lines[0])
    divergent = build_record(
        project_id=original.project_id,
        record_id=original.record_id,
        record_type=original.record_type,
        actor_id=original.actor_id,
        created_at=original.created_at,
        observed_at=original.observed_at,
        provenance=original.provenance,
        lineage_key=original.lineage_key,
        predecessor_record_id=original.predecessor_record_id,
        payload={**original.payload, "divergent_test_marker": "must-not-overwrite"},
    )
    lines[0] = divergent.canonical_json
    records_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    (bundle / "records.ndjson").write_bytes(records_bytes)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    manifest["records_sha256"] = sha256_hex(records_bytes)
    (bundle / "manifest.json").write_bytes(canonical_json_bytes(manifest) + b"\n")
    before = seeded_store.get_record(original.record_id).canonical_json
    receipt = seeded_store.import_bundle(bundle)
    result = next(item for item in receipt["results"] if item["record_id"] == original.record_id)
    assert result["outcome"] == "CONFLICT"
    assert seeded_store.get_record(original.record_id).canonical_json == before


def test_import_skips_records_that_depend_on_a_conflicting_id(seeded_store, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle-skipped"
    seeded_store.export_bundle(bundle)
    source_a = next(
        seeded_store._row_to_record(row)
        for row in seeded_store._connection.execute("select * from records where record_type='SourceSnapshot' order by created_at")
    )
    target = LanternStore.initialize(tmp_path / "skip-target", project_id=seeded_store.project_id, actor_id="importer")
    try:
        divergent = build_record(
            project_id=source_a.project_id,
            record_id=source_a.record_id,
            record_type="SourceSnapshot",
            actor_id=source_a.actor_id,
            created_at=source_a.created_at,
            observed_at=source_a.observed_at,
            provenance=source_a.provenance,
            lineage_key=source_a.lineage_key,
            payload={**source_a.payload, "retention_status": "DIVERGENT_LOCAL_COPY"},
        )
        assert target.insert_record(divergent).outcome == "CREATED"
        receipt = target.import_bundle(bundle)
        outcomes = {item["record_id"]: item["outcome"] for item in receipt["results"]}
        assert outcomes[source_a.record_id] == "CONFLICT"
        assert "SKIPPED" in outcomes.values()
        assert target.get_record(source_a.record_id).canonical_json == divergent.canonical_json
    finally:
        target.close()
