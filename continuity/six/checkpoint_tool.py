#!/usr/bin/env python3
"""Deterministic helper for Six operational checkpoint payloads.

Validates the permanent role/training binding and required checkpoint shape, then
emits canonical compact JSON text plus its SHA-256. It does not write to any
external service and grants no authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "SIX_OPERATIONAL_RESUME_CHECKPOINT_V1"
ROLE_LABEL = "Six"
NUMERICAL_IDENTITY = 6
PACKAGE_ID = "BT2_ROLE_SIX_PERMANENT_TRAINING"
PACKAGE_VERSION = "1.0.0"
MANIFEST_SHA256 = "32ed842c8bb6c2ccc49bb327189da9b03178b403f05ad6b10cca9b5f1ceeff38"
SOURCE_SET_DIGEST = "ef44176582819750193c7d591e9ee449ea8c3d6743a8bff3eb5228baf4fad1cc"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_TOP_LEVEL = {
    "schema",
    "training",
    "role_identity",
    "current_governance",
    "foreground",
    "assignments",
    "immutable_subjects",
    "mutable_observations",
    "operator_evidence",
    "target_runtime",
    "blockers",
    "authority_and_leases",
    "external_effects",
    "handoffs_and_escalations",
    "claim_ceilings",
    "do_not_rerun",
    "evidence_pointers",
    "unknowns",
}


def canonical_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be a JSON object"]

    missing = sorted(REQUIRED_TOP_LEVEL - payload.keys())
    extra = sorted(payload.keys() - REQUIRED_TOP_LEVEL)
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected top-level fields: {', '.join(extra)}")

    if payload.get("schema") != SCHEMA:
        errors.append(f"schema must equal {SCHEMA}")

    role = payload.get("role_identity")
    if not isinstance(role, dict):
        errors.append("role_identity must be an object")
    else:
        if set(role) != {"label", "numerical_identity"}:
            errors.append("role_identity must contain exactly label and numerical_identity")
        if role.get("label") != ROLE_LABEL:
            errors.append(f"role_identity.label must equal {ROLE_LABEL}")
        if role.get("numerical_identity") != NUMERICAL_IDENTITY:
            errors.append(f"role_identity.numerical_identity must equal {NUMERICAL_IDENTITY}")

    training = payload.get("training")
    if not isinstance(training, dict):
        errors.append("training must be an object")
    else:
        allowed = {"package_id", "version", "manifest_sha256", "source_commit_or_digest"}
        if set(training) != allowed:
            errors.append("training must contain exactly package_id, version, manifest_sha256, source_commit_or_digest")
        if training.get("package_id") != PACKAGE_ID:
            errors.append(f"training.package_id must equal {PACKAGE_ID}")
        if training.get("version") != PACKAGE_VERSION:
            errors.append(f"training.version must equal {PACKAGE_VERSION}")
        manifest = training.get("manifest_sha256")
        if manifest != MANIFEST_SHA256 or not isinstance(manifest, str) or not HEX64.fullmatch(manifest):
            errors.append("training.manifest_sha256 does not match Six v1.0.0")
        source = training.get("source_commit_or_digest")
        if source != SOURCE_SET_DIGEST:
            errors.append("training.source_commit_or_digest must equal the registered Six v1.0.0 source-set digest")

    list_fields = {
        "assignments",
        "immutable_subjects",
        "mutable_observations",
        "operator_evidence",
        "blockers",
        "authority_and_leases",
        "external_effects",
        "handoffs_and_escalations",
        "claim_ceilings",
        "do_not_rerun",
        "evidence_pointers",
        "unknowns",
    }
    for key in sorted(list_fields):
        if key in payload and not isinstance(payload[key], list):
            errors.append(f"{key} must be list")

    for key in ("current_governance", "foreground", "target_runtime"):
        if key in payload and not isinstance(payload[key], dict):
            errors.append(f"{key} must be object")

    return errors


def load_payload(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["verify", "digest", "canonicalize"])
    parser.add_argument("payload", type=Path)
    args = parser.parse_args(argv)

    try:
        payload = load_payload(args.payload)
    except Exception as exc:
        print(json.dumps({"valid": False, "errors": [f"cannot load JSON: {exc}"]}, sort_keys=True))
        return 2

    errors = validate(payload)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, sort_keys=True))
        return 2

    text = canonical_text(payload)
    digest = digest_text(text)
    if args.command == "canonicalize":
        print(text)
    elif args.command == "digest":
        print(digest)
    else:
        print(json.dumps({"valid": True, "checkpoint_sha256": digest, "canonical_payload_text": text}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
