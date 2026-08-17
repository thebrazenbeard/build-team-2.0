#!/usr/bin/env python3
"""Mechanical checkpoint/BASE_READY receipt validation for BT2 Four training.

No network access. No external writes. No authority decisions. The declarative JSON
schemas are the portable contract; this helper performs semantic checks that are
awkward to express in JSON Schema alone.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MIDS = [f"M{i:02d}" for i in range(1, 10)]
CURRENTNESS = "CHECKPOINT_IS_RECOVERY_EVIDENCE_NOT_CURRENT_AUTHORITY"
CONTINUITY = "NO_UNINTERRUPTED_RUNTIME_OR_SUBJECTIVE_CONTINUITY_CLAIM"

class ValidationError(ValueError): pass

def need(cond: bool, msg: str) -> None:
    if not cond: raise ValidationError(msg)

def load(path: str):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def keys(obj, required, allowed, where):
    need(isinstance(obj, dict), f"{where}: expected object")
    miss = [k for k in required if k not in obj]
    extra = [k for k in obj if k not in allowed]
    need(not miss, f"{where}: missing keys {miss}")
    need(not extra, f"{where}: unknown keys {extra}")

def text(v, where): need(isinstance(v, str) and bool(v.strip()), f"{where}: non-empty string required")
def arr(v, where): need(isinstance(v, list), f"{where}: array required")

def validate_operational(d):
    required = ["schema","role_id","checkpoint_id","observed_at","provenance_boundary","training_base","governance","coordination","assignments","dependencies","blockers","repositories","authority","terminal_work","corrections_supersessions","next_safe_action","prohibited_effects","unresolved_evidence","currentness_rule","continuity_ceiling"]
    keys(d, required, required, "checkpoint")
    need(d["schema"] == "BT2_FOUR_OPERATIONAL_CHECKPOINT_V1", "checkpoint.schema")
    need(d["role_id"] == "Four", "checkpoint.role_id")
    text(d["checkpoint_id"], "checkpoint.checkpoint_id"); text(d["observed_at"], "checkpoint.observed_at")
    keys(d["provenance_boundary"], ["statement"], ["statement"], "provenance_boundary"); text(d["provenance_boundary"]["statement"], "provenance_boundary.statement")
    tb = d["training_base"]; ks=["version","repository","source_commit","manifest_path","manifest_sha256"]; keys(tb, ks, ks, "training_base")
    for k in ["version","repository","manifest_path"]: text(tb[k], f"training_base.{k}")
    need(bool(HEX40.fullmatch(tb["source_commit"])), "training_base.source_commit: 40 lowercase hex required")
    need(bool(HEX64.fullmatch(tb["manifest_sha256"])), "training_base.manifest_sha256: 64 lowercase hex required")
    keys(d["governance"], ["locator","observed_revision"], ["locator","observed_revision"], "governance"); text(d["governance"]["locator"], "governance.locator")
    keys(d["coordination"], ["last_consumed_sequence","sources_checked"], ["last_consumed_sequence","sources_checked"], "coordination"); arr(d["coordination"]["sources_checked"], "coordination.sources_checked")
    arr(d["assignments"], "assignments")
    for i,a in enumerate(d["assignments"]):
        ks=["id","scope","status","source_locator"]; keys(a,ks,ks,f"assignments[{i}]")
        for k in ks: text(a[k], f"assignments[{i}].{k}")
    for k in ["dependencies","blockers","repositories","terminal_work","corrections_supersessions","unresolved_evidence"]: arr(d[k], k)
    for i,r in enumerate(d["repositories"]):
        ks=["repository","ref","observed_head","tree","observed_at"]; keys(r,ks,ks,f"repositories[{i}]")
        text(r["repository"],f"repositories[{i}].repository"); text(r["ref"],f"repositories[{i}].ref"); text(r["observed_at"],f"repositories[{i}].observed_at")
        need(bool(HEX40.fullmatch(r["observed_head"])), f"repositories[{i}].observed_head")
        need(bool(HEX40.fullmatch(r["tree"])), f"repositories[{i}].tree")
    auth=d["authority"]; aks=["leases","explicit_absences","direct_user_authorizations"]; keys(auth,aks,aks,"authority")
    for k in aks: arr(auth[k], f"authority.{k}")
    need(sum(len(auth[k]) for k in aks) > 0, "authority: state must be explicit; record a lease, absence, or direct authorization")
    text(d["next_safe_action"], "next_safe_action"); arr(d["prohibited_effects"], "prohibited_effects"); need(len(d["prohibited_effects"])>0, "prohibited_effects: at least one required")
    need(d["currentness_rule"] == CURRENTNESS, "currentness_rule")
    need(d["continuity_ceiling"] == CONTINUITY, "continuity_ceiling")
    return True

def validate_base(d):
    required=["schema","role_id","qualified_at","training_source","manifest_sha256","package_content_sha256","module_results","concrete_evidence_subjects","automatic_disqualifiers","final_qualification","base_ready","continuity_ceiling"]
    keys(d,required,required,"receipt")
    need(d["schema"]=="BT2_FOUR_BASE_READY_RECEIPT_V1","receipt.schema"); need(d["role_id"]=="Four","receipt.role_id"); text(d["qualified_at"],"qualified_at")
    ts=d["training_source"]; ks=["repository","source_commit","manifest_path","version"]; keys(ts,ks,ks,"training_source")
    for k in ["repository","manifest_path","version"]: text(ts[k],f"training_source.{k}")
    need(bool(HEX40.fullmatch(ts["source_commit"])),"training_source.source_commit")
    need(bool(HEX64.fullmatch(d["manifest_sha256"])),"manifest_sha256"); need(bool(HEX64.fullmatch(d["package_content_sha256"])),"package_content_sha256")
    arr(d["module_results"],"module_results"); need(len(d["module_results"])==9,"module_results: exactly nine results required")
    seen=[]
    for i,m in enumerate(d["module_results"]):
        ks=["id","result","evidence_summary"]; keys(m,ks,ks,f"module_results[{i}]"); seen.append(m["id"])
        need(m["result"]=="PASS",f"module_results[{i}]: all modules must PASS"); text(m["evidence_summary"],f"module_results[{i}].evidence_summary")
    need(seen==MIDS,f"module_results: exact ordered ids required {MIDS}")
    arr(d["concrete_evidence_subjects"],"concrete_evidence_subjects"); need(len(d["concrete_evidence_subjects"])>0,"concrete_evidence_subjects: at least one required")
    arr(d["automatic_disqualifiers"],"automatic_disqualifiers"); need(len(d["automatic_disqualifiers"])==0,"automatic_disqualifiers must be empty")
    fq=d["final_qualification"]; keys(fq,["result","rationale"],["result","rationale"],"final_qualification"); need(fq["result"]=="QUALIFIED","final_qualification.result"); text(fq["rationale"],"final_qualification.rationale")
    need(d["base_ready"] is True,"base_ready must be true"); need(d["continuity_ceiling"]==CONTINUITY,"continuity_ceiling")
    return True

def operational_template():
    return {"schema":"BT2_FOUR_OPERATIONAL_CHECKPOINT_V1","role_id":"Four","checkpoint_id":"REPLACE","observed_at":"REPLACE","provenance_boundary":{"statement":"Recovery evidence only; refresh mutable state before acting."},"training_base":{"version":"REPLACE","repository":"REPLACE","source_commit":"0"*40,"manifest_path":"REPLACE","manifest_sha256":"0"*64},"governance":{"locator":"REPLACE","observed_revision":"REPLACE"},"coordination":{"last_consumed_sequence":None,"sources_checked":[]},"assignments":[],"dependencies":[],"blockers":[],"repositories":[],"authority":{"leases":[],"explicit_absences":["REPLACE with explicit current authority state"],"direct_user_authorizations":[]},"terminal_work":[],"corrections_supersessions":[],"next_safe_action":"REPLACE","prohibited_effects":["No external mutation without current exact authority."],"unresolved_evidence":[],"currentness_rule":CURRENTNESS,"continuity_ceiling":CONTINUITY}

def base_template():
    return {"schema":"BT2_FOUR_BASE_READY_RECEIPT_V1","role_id":"Four","qualified_at":"REPLACE","training_source":{"repository":"REPLACE","source_commit":"0"*40,"manifest_path":"REPLACE","version":"REPLACE"},"manifest_sha256":"0"*64,"package_content_sha256":"0"*64,"module_results":[{"id":m,"result":"PASS","evidence_summary":"REPLACE"} for m in MIDS],"concrete_evidence_subjects":["REPLACE"],"automatic_disqualifiers":[],"final_qualification":{"result":"QUALIFIED","rationale":"REPLACE"},"base_ready":True,"continuity_ceiling":CONTINUITY}

def main(argv=None):
    p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="cmd",required=True)
    for name in ["validate-operational","validate-base-receipt"]:
        s=sp.add_parser(name); s.add_argument("path")
    sp.add_parser("emit-operational-template"); sp.add_parser("emit-base-template")
    a=p.parse_args(argv)
    try:
        if a.cmd=="validate-operational": validate_operational(load(a.path)); print("VALID_OPERATIONAL_CHECKPOINT")
        elif a.cmd=="validate-base-receipt": validate_base(load(a.path)); print("VALID_BASE_READY_RECEIPT")
        elif a.cmd=="emit-operational-template": print(json.dumps(operational_template(),indent=2,sort_keys=True))
        elif a.cmd=="emit-base-template": print(json.dumps(base_template(),indent=2,sort_keys=True))
    except (OSError,json.JSONDecodeError,ValidationError) as e:
        print(f"INVALID: {e}",file=sys.stderr); return 2
    return 0

if __name__=="__main__": raise SystemExit(main())
