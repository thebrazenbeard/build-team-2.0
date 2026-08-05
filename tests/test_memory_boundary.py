from build_team.models import MemoryEvent
from build_team.storage.memory import InMemorySharedStore


def test_store_has_no_private_facet_namespace() -> None:
    store = InMemorySharedStore()
    assert not hasattr(store, "private_memory")
    assert not hasattr(store, "facet_sessions")


def test_source_facets_are_provenance_not_ownership() -> None:
    store = InMemorySharedStore()
    event = MemoryEvent(
        event_type="observation",
        content={"claim": "A shared observation"},
        source_facets=["Five", "Thirteen"],
        authority_class="SUPPORTED_INFERENCE",
    )
    store.append_memory("task", event)
    assert store.load_recent_memory("build-team-2", 10) == [event]
