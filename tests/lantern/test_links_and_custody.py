from __future__ import annotations

import pytest

from lantern.store import ValidationError


def test_closed_link_matrix_prevents_dependency_cycles(seeded_store, fixture_data: dict) -> None:
    decision_id = next(
        op["args"]["record_id"] for op in fixture_data["operations"] if op["operation"] == "decision.record"
    )
    before = seeded_store._connection.execute("select count(*) from records").fetchone()[0]
    with pytest.raises(ValidationError, match="endpoint matrix"):
        seeded_store.add_link(
            actor_id="operator-1",
            link_type="DEPENDS_ON",
            source_record_id=decision_id,
            target_record_id=decision_id,
        )
    assert seeded_store._connection.execute("select count(*) from records").fetchone()[0] == before


def test_source_custody_bytes_are_content_addressed(seeded_store) -> None:
    rows = seeded_store._connection.execute(
        "select payload_json from records where record_type='SourceSnapshot' order by created_at"
    ).fetchall()
    assert len(rows) == 2
    for row in rows:
        import json

        payload = json.loads(row["payload_json"])
        digest = payload["content_sha256"]
        assert payload["custody_mode"] == "CAPTURED"
        assert (seeded_store.sources_path / digest).exists()
