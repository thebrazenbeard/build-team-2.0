from __future__ import annotations

import os
from typing import Any

from supabase import Client, create_client

from build_team.models import CollectiveDecision, HivemindSnapshot, MemoryEvent, Perspective


class SupabaseSharedStore:
    """Durable collective storage through narrow service-role-only RPCs."""

    def __init__(self, client: Client) -> None:
        self._client = client

    @classmethod
    def from_env(cls) -> "SupabaseSharedStore":
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SECRET_KEY"]
        return cls(create_client(url, key))

    def load_recent_memory(self, collective_slug: str, limit: int) -> list[MemoryEvent]:
        response = self._client.rpc(
            "bt2_load_recent_memory",
            {"p_slug": collective_slug, "p_limit": limit},
        ).execute()
        rows: list[dict[str, Any]] = response.data or []
        return [MemoryEvent.model_validate(row) for row in rows]

    def create_task(self, snapshot: HivemindSnapshot) -> None:
        payload = {
            "collective_slug": snapshot.collective_slug,
            "task_id": snapshot.task_id,
            "objective": snapshot.objective,
            "snapshot_digest": snapshot.digest(),
            "snapshot": snapshot.model_dump(mode="json"),
        }
        self._client.rpc("bt2_create_task", {"p_snapshot": payload}).execute()

    def save_perspective(self, task_id: str, perspective: Perspective) -> None:
        self._client.rpc(
            "bt2_save_perspective",
            {"p_task_id": task_id, "p_perspective": perspective.model_dump(mode="json")},
        ).execute()

    def save_decision(self, task_id: str, decision: CollectiveDecision) -> None:
        self._client.rpc(
            "bt2_save_decision",
            {"p_task_id": task_id, "p_decision": decision.model_dump(mode="json")},
        ).execute()

    def append_memory(self, task_id: str, event: MemoryEvent) -> None:
        self._client.rpc(
            "bt2_append_memory",
            {"p_task_id": task_id, "p_event": event.model_dump(mode="json")},
        ).execute()
