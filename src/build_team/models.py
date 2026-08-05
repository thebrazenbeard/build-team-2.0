from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

BT2_ABBREVIATION = "BT2"
BT2_NAME = "Build Team Two"
BT2_VERSION = 2
BT2_MEANING = (
    "Build Team Two is version 2 of the Build Team system; "
    "it is not the second of two build teams."
)
BT2_COORDINATOR_ROLE = "BT2 Coordinator"

FacetName = Literal[
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Thirteen",
]

ANALYSIS_FACETS: tuple[FacetName, ...] = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Thirteen",
)
ALL_FACETS: tuple[FacetName, ...] = ("One",) + ANALYSIS_FACETS


class MemoryEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str
    content: dict[str, Any]
    source_facets: list[FacetName] = Field(default_factory=list)
    authority_class: str
    provenance: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class HivemindSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    collective_slug: str = "build-team-2"
    task_id: str
    objective: str
    constraints: list[str] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    shared_memory: list[MemoryEvent] = Field(default_factory=list)
    shared_state: dict[str, Any] = Field(default_factory=dict)
    approval_gates: list[str] = Field(default_factory=list)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def canonical_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


class Perspective(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facet: FacetName
    snapshot_digest: str
    summary: str
    observations: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    proposals: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    disagreements: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def analysis_facet_only(self) -> Perspective:
        if self.facet == "One":
            raise ValueError("One synthesizes; One does not emit an analysis perspective")
        return self


class FailedFacet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facet: FacetName
    error_class: str
    message: str


class CollectiveDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    speaker: Literal["One"] = "One"
    coordinator_role: Literal["BT2 Coordinator"] = "BT2 Coordinator"
    snapshot_digest: str
    decision: str
    rationale: list[str] = Field(default_factory=list)
    action_sequence: list[str] = Field(default_factory=list)
    efficiency_choices: list[str] = Field(default_factory=list)
    rejected_alternatives: list[str] = Field(default_factory=list)
    material_dissent: list[str] = Field(default_factory=list)
    evidence_used: list[str] = Field(default_factory=list)
    approval_required: list[str] = Field(default_factory=list)
    unresolved_items: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
