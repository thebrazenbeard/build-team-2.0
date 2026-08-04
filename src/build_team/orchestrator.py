from __future__ import annotations

import asyncio
import os
import uuid
from collections.abc import Iterable
from typing import Any

from agents import RunConfig, Runner, trace

from .agents import analysis_agent, synthesis_agent
from .models import (
    ANALYSIS_FACETS,
    CollectiveDecision,
    FailedFacet,
    HivemindSnapshot,
    MemoryEvent,
    Perspective,
)
from .prompts import build_analysis_prompt, build_synthesis_prompt
from .storage.base import SharedStore


class HivemindOrchestrator:
    def __init__(self, store: SharedStore) -> None:
        self.store = store

    def snapshot(
        self,
        objective: str,
        *,
        constraints: Iterable[str] = (),
        evidence: Iterable[dict[str, Any]] = (),
        shared_state: dict[str, Any] | None = None,
        approval_gates: Iterable[str] = (),
        task_id: str | None = None,
    ) -> HivemindSnapshot:
        slug = os.getenv("BUILD_TEAM_COLLECTIVE_SLUG", "build-team-2")
        max_events = int(os.getenv("BUILD_TEAM_MAX_MEMORY_EVENTS", "40"))
        memory = self.store.load_recent_memory(slug, max_events)
        return HivemindSnapshot(
            collective_slug=slug,
            task_id=task_id or str(uuid.uuid4()),
            objective=objective,
            constraints=list(constraints),
            evidence=list(evidence),
            shared_memory=memory,
            shared_state=shared_state or {},
            approval_gates=list(approval_gates),
        )

    async def _run_facet(self, snapshot: HivemindSnapshot, facet: str) -> Perspective:
        result = await Runner.run(
            analysis_agent(facet),
            build_analysis_prompt(snapshot, facet),
            run_config=RunConfig(
                workflow_name="Build Team 2.0 analysis",
                group_id=snapshot.task_id,
                trace_include_sensitive_data=False,
            ),
        )
        perspective = result.final_output_as(Perspective)
        if perspective.facet != facet:
            raise ValueError(f"Facet mismatch: requested {facet}, received {perspective.facet}")
        if perspective.snapshot_digest != snapshot.digest():
            raise ValueError(f"Snapshot digest mismatch from {facet}")
        return perspective

    async def run(self, snapshot: HivemindSnapshot) -> CollectiveDecision:
        self.store.create_task(snapshot)
        perspectives: list[Perspective] = []
        failures: list[FailedFacet] = []

        with trace(
            workflow_name="Build Team 2.0 collective",
            group_id=snapshot.task_id,
            metadata={"snapshot_digest": snapshot.digest()},
        ):
            outcomes = await asyncio.gather(
                *(self._run_facet(snapshot, facet) for facet in ANALYSIS_FACETS),
                return_exceptions=True,
            )

            for facet, outcome in zip(ANALYSIS_FACETS, outcomes, strict=True):
                if isinstance(outcome, Exception):
                    failures.append(
                        FailedFacet(
                            facet=facet,
                            error_class=type(outcome).__name__,
                            message=str(outcome),
                        )
                    )
                    continue
                self.store.save_perspective(snapshot.task_id, outcome)
                perspectives.append(outcome)

            if not perspectives:
                raise RuntimeError("No analysis facet completed; collective synthesis is impossible")

            result = await Runner.run(
                synthesis_agent(),
                build_synthesis_prompt(
                    snapshot,
                    perspectives,
                    [failure.model_dump(mode="json") for failure in failures],
                ),
                run_config=RunConfig(
                    workflow_name="Build Team 2.0 synthesis",
                    group_id=snapshot.task_id,
                    trace_include_sensitive_data=False,
                ),
            )
            decision = result.final_output_as(CollectiveDecision)

        if decision.snapshot_digest != snapshot.digest():
            raise ValueError("One returned a decision for the wrong snapshot")

        self.store.save_decision(snapshot.task_id, decision)
        self.store.append_memory(
            snapshot.task_id,
            MemoryEvent(
                event_type="collective_decision",
                content=decision.model_dump(mode="json"),
                source_facets=[perspective.facet for perspective in perspectives] + ["One"],
                authority_class="COLLECTIVE_DECISION",
                provenance={
                    "task_id": snapshot.task_id,
                    "snapshot_digest": snapshot.digest(),
                    "failed_facets": [failure.model_dump(mode="json") for failure in failures],
                },
            ),
        )
        return decision
