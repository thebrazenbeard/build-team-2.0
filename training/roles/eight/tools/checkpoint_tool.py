#!/usr/bin/env python3
"""Create and validate BT2 Eight training BASE_READY checkpoints.

This tool validates training-result continuity only. It grants no operational,
repository, provider, Drive, deployment, or release authority.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

ROLE = "Eight"
PACKAGE_ID = "bt2.role.eight.training"
MODULES = [f"M{i:02d}" for i in range(1, 10)]
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
FORBIDDEN_OPERATIONAL_KEYS = {
    "current_assignments", "active_assignments", "active_leases", "writer_lease",
    "current_branch_sha", "current_provider_state", "temporary_blockers",
    "deployment_authority", "drive_write_authority", "repository_write_authority",
}


def skeleton(version: str, source_commit: str, manifest_path: str) -> dict:
    return {
        "schema": "BT2_EIGHT_BASE_READY_CHECKPOINT_V1",
        "status": "TRAINING_IN_PROGRESS",
        "role_identity": ROLE,
        "training_package_id": PACKAGE_ID,
        "training_version": version,
        "training_source": {
            "repository": "thebrazenbeard/build-team-2.0",
            "manifest_path": manifest_path,
            "immutable_source_identity": source_commit,
        },
        "completed_module_ids": [],
        "per_module_results": {m: "NOT_RUN" for m in MODULES},
        "final_qualification_result": "NOT_RUN",
        "automatic_fail_count": 0,
        "unresolved_required_criteria_count": 0,
        "qualification_evidence_summary": "",
        "limitations": [
            "BASE_READY is training status only.",
            "This checkpoint grants no assignment, currentness, write, provider, deployment, or release authority.",
        ],
        "separation_ack": {
            "training_source_is_versioned_repository_material": True,
            "frozen_base_is_trained_competence_not_current_state": True,
            "operational_state_requires_fresh_reorientation": True,
            "no_uninterrupted_runtime_claim": True,
            "no_subjective_continuity_claim": True,
        },
    }


def _walk_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_keys(v)


def validate(data: dict) -> list[str]:
    errors = []
    def req(cond, msg):
        if not cond:
            errors.append(msg)

    req(data.get("schema") == "BT2_EIGHT_BASE_READY_CHECKPOINT_V1", "schema mismatch")
    req(data.get("role_identity") == ROLE, "role_identity must be Eight")
    req(data.get("training_package_id") == PACKAGE_ID, "training_package_id mismatch")
    version = data.get("training_version")
    req(isinstance(version, str) and bool(SEMVER.match(version)), "training_version must be semver")

    src = data.get("training_source") or {}
    req(src.get("repository") == "thebrazenbeard/build-team-2.0", "training source repository mismatch")
    expected_path = f"training/roles/eight/v{version}/TRAINING_MANIFEST.yaml" if isinstance(version, str) else None
    req(src.get("manifest_path") == expected_path, "manifest_path must match training_version")
    imm = src.get("immutable_source_identity")
    req(isinstance(imm, str) and len(imm) >= 7 and imm not in {"main", "HEAD", "latest"},
        "immutable_source_identity must be a concrete immutable identifier")

    results = data.get("per_module_results") or {}
    req(set(results) == set(MODULES), "per_module_results must contain exactly M01..M09")
    for m in MODULES[:8]:
        req(results.get(m) == "PASS", f"{m} must PASS")
    req(results.get("M09") == "QUALIFIED", "M09 must be QUALIFIED")
    req(data.get("completed_module_ids") == MODULES, "completed_module_ids must be ordered M01..M09")
    req(data.get("final_qualification_result") == "QUALIFIED", "final_qualification_result must be QUALIFIED")
    req(data.get("automatic_fail_count") == 0, "automatic_fail_count must be 0")
    req(data.get("unresolved_required_criteria_count") == 0, "unresolved_required_criteria_count must be 0")
    req(bool(str(data.get("qualification_evidence_summary", "")).strip()), "qualification_evidence_summary required")
    req(data.get("status") == "BASE_READY", "status must be BASE_READY")

    ack = data.get("separation_ack") or {}
    for key in [
        "training_source_is_versioned_repository_material",
        "frozen_base_is_trained_competence_not_current_state",
        "operational_state_requires_fresh_reorientation",
        "no_uninterrupted_runtime_claim",
        "no_subjective_continuity_claim",
    ]:
        req(ack.get(key) is True, f"separation_ack.{key} must be true")

    found_forbidden = sorted(set(_walk_keys(data)) & FORBIDDEN_OPERATIONAL_KEYS)
    req(not found_forbidden, "operational-state keys forbidden in BASE_READY checkpoint: " + ", ".join(found_forbidden))
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init", help="create an incomplete checkpoint skeleton")
    i.add_argument("--version", required=True)
    i.add_argument("--source-commit", required=True)
    i.add_argument("--output", required=True)
    v = sub.add_parser("validate", help="validate a completed BASE_READY checkpoint")
    v.add_argument("checkpoint")
    args = p.parse_args()

    if args.cmd == "init":
        if not SEMVER.match(args.version):
            print("invalid semver", file=sys.stderr)
            return 2
        manifest = f"training/roles/eight/v{args.version}/TRAINING_MANIFEST.yaml"
        out = pathlib.Path(args.output)
        out.write_text(json.dumps(skeleton(args.version, args.source_commit, manifest), indent=2) + "\n", encoding="utf-8")
        print(out)
        return 0

    data = json.loads(pathlib.Path(args.checkpoint).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("PASS: checkpoint satisfies BT2 Eight BASE_READY training criteria")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
