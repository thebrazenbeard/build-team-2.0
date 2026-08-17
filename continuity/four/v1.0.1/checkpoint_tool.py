#!/usr/bin/env python3
"""Validate/canonicalize Four operational checkpoint payloads. No external writes."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

SCHEMA="FOUR_OPERATIONAL_CHECKPOINT_V1"
ROLE_KEY="four"
NUMERICAL_IDENTITY=4
PACKAGE_VERSION="1.0.1"
SOURCE_SET_DIGEST="1070866d342043c21d06d9bc384fbf7cf78d231850ef2edef514b3e95229c332"
HEX64=re.compile(r"^[0-9a-f]{64}$")
REQUIRED={"schema","role_key","numerical_identity","training_binding","governance_observation","role_map_ref","active_assignments","exact_subjects","package_state","blockers","write_authority_observations","provider_objects","verified_effects","finding_families","claim_ceilings","next_safe_frontier","provenance"}

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
    if payload.get("numerical_identity")!=NUMERICAL_IDENTITY: errors.append("numerical_identity must equal 4")
    b=payload.get("training_binding")
    if not isinstance(b,dict): errors.append("training_binding must be an object")
    else:
        if set(b)!={"version","source_set_digest_sha256","qualification_id"}: errors.append("training_binding must contain exactly version, source_set_digest_sha256, qualification_id")
        if b.get("version")!=PACKAGE_VERSION: errors.append("training_binding.version mismatch")
        d=b.get("source_set_digest_sha256")
        if d!=SOURCE_SET_DIGEST or not isinstance(d,str) or not HEX64.fullmatch(d): errors.append("training_binding.source_set_digest_sha256 mismatch")
        q=b.get("qualification_id")
        if q is not None and (isinstance(q,bool) or not isinstance(q,int) or q<1): errors.append("training_binding.qualification_id must be null or positive integer")
    types={"governance_observation":dict,"active_assignments":list,"exact_subjects":list,"package_state":dict,"blockers":list,"write_authority_observations":list,"provider_objects":list,"verified_effects":list,"finding_families":list,"claim_ceilings":list,"provenance":list}
    for k,t in types.items():
        if k in payload and not isinstance(payload[k],t): errors.append(f"{k} must be {t.__name__}")
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
