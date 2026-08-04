from __future__ import annotations

import json

from .models import CollectiveDecision, HivemindSnapshot, Perspective
from .roster import ROSTER

SHARED_RULES = """
You are one cognitive facet of Build Team Two (BT2), version 2 of the Build Team system.
BT2 does not mean the second of two build teams. The collective is a single system.
You have no private history, private memory, private objective, or independent authority.
Use only the shared snapshot supplied in this run.
Do not imply that your perspective is a durable personal belief.
Distinguish evidence, assumptions, inference, and unknowns.
Return only the requested structured output.
""".strip()


def build_analysis_instructions(facet: str) -> str:
    definition = ROSTER[facet]  # type: ignore[index]
    if definition.synthesizer:
        raise ValueError("One does not use analysis instructions")
    return f"{SHARED_RULES}\n\n{definition.instruction}"


def build_analysis_prompt(snapshot: HivemindSnapshot, facet: str) -> str:
    if facet == "One":
        raise ValueError("One does not emit an analysis perspective")
    return (
        f"SHARED_SNAPSHOT_SHA256: {snapshot.digest()}\n"
        "SHARED_SNAPSHOT_JSON:\n"
        f"{snapshot.canonical_json()}\n\n"
        f"Analyze this snapshot through {facet}'s assigned lens."
    )


def build_synthesis_instructions() -> str:
    return f"{SHARED_RULES}\n\n{ROSTER['One'].instruction}"


def build_synthesis_prompt(
    snapshot: HivemindSnapshot,
    perspectives: list[Perspective],
    failed_facets: list[dict[str, str]],
) -> str:
    perspective_json = json.dumps(
        [perspective.model_dump(mode="json") for perspective in perspectives],
        sort_keys=True,
        ensure_ascii=False,
    )
    failure_json = json.dumps(failed_facets, sort_keys=True, ensure_ascii=False)
    return (
        f"SHARED_SNAPSHOT_SHA256: {snapshot.digest()}\n"
        "SHARED_SNAPSHOT_JSON:\n"
        f"{snapshot.canonical_json()}\n\n"
        "PERSPECTIVES_JSON:\n"
        f"{perspective_json}\n\n"
        "FAILED_FACETS_JSON:\n"
        f"{failure_json}\n\n"
        "Synthesize the collective decision. Preserve material dissent, identify efficiency choices, "
        "remove redundant work, and never invent output "
        f"from a failed facet. Return {CollectiveDecision.__name__}."
    )
