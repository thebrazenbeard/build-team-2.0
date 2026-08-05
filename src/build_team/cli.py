from __future__ import annotations

import asyncio
import json
import os
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from .orchestrator import HivemindOrchestrator
from .roster import ROSTER
from .storage import InMemorySharedStore
from .storage.supabase_store import SupabaseSharedStore

app = typer.Typer(no_args_is_help=True)
console = Console()


def _store(durable: bool):
    if durable:
        return SupabaseSharedStore.from_env()
    return InMemorySharedStore()


@app.command()
def roster() -> None:
    """Display the ten facets and their productive biases."""
    table = Table(title="Build Team Two (BT2) — Build Team system version 2")
    table.add_column("Facet")
    table.add_column("Permanent role")
    table.add_column("Lens")
    table.add_column("Temperament")
    table.add_column("Productive bias")
    table.add_column("Blind spot")
    for facet in ROSTER.values():
        table.add_row(
            facet.name,
            facet.permanent_role or "—",
            facet.lens,
            facet.temperament,
            facet.productive_bias,
            facet.blind_spot,
        )
    console.print(table)


@app.command("inspect-snapshot")
def inspect_snapshot(
    objective: Annotated[str, typer.Argument(help="The task objective")],
) -> None:
    """Create and print the exact shared snapshot without calling a model."""
    load_dotenv()
    orchestrator = HivemindOrchestrator(_store(False))
    snapshot = orchestrator.snapshot(objective)
    console.print(snapshot.canonical_json())
    console.print(f"sha256={snapshot.digest()}")


@app.command("run")
def run_collective(
    objective: Annotated[str, typer.Argument(help="The task objective")],
    durable: Annotated[
        bool,
        typer.Option("--durable/--local", help="Persist shared state in Supabase"),
    ] = True,
) -> None:
    """Run all ten facets over one shared task snapshot."""
    load_dotenv()
    if "OPENAI_API_KEY" not in os.environ:
        raise typer.BadParameter("OPENAI_API_KEY is required for a live collective run")
    orchestrator = HivemindOrchestrator(_store(durable))
    snapshot = orchestrator.snapshot(
        objective,
        approval_gates=[
            "merge",
            "production write",
            "credential change",
            "destructive action",
            "paid infrastructure",
        ],
    )
    decision = asyncio.run(orchestrator.run(snapshot))
    console.print_json(json.dumps(decision.model_dump(mode="json")))


if __name__ == "__main__":
    app()
