from __future__ import annotations


def _fixture_ids(fixture_data: dict) -> dict[str, str]:
    ids: dict[str, str] = {}
    for operation in fixture_data["operations"]:
        args = operation["args"]
        record_id = args.get("record_id")
        if record_id:
            ids[operation["operation"] + ":" + record_id] = record_id
    return ids


def test_stale_competing_successor_has_no_partial_effects(seeded_store, fixture_data: dict) -> None:
    source_ops = [op for op in fixture_data["operations"] if op["operation"] == "source.observe"]
    source_a = source_ops[0]["args"]["record_id"]
    before_records = seeded_store._connection.execute("select count(*) from records").fetchone()[0]
    before_events = seeded_store._connection.execute("select count(*) from state_events").fetchone()[0]
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


def test_successor_projection_and_events_commit_together(seeded_store, fixture_data: dict) -> None:
    source_ops = [op for op in fixture_data["operations"] if op["operation"] == "source.observe"]
    source_a = source_ops[0]["args"]["record_id"]
    source_b = source_ops[1]["args"]["record_id"]
    head = seeded_store._connection.execute(
        "select record_id from lineage_heads where record_type='SourceSnapshot' and lineage_key='fixture-source'"
    ).fetchone()[0]
    assert head == source_b
    superseded = seeded_store._connection.execute(
        "select count(*) from state_events where subject_record_id=? and event_type='SUPERSEDED'",
        (source_a,),
    ).fetchone()[0]
    assert superseded == 1
    review_events = seeded_store._connection.execute(
        "select count(*) from state_events where event_type='REVIEW_REQUIRED'"
    ).fetchone()[0]
    assert review_events == 2
