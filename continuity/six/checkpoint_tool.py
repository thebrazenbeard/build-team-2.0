#!/usr/bin/env python3
"""Deterministic helper for Six operational checkpoint payloads.

Validates the live shared-store envelope plus Six's v1.0.0 training binding, then
emits canonical compact JSON text and its SHA-256. It performs no external write
and grants no authority.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

SCHEMA = "SIX_OPERATIONAL_RESUME_CHECKPOINT_V1"
ROLE_KEY = "six"
NUMERICAL_IDENTITY = 6
PACKAGE_VERSION = "1.0.0"
SOURCE_SET_DIGEST = "ef44176582819750193c7d591e9ee449ea8c3d6743a8bff3eb5228baf4fad1cc"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_TOP_LEVEL = {
    "schema","role_key","numerical_identity","training_binding",
    "governance_observation","role_map_ref","active_assignments",
    "operator_evidence","target_runtime","blockers","service_warden_map",
    "write_authority_observations","provider_objects","verified_effects",
    "historical_constraints","direct_addresses","handoffs_and_escalations",
    "claim_ceilings","do_not_rerun","next_safe_frontier","provenance","unknowns",
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
        allowed = {"version","source_set_digest_sha256","qualification_id"}
        if set(binding) != allowed:
            errors.append("training_binding must contain exactly version, source_set_digest_sha256, qualification_id")
        if binding.get("version") != PACKAGE_VERSION:
            errors.append(f"training_binding.version must equal {PACKAGE_VERSION}")
        digest = binding.get("source_set_digest_sha256")
        if digest != SOURCE_SET_DIGEST or not isinstance(digest, str) or not HEX64.fullmatch(digest):
            errors.append("training_binding.source_set_digest_sha256 does not match registered Six v1.0.0")
        qid = binding.get("qualification_id")
        if qid is not None and (isinstance(qid, bool) or not isinstance(qid, int) or qid < 1):
            errors.append("training_binding.qualification_id must be null or a positive integer")

    list_fields = {
        "active_assignments","operator_evidence","blockers",
        "write_authority_observations","provider_objects","verified_effects",
        "historical_constraints","direct_addresses","handoffs_and_escalations",
        "claim_ceilings","do_not_rerun","provenance","unknowns",
    }
    for key in sorted(list_fields):
        if key in payload and not isinstance(payload[key], list):
            errors.append(f"{key} must be list")
    for key in ("governance_observation","target_runtime","service_warden_map"):
        if key in payload and not isinstance(payload[key], dict):
            errors.append(f"{key} must be object")
    for key in ("role_map_ref","next_safe_frontier"):
        if key in payload and not isinstance(payload[key], (str, dict)):
            errors.append(f"{key} must be string or object")
    return errors

def load_payload(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["verify","digest","canonicalize"])
    parser.add_argument("payload", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = load_payload(args.payload)
    except Exception as exc:
        print(json.dumps({"valid":False,"errors":[f"cannot load JSON: {exc}"]}, sort_keys=True))
        return 2
    errors = validate(payload)
    if errors:
        print(json.dumps({"valid":False,"errors":errors}, sort_keys=True))
        return 2
    text = canonical_text(payload)
    digest = digest_text(text)
    if args.command == "canonicalize":
        print(text)
    elif args.command == "digest":
        print(digest)
    else:
        print(json.dumps({"valid":True,"checkpoint_sha256":digest,"canonical_payload_text":text}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
