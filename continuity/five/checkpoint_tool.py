#!/usr/bin/env python3
"""Validate/canonicalize Five operational checkpoint payloads. No external writes."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

SCHEMA="FIVE_OPERATIONAL_RESUME_CHECKPOINT_V1"
ROLE_KEY="five"
NUMERICAL_IDENTITY=5
PACKAGE_VERSION="1.0.0"
SOURCE_SET_DIGEST="80d2aab944ee8c8e13b83ae99aacc4ba530bc42cda69ed6c9ab21958a64e55f8"
HEX64=re.compile(r"^[0-9a-f]{64}$")
REQUIRED={"schema","role_key","numerical_identity","training_binding","governance_observation","role_map_ref","active_assignments","source_registry_state","artifact_registry_state","custody_subjects","blockers","service_warden_map","write_authority_observations","provider_objects","verified_effects","finding_families","claim_ceilings","direct_addresses","handoffs_and_escalations","do_not_rerun","next_safe_frontier","provenance","unknowns"}

def canonical_text(payload: dict[str,Any])->str:
    return json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest_text(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
def validate(payload:Any)->list[str]:
    errors=[]
    if not isinstance(payload,dict): return ["payload must be a JSON object"]
    missing=sorted(REQUIRED-payload.keys()); extra=sorted(payload.keys()-REQUIRED)
    if missing: errors.append("missing top-level fields: "+", ".join(missing))
    if extra: errors.append("unexpected top-level fields: "+", ".join(extra))
    if payload.get("schema")!=SCHEMA: errors.append(f"schema must equal {SCHEMA}")
    if payload.get("role_key")!=ROLE_KEY: errors.append(f"role_key must equal {ROLE_KEY}")
    if payload.get("numerical_identity")!=NUMERICAL_IDENTITY: errors.append("numerical_identity must equal 5")
    b=payload.get("training_binding")
    if not isinstance(b,dict): errors.append("training_binding must be an object")
    else:
        if set(b)!={"version","source_set_digest_sha256","qualification_id"}: errors.append("training_binding must contain exactly version, source_set_digest_sha256, qualification_id")
        if b.get("version")!=PACKAGE_VERSION: errors.append("training_binding.version mismatch")
        d=b.get("source_set_digest_sha256")
        if d!=SOURCE_SET_DIGEST or not isinstance(d,str) or not HEX64.fullmatch(d): errors.append("training_binding.source_set_digest_sha256 mismatch")
        q=b.get("qualification_id")
        if q is not None and (isinstance(q,bool) or not isinstance(q,int) or q<1): errors.append("training_binding.qualification_id must be null or positive integer")
    object_fields={"governance_observation","source_registry_state","artifact_registry_state","service_warden_map"}
    array_fields={"active_assignments","custody_subjects","blockers","write_authority_observations","provider_objects","verified_effects","finding_families","claim_ceilings","direct_addresses","handoffs_and_escalations","do_not_rerun","provenance","unknowns"}
    for k in object_fields:
        if k in payload and not isinstance(payload[k],dict): errors.append(f"{k} must be dict")
    for k in array_fields:
        if k in payload and not isinstance(payload[k],list): errors.append(f"{k} must be list")
    if "role_map_ref" in payload and not isinstance(payload["role_map_ref"],(str,dict)): errors.append("role_map_ref must be string or object")
    if "next_safe_frontier" in payload and not isinstance(payload["next_safe_frontier"],(str,dict)): errors.append("next_safe_frontier must be string or object")
    return errors

def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["verify","digest","canonicalize"]); p.add_argument("payload",type=Path); a=p.parse_args(argv)
    try: payload=json.loads(a.payload.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"valid":False,"errors":[f"cannot load JSON: {exc}"]})); return 2
    e=validate(payload)
    if e: print(json.dumps({"valid":False,"errors":e},sort_keys=True)); return 2
    text=canonical_text(payload); digest=digest_text(text)
    if a.command=="canonicalize": print(text)
    elif a.command=="digest": print(digest)
    else: print(json.dumps({"valid":True,"checkpoint_sha256":digest,"canonical_payload_text":text},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
