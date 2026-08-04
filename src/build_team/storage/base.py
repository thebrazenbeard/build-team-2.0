from __future__ import annotations

from typing import Protocol

from build_team.models import CollectiveDecision, HivemindSnapshot, MemoryEvent, Perspective


class SharedStore(Protocol):
    def load_recent_memory(self, collective_slug: str, limit: int) -> list[MemoryEvent]: ...

    def create_task(self, snapshot: HivemindSnapshot) -> None: ...

    def save_perspective(self, task_id: str, perspective: Perspective) -> None: ...

    def save_decision(self, task_id: str, decision: CollectiveDecision) -> None: ...

    def append_memory(self, task_id: str, event: MemoryEvent) -> None: ...
