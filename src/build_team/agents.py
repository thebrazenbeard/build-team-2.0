from __future__ import annotations

import os
from functools import lru_cache

from agents import Agent

from .models import CollectiveDecision, Perspective
from .prompts import build_analysis_instructions, build_synthesis_instructions
from .roster import ROSTER


def _model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@lru_cache(maxsize=9)
def analysis_agent(name: str) -> Agent[None]:
    definition = ROSTER[name]  # type: ignore[index]
    if definition.synthesizer:
        raise ValueError("One cannot be created as an analysis agent")
    return Agent(
        name=name,
        instructions=build_analysis_instructions(name),
        model=_model_name(),
        output_type=Perspective,
    )


@lru_cache(maxsize=1)
def synthesis_agent() -> Agent[None]:
    return Agent(
        name="One",
        instructions=build_synthesis_instructions(),
        model=_model_name(),
        output_type=CollectiveDecision,
    )
