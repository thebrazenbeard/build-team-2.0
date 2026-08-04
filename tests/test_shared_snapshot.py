from build_team.models import ANALYSIS_FACETS, HivemindSnapshot
from build_team.prompts import build_analysis_prompt


def test_every_analysis_facet_receives_same_snapshot() -> None:
    snapshot = HivemindSnapshot(task_id="00000000-0000-0000-0000-000000000001", objective="Test")
    digest = snapshot.digest()
    prompts = [build_analysis_prompt(snapshot, facet) for facet in ANALYSIS_FACETS]
    assert all(f"SHARED_SNAPSHOT_SHA256: {digest}" in prompt for prompt in prompts)
    canonical = snapshot.canonical_json()
    assert all(canonical in prompt for prompt in prompts)


def test_snapshot_is_immutable() -> None:
    snapshot = HivemindSnapshot(task_id="00000000-0000-0000-0000-000000000001", objective="Test")
    try:
        snapshot.objective = "Changed"  # type: ignore[misc]
    except Exception:
        pass
    else:
        raise AssertionError("HivemindSnapshot must be immutable")
