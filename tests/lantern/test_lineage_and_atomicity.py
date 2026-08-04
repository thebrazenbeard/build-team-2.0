from __future__ import annotations

import pytest

from lantern.store import ValidationError


def test_stale_competing_successor_has_no_partial_database_or_source_effects(seeded_store, fixture_data: dict) -> None:
    source_ops = [op for op in fixture_data["operations"] if op["operation"] == "source.observe"]
    source_a = source_ops[0]["args"]["record_id"]
    before_records = seeded_store._connection.execute("select count(*) from records").fetchone()[0]
    before_events = seeded_store._connection.execute("select count(*) from state_events").fetchone()[0]
    before_files = sorted(path.name for path in seeded_store.sources_path.iterdir())
    result = seeded_store.observe_source(
        actor_id="operator-1",
        source_key="fixture-source",
        locator="fixture/source.md",
        retrieval_route="TEST",
        media_type="text/markdown",
        custody_mode="CAPTURED",
        retention_status="RETAINED",
        observed_at="2026-08-04T12:20:00Z",
        content=b"Competing successor",
        predecessor_record_id=source_a,
    )
    assert result.outcome == "CONFLICT"
    assert seeded_store._connection.execute("select count(*) from records").fetchone()[0] == before_records
    assert seeded_store._connection.execute("select count(*) from state_events").fetchone()[0] == before_events
    assert sorted(path.name for path in seeded_store.sources_path.iterdir()) == before_files


def test_invalid_timestamp_fails_before_source_staging(seeded_store) -> None:
    before = sorted(path.name for path in seeded_store.sources_path.iterdir())
    with pytest.raises(ValueError):
        seeded_store.observe_source(
            actor_id="operator-1", source_key="bad-time", locator="bad", retrieval_route="TEST",
            media_type="text/plain", custody_mode="CAPTURED", retention_status="RETAINED",
            observed_at="not-a-time", content=b"bytes",
        )
    assert sorted(path.name for path in seeded_store.sources_path.iterdir()) == before


def test_successor_projection_and_events_commit_together(seeded_store, fixture_data: dict) -> None:
    source_ops = [op for op in fixture_data["operations"] if op["operation"] == "source.observe"]
    source_a = source_ops[0]["args"]["record_id"]
    source_b = source_ops[1]["args"]["record_id"]
    head = seeded_store._connection.execute(
        "select record_id from lineage_heads where record_type='SourceSnapshot' and lineage_key='fixture-source'"
    ).fetchone()[0]
    assert head == source_b
    assert seeded_store._connection.execute(
        "select count(*) from state_events where subject_record_id=? and event_type='SUPERSEDED'", (source_a,)
    ).fetchone()[0] == 1
    assert seeded_store._connection.execute(
        "select count(*) from state_events where event_type='REVIEW_REQUIRED'"
    ).fetchone()[0] == 2
