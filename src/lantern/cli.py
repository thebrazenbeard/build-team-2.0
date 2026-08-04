from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .benchmark import score_benchmark
from .canonical import canonical_json
from .fixture import apply_fixture
from .store import ConflictError, LanternError, LanternStore, ValidationError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lantern")
    parser.add_argument("--project", default=".lantern", help="Lantern project directory")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Initialize a local Lantern project")
    init.add_argument("--project-id")
    init.add_argument("--actor-id", default="operator")
    init.add_argument("--name", default="Lantern Project")
    init.add_argument("--seed-fixture", help="Apply a frozen fixture after initialization")

    source = commands.add_parser("source", help="SourceSnapshot operations")
    source_commands = source.add_subparsers(dest="source_command", required=True)
    observe = source_commands.add_parser("observe", help="Record an observed source version")
    observe.add_argument("--actor-id", required=True)
    observe.add_argument("--source-key", required=True)
    observe.add_argument("--locator", required=True)
    observe.add_argument("--retrieval-route", required=True)
    observe.add_argument("--media-type", required=True)
    observe.add_argument(
        "--custody-mode",
        required=True,
        choices=["REFERENCE_ONLY", "CAPTURED", "EMBEDDED", "REDACTED", "UNAVAILABLE"],
    )
    observe.add_argument("--retention-status", required=True)
    observe.add_argument("--observed-at", required=True)
    observe.add_argument("--content-file")
    observe.add_argument("--predecessor-record-id")
    observe.add_argument("--record-id")
    observe.add_argument("--created-at")

    claim = commands.add_parser("claim", help="Claim operations")
    claim_commands = claim.add_subparsers(dest="claim_command", required=True)
    claim_add = claim_commands.add_parser("add", help="Create an immutable Claim")
    claim_add.add_argument("--actor-id", required=True)
    claim_add.add_argument("--claim-key", required=True)
    claim_add.add_argument("--text", required=True)
    claim_add.add_argument("--epistemic-class", required=True)
    claim_add.add_argument("--attributable-to", required=True)
    claim_add.add_argument("--predecessor-record-id")
    claim_add.add_argument("--record-id")
    claim_add.add_argument("--created-at")

    assess = commands.add_parser("assess", help="Create an actor-and-scope Assessment")
    assess.add_argument("--actor-id", required=True)
    assess.add_argument("--claim-id", required=True)
    assess.add_argument("--assessor-id", required=True)
    assess.add_argument("--scope-id", required=True)
    assess.add_argument(
        "--disposition",
        required=True,
        choices=["ACCEPTED", "DISPUTED", "REJECTED", "UNVERIFIED"],
    )
    assess.add_argument("--rationale", required=True)
    assess.add_argument("--predecessor-record-id")
    assess.add_argument("--record-id")
    assess.add_argument("--created-at")

    link = commands.add_parser("link", help="Typed Link operations")
    link_commands = link.add_subparsers(dest="link_command", required=True)
    link_add = link_commands.add_parser("add", help="Create a typed immutable Link")
    link_add.add_argument("--actor-id", required=True)
    link_add.add_argument(
        "--type", dest="link_type", required=True, choices=["SUPPORTS", "OPPOSES", "CONTRADICTS", "DEPENDS_ON"]
    )
    link_add.add_argument("--source", dest="source_record_id", required=True)
    link_add.add_argument("--target", dest="target_record_id", required=True)
    link_add.add_argument("--record-id")
    link_add.add_argument("--created-at")

    decision = commands.add_parser("decision", help="Decision operations")
    decision_commands = decision.add_subparsers(dest="decision_command", required=True)
    decision_record = decision_commands.add_parser("record", help="Record an immutable Decision")
    decision_record.add_argument("--actor-id", required=True)
    decision_record.add_argument("--decision-key", required=True)
    decision_record.add_argument("--authority", required=True)
    decision_record.add_argument("--conclusion", required=True)
    decision_record.add_argument("--evidence", action="append", default=[])
    decision_record.add_argument("--assumption", dest="assumptions", action="append", default=[])
    decision_record.add_argument("--alternative", dest="alternatives", action="append", default=[])
    decision_record.add_argument("--predecessor-record-id")
    decision_record.add_argument("--record-id")
    decision_record.add_argument("--created-at")
    decision_trace = decision_commands.add_parser("trace", help="Trace a Decision and its exact dependencies")
    decision_trace.add_argument("--decision-id", required=True)

    commands.add_parser("status", help="Show current assessment and review state")

    export = commands.add_parser("export", help="Export canonical records and retained source bytes")
    export.add_argument("destination")

    import_command = commands.add_parser("import", help="Import a canonical Lantern bundle")
    import_command.add_argument("source")
    import_command.add_argument("--create", action="store_true", help="Initialize the target from the bundle project manifest")
    import_command.add_argument("--actor-id", default="importer")

    benchmark = commands.add_parser("benchmark", help="Frozen benchmark operations")
    benchmark_commands = benchmark.add_subparsers(dest="benchmark_command", required=True)
    benchmark_score = benchmark_commands.add_parser("score", help="Score frozen Lantern versus control measurements")
    benchmark_score.add_argument("--contract", required=True)
    benchmark_score.add_argument("--measurements", required=True)
    benchmark_score.add_argument("--freeze-receipt", required=True)
    benchmark_score.add_argument("--output")

    return parser


def _emit(payload: dict[str, Any]) -> None:
    print(canonical_json(payload))


