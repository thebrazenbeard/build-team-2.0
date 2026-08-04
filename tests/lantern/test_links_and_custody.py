from __future__ import annotations

import json
from pathlib import Path

import pytest

from lantern.canonical import sha256_hex
from lantern.store import ValidationError


def test_closed_link_matrix_prevents_dependency_cycles(seeded_store, fixture_data: dict) -> None:
    decision_id = next(
        op["args"]["record_id"] for op in fixture_data["operations"] if op["operation"] == "decision.record"
    )
    before = seeded_store._connection.execute("select count(*) from records").fetchone()[0]
    with pytest.raises(ValidationError, match="endpoint matrix"):
        seeded_store.add_link(
            actor_id="operator-1", link_type="DEPENDS_ON",
            source_record_id=decision_id, target_record_id=decision_id,
        )
    assert seeded_store._connection.execute("select count(*) from records").fetchone()[0] == before


def test_source_custody_bytes_are_content_addressed(seeded_store) -> None:
    rows = seeded_store._connection.execute(
        "select payload_json from records where record_type='SourceSnapshot' order by created_at"
    ).fetchall()
    assert len(rows) == 2
    for row in rows:
        payload = json.loads(row["payload_json"])
        digest = payload["content_sha256"]
        assert payload["custody_mode"] == "CAPTURED"
        assert sha256_hex((seeded_store.sources_path / digest).read_bytes()) == digest


def test_invalid_custody_or_record_conflict_leaves_source_directory_unchanged(seeded_store) -> None:
    before = sorted(path.name for path in seeded_store.sources_path.iterdir())
    with pytest.raises(ValidationError, match="cannot retain|requires content"):
        seeded_store.observe_source(
            actor_id="operator-1", source_key="invalid-custody", locator="x", retrieval_route="TEST",
            media_type="text/plain", custody_mode="REFERENCE_ONLY", retention_status="RETAINED",
            observed_at="2026-08-04T13:00:00Z", content=b"not allowed",
        )
    first = seeded_store._connection.execute(
        "select * from records where record_type='SourceSnapshot' order by created_at limit 1"
    ).fetchone()
    result = seeded_store.observe_source(
        actor_id=first["actor_id"], source_key=json.loads(first["payload_json"])["source_key"],
        locator=json.loads(first["payload_json"])["locator"],
        retrieval_route=json.loads(first["payload_json"])["retrieval_route"],
        media_type=json.loads(first["payload_json"])["media_type"], custody_mode="CAPTURED",
        retention_status="DIFFERENT", observed_at=first["observed_at"], content=b"different",
        record_id=first["record_id"], created_at=first["created_at"],
    )
    assert result.outcome == "CONFLICT"
    assert sorted(path.name for path in seeded_store.sources_path.iterdir()) == before


def test_export_excludes_unreferenced_orphan_blob(seeded_store, tmp_path: Path) -> None:
    orphan = b"orphan"
    orphan_digest = sha256_hex(orphan)
    (seeded_store.sources_path / orphan_digest).write_bytes(orphan)
    bundle = tmp_path / "bundle"
    manifest = seeded_store.export_bundle(bundle)
    exported = {entry["sha256"] for entry in manifest["sources"]}
    assert orphan_digest not in exported
    assert not (bundle / "sources" / orphan_digest).exists()
