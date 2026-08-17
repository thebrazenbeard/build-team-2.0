#!/usr/bin/env python3
"""Deterministic helper for Thirteen operational checkpoint payloads.

This tool validates the role/training binding and emits the canonical compact JSON
text plus SHA-256 expected by the shared Supabase checkpoint store. It does not
write to any external service and does not grant authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "THIRTEEN_OPERATIONAL_CHECKPOINT_V1"
ROLE_KEY = "thirteen"
NUMERICAL_IDENTITY = 13
PACKAGE_VERSION = "1.0.0"
SOURCE_SET_DIGEST = "89f3da76b9033c9302e2ddb85c68b6bf0b7856383d7bce65f671170d4a8a7bc1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_TOP_LEVEL = {
    "schema",
    "role_key",
    "numerical_identity",
    "training_binding",
    "governance_observation",
    "role_map_ref",
    "active_assignments",
    "corrections_pipeline",
    "blockers",
    "service_warden_map",
    "write_authority_observations",
    "provider_objects",
    "verified_effects",
    "historical_constraints",
    "finding_families",
    "claim_ceilings",
    "next_safe_frontier",
    "provenance",
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
    if payload.get("role_key") != ROLE_KEY:
        errors.append(f"role_key must equal {ROLE_KEY}")
    if payload.get("numerical_identity") != NUMERICAL_IDENTITY:
        errors.append(f"numerical_identity must equal {NUMERICAL_IDENTITY}")

    binding = payload.get("training_binding")
    if not isinstance(binding, dict):
        errors.append("training_binding must be an object")
    else:
        allowed = {"version", "source_set_digest_sha256", "qualification_id"}
        if set(binding) != allowed:
            errors.append("training_binding must contain exactly version, source_set_digest_sha256, qualification_id")
        if binding.get("version") != PACKAGE_VERSION:
            errors.append(f"training_binding.version must equal {PACKAGE_VERSION}")
        digest = binding.get("source_set_digest_sha256")
        if digest != SOURCE_SET_DIGEST or not isinstance(digest, str) or not HEX64.fullmatch(digest):
            errors.append("training_binding.source_set_digest_sha256 does not match the registered v1.0.0 source set")
        qualification_id = binding.get("qualification_id")
        if qualification_id is not None and (isinstance(qualification_id, bool) or not isinstance(qualification_id, int) or qualification_id < 1):
            errors.append("training_binding.qualification_id must be null or a positive integer")

    typed = {
        "active_assignments": list,
        "corrections_pipeline": dict,
        "blockers": list,
        "service_warden_map": dict,
        "write_authority_observations": list,
        "provider_objects": list,
        "verified_effects": list,
        "historical_constraints": list,
        "finding_families": list,
        "claim_ceilings": list,
        "provenance": list,
    }
    for key, expected in typed.items():
        if key in payload and not isinstance(payload[key], expected):
            errors.append(f"{key} must be {expected.__name__}")
    if "governance_observation" in payload and not isinstance(payload["governance_observation"], dict):
        errors.append("governance_observation must be object")
    if "role_map_ref" in payload and not isinstance(payload["role_map_ref"], (str, dict)):
        errors.append("role_map_ref must be string or object")
    if "next_safe_frontier" in payload and not isinstance(payload["next_safe_frontier"], (str, dict)):
        errors.append("next_safe_frontier must be string or object")
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
        print(json.dumps({"valid": False, "errors": [f"cannot load JSON: {exc}"]}))
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