def _operation_response(command: str, result: Any) -> dict[str, Any]:
    if hasattr(result, "to_dict"):
        body = result.to_dict()
    elif isinstance(result, dict):
        body = result
    else:
        body = {"result": result}
    return {"schema": "LANTERN_CLI_RESPONSE_V1", "command": command, "status": "OK", "result": body}


def _initialize_for_import(project_root: Path, bundle: Path, actor_id: str) -> LanternStore:
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    project_manifest = manifest.get("project_manifest", {})
    project_id = project_manifest.get("project_id")
    project_name = project_manifest.get("project_name", "Imported Lantern Project")
    if not isinstance(project_id, str):
        raise ValidationError("Bundle manifest is missing project_id")
    return LanternStore.initialize(project_root, project_id=project_id, actor_id=actor_id, project_name=project_name)


def run(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.project)
    try:
        if args.command == "init":
            fixture_project_id = None
            if args.seed_fixture:
                fixture = json.loads(Path(args.seed_fixture).read_text(encoding="utf-8"))
                fixture_project_id = fixture.get("project_id")
            project_id = args.project_id or fixture_project_id
            with LanternStore.initialize(root, project_id=project_id, actor_id=args.actor_id, project_name=args.name) as store:
                receipt: dict[str, Any] = {
                    "schema": "LANTERN_INIT_RECEIPT_V1",
                    "project_manifest": store.manifest(),
                }
                if args.seed_fixture:
                    receipt["fixture"] = apply_fixture(store, args.seed_fixture)
                _emit(_operation_response("init", receipt))
            return 0

        if args.command == "benchmark" and args.benchmark_command == "score":
            result = score_benchmark(
                contract_path=args.contract,
                measurements_path=args.measurements,
                freeze_receipt_path=args.freeze_receipt,
                output_path=args.output,
            )
            _emit(_operation_response("benchmark score", result))
            return 0 if result["result"] == "PASS" else 2

        if args.command == "import" and args.create and not (root / LanternStore.DB_NAME).exists():
            store = _initialize_for_import(root, Path(args.source), args.actor_id)
        else:
            store = LanternStore.open(root)
        with store:
            if args.command == "source" and args.source_command == "observe":
                content = Path(args.content_file).read_bytes() if args.content_file else None
                result = store.observe_source(
                    actor_id=args.actor_id,
                    source_key=args.source_key,
                    locator=args.locator,
                    retrieval_route=args.retrieval_route,
                    media_type=args.media_type,
                    custody_mode=args.custody_mode,
                    retention_status=args.retention_status,
                    observed_at=args.observed_at,
                    content=content,
                    predecessor_record_id=args.predecessor_record_id,
                    record_id=args.record_id,
                    created_at=args.created_at,
                )
                command = "source observe"
            elif args.command == "claim" and args.claim_command == "add":
                result = store.add_claim(
                    actor_id=args.actor_id,
                    claim_key=args.claim_key,
                    text=args.text,
                    epistemic_class=args.epistemic_class,
                    attributable_to=args.attributable_to,
                    predecessor_record_id=args.predecessor_record_id,
                    record_id=args.record_id,
                    created_at=args.created_at,
                )
                command = "claim add"
            elif args.command == "assess":
                result = store.add_assessment(
                    actor_id=args.actor_id,
                    claim_id=args.claim_id,
                    assessor_id=args.assessor_id,
                    scope_id=args.scope_id,
                    disposition=args.disposition,
                    rationale=args.rationale,
                    predecessor_record_id=args.predecessor_record_id,
                    record_id=args.record_id,
                    created_at=args.created_at,
                )
                command = "assess"
            elif args.command == "link" and args.link_command == "add":
                result = store.add_link(
                    actor_id=args.actor_id,
                    link_type=args.link_type,
                    source_record_id=args.source_record_id,
                    target_record_id=args.target_record_id,
                    record_id=args.record_id,
                    created_at=args.created_at,
                )
                command = "link add"
            elif args.command == "decision" and args.decision_command == "record":
                result = store.add_decision(
                    actor_id=args.actor_id,
                    decision_key=args.decision_key,
                    authority=args.authority,
                    conclusion=args.conclusion,
                    evidence=args.evidence,
                    assumptions=args.assumptions,
                    alternatives=args.alternatives,
                    predecessor_record_id=args.predecessor_record_id,
                    record_id=args.record_id,
                    created_at=args.created_at,
                )
                command = "decision record"
            elif args.command == "decision" and args.decision_command == "trace":
                result = store.decision_trace(args.decision_id)
                command = "decision trace"
            elif args.command == "status":
                result = store.status()
                command = "status"
            elif args.command == "export":
                result = store.export_bundle(args.destination)
                command = "export"
            elif args.command == "import":
                result = store.import_bundle(args.source)
                command = "import"
            else:
                raise ValidationError("Unsupported command")
            _emit(_operation_response(command, result))
            if hasattr(result, "outcome") and result.outcome == "CONFLICT":
                return 2
            return 0
    except (LanternError, ValueError, OSError, json.JSONDecodeError) as exc:
        _emit(
            {
                "schema": "LANTERN_CLI_RESPONSE_V1",
                "command": getattr(args, "command", "unknown"),
                "status": "ERROR",
                "error": {"class": type(exc).__name__, "message": str(exc)},
            }
        )
        return 2 if isinstance(exc, (ConflictError, ValidationError)) else 1


def main() -> int:
    return run(sys.argv[1:])
