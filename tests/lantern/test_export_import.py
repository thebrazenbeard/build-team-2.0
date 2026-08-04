from __future__ import annotations

import json
from pathlib import Path

import pytest

from lantern.canonical import canonical_json_bytes, sha256_hex
from lantern.contracts import build_record, parse_record
from lantern.store import ConflictError, LanternStore, ValidationError


def _rewrite_records(bundle: Path, lines: list[str]) -> None:
    records_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    (bundle / "records.ndjson").write_bytes(records_bytes)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    manifest["records_sha256"] = sha256_hex(records_bytes)
    (bundle / "manifest.json").write_bytes(canonical_json_bytes(manifest) + b"\n")


def _empty_compatible_store(root: Path, source_store) -> LanternStore:
    return LanternStore.initialize(root, manifest=source_store.manifest())


def test_clean_export_import_preserves_exact_manifest_records_and_queries(seeded_store, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    target_root = tmp_path / "target"
    receipt = LanternStore.import_bundle_new(target_root, bundle)
    assert receipt["summary"] == {"CREATED": len(receipt["results"])}
    assert (target_root / "project-manifest.json").read_bytes() == (seeded_store.root / "project-manifest.json").read_bytes()
    with LanternStore.open(target_root) as target:
        assert target.manifest() == seeded_store.manifest()
        assert target.status() == seeded_store.status()
        second = target.import_bundle(bundle)
        assert second["summary"] == {"VERIFIED": len(second["results"])}
        roundtrip = tmp_path / "roundtrip"
        target.export_bundle(roundtrip)
        assert (bundle / "records.ndjson").read_bytes() == (roundtrip / "records.ndjson").read_bytes()
        assert (bundle / "manifest.json").read_bytes() == (roundtrip / "manifest.json").read_bytes()


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
        payload={**original.payload, "retention_status": "DIVERGENT_LOCAL_COPY"},
    )
    lines[0] = divergent.canonical_json
    _rewrite_records(bundle, lines)
    before = seeded_store.get_record(original.record_id).canonical_json
    receipt = seeded_store.import_bundle(bundle)
    result = next(item for item in receipt["results"] if item["record_id"] == original.record_id)
    assert result["outcome"] == "CONFLICT"
    assert seeded_store.get_record(original.record_id).canonical_json == before


def test_import_skips_records_that_depend_on_a_conflicting_id(seeded_store, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    source = next(
        seeded_store._row_to_record(row)
        for row in seeded_store._connection.execute(
            "select * from records where record_type='SourceSnapshot' order by created_at"
        )
    )
    target = _empty_compatible_store(tmp_path / "target", seeded_store)
    try:
        divergent = build_record(
            project_id=source.project_id,
            record_id=source.record_id,
            record_type="SourceSnapshot",
            actor_id=source.actor_id,
            created_at=source.created_at,
            observed_at=source.observed_at,
            provenance=source.provenance,
            lineage_key=source.lineage_key,
            payload={**source.payload, "retention_status": "DIVERGENT_LOCAL_COPY"},
        )
        assert target.insert_record(divergent).outcome == "CREATED"
        receipt = target.import_bundle(bundle)
        outcomes = {item["record_id"]: item["outcome"] for item in receipt["results"]}
        assert outcomes[source.record_id] == "CONFLICT"
        assert "SKIPPED" in outcomes.values()
    finally:
        target.close()


@pytest.mark.parametrize("failure", ["missing", "wrong_size", "divergent", "undeclared"])
def test_source_preflight_failure_leaves_database_and_source_directory_unchanged(
    seeded_store, tmp_path: Path, failure: str
) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    manifest_path = bundle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = manifest["sources"][0]["sha256"]
    source_path = bundle / "sources" / digest
    if failure == "missing":
        source_path.unlink()
    elif failure == "wrong_size":
        manifest["sources"][0]["size"] += 1
        manifest_path.write_bytes(canonical_json_bytes(manifest) + b"\n")
    elif failure == "divergent":
        source_path.write_bytes(b"divergent")
    else:
        extra = b"undeclared"
        extra_digest = sha256_hex(extra)
        (bundle / "sources" / extra_digest).write_bytes(extra)
        manifest["sources"].append({"sha256": extra_digest, "size": len(extra)})
        manifest["sources"].sort(key=lambda item: item["sha256"])
        manifest_path.write_bytes(canonical_json_bytes(manifest) + b"\n")
    target = _empty_compatible_store(tmp_path / "target", seeded_store)
    try:
        before_records = target._connection.execute("select count(*) from records").fetchone()[0]
        before_files = sorted(path.name for path in target.sources_path.iterdir())
        with pytest.raises((ValidationError, ConflictError)):
            target.import_bundle(bundle)
        assert target._connection.execute("select count(*) from records").fetchone()[0] == before_records
        assert sorted(path.name for path in target.sources_path.iterdir()) == before_files
    finally:
        target.close()


def test_failure_after_blob_promotion_rolls_back_database_and_files_then_retry_is_idempotent(
    seeded_store, tmp_path: Path
) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    target = _empty_compatible_store(tmp_path / "target", seeded_store)
    try:
        target._import_failure_hook = lambda: (_ for _ in ()).throw(RuntimeError("injected"))
        with pytest.raises(RuntimeError, match="injected"):
            target.import_bundle(bundle)
        assert target._connection.execute("select count(*) from records").fetchone()[0] == 0
        assert list(target.sources_path.iterdir()) == []
        del target._import_failure_hook
        receipt = target.import_bundle(bundle)
        assert receipt["summary"] == {"CREATED": len(receipt["results"])}
        second = target.import_bundle(bundle)
        assert second["summary"] == {"VERIFIED": len(second["results"])}
        assert len(list(target.sources_path.iterdir())) == len(json.loads((bundle / "manifest.json").read_text())["sources"])
    finally:
        target.close()


def test_existing_store_manifest_incompatibility_and_bundle_manifest_tampering_fail_before_mutation(
    seeded_store, tmp_path: Path
) -> None:
    bundle = tmp_path / "bundle"
    seeded_store.export_bundle(bundle)
    incompatible = LanternStore.initialize(tmp_path / "incompatible", project_id=seeded_store.project_id)
    try:
        with pytest.raises(ConflictError, match="ProjectManifest"):
            incompatible.import_bundle(bundle)
        assert incompatible._connection.execute("select count(*) from records").fetchone()[0] == 0
    finally:
        incompatible.close()

    manifest_path = bundle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["project_manifest"]["custody_policy"] = "MUTATED"
    manifest_path.write_bytes(canonical_json_bytes(manifest) + b"\n")
    target = _empty_compatible_store(tmp_path / "target", seeded_store)
    try:
        with pytest.raises(ValidationError, match="custody"):
            target.import_bundle(bundle)
        assert target._connection.execute("select count(*) from records").fetchone()[0] == 0
    finally:
        target.close()
