from __future__ import annotations

from dataclasses import dataclass, field

from build_team.models import CollectiveDecision, HivemindSnapshot, MemoryEvent, Perspective


@dataclass(slots=True)
class InMemorySharedStore:
    """Single shared store used for tests and local non-durable runs."""

    memory: list[MemoryEvent] = field(default_factory=list)
    tasks: dict[str, HivemindSnapshot] = field(default_factory=dict)
    perspectives: dict[str, list[Perspective]] = field(default_factory=dict)
    decisions: dict[str, CollectiveDecision] = field(default_factory=dict)

    def load_recent_memory(self, collective_slug: str, limit: int) -> list[MemoryEvent]:
        del collective_slug
        return self.memory[-limit:]

    def create_task(self, snapshot: HivemindSnapshot) -> None:
        self.tasks[snapshot.task_id] = snapshot

    def save_perspective(self, task_id: str, perspective: Perspective) -> None:
        self.perspectives.setdefault(task_id, []).append(perspective)

    def save_decision(self, task_id: str, decision: CollectiveDecision) -> None:
        self.decisions[task_id] = decision

    def append_memory(self, task_id: str, event: MemoryEvent) -> None:
        del task_id
        self.memory.append(event)
