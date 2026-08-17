#!/usr/bin/env python3
"""Optional Masa training/checkpoint helper. Repository presence does not execute this code."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROLE="MASA"
VERSION="1.0.0"
REQUIRED_CP={"schema","role","training_source","operational_reorientation","assignments","exact_subjects","provider_observations","leases","findings","dependencies","handoffs","claim_ledger","continuity_claim"}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fail(msg): print("FAIL: "+msg,file=sys.stderr); return 2

def verify_package(d):
    mp=d/"manifest.json"; sp=d/"SHA256SUMS"
    if not mp.is_file() or not sp.is_file(): return fail("manifest.json or SHA256SUMS missing")
    try: m=json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e: return fail(f"manifest parse failed: {e}")
    p=m.get("package",{})
    if p.get("role_key")!=ROLE or p.get("training_version")!=VERSION: return fail("role/version mismatch")
    mods=m.get("modules",[])
    if [x.get("id") for x in mods] != [f"M{i:02d}" for i in range(1,10)]: return fail("module ids/order invalid")
    if [x.get("order") for x in mods] != list(range(1,10)): return fail("module order invalid")
    for x in mods:
        if not (d/x["path"]).is_file(): return fail("missing module "+x["path"])
    n=0
    for line in sp.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try: expected, rel=line.split("  ",1)
        except ValueError: return fail("bad SHA256SUMS line")
        t=d/rel
        if not t.is_file() or digest(t)!=expected: return fail("checksum mismatch "+rel)
        n+=1
    if n<14: return fail("checksum coverage unexpectedly small")
    print(json.dumps({"status":"TRAINING_PACKAGE_VERIFIED","role":ROLE,"training_version":VERSION,"manifest_sha256":digest(mp),"checksum_entries_verified":n,"modules_verified":len(mods)},sort_keys=True)); return 0

def skeleton(manifest_sha):
    return {"schema":"BT2_MASA_OPERATIONAL_CHECKPOINT_V1","role":ROLE,"training_source":{"training_version":VERSION,"manifest_sha256":manifest_sha,"base_status":"BASE_READY_REQUIRED"},"operational_reorientation":{"working_laws_revision":None,"role_map_event":None,"active_roster":[],"coordination_high_water":None,"observed_at":None},"assignments":[],"exact_subjects":[],"provider_observations":[],"leases":[],"findings":[],"dependencies":[],"handoffs":[],"claim_ledger":[],"continuity_claim":"OPERATIONAL_RESUME_ONLY_NOT_UNINTERRUPTED_RUNTIME_OR_SUBJECTIVE_CONTINUITY"}

def new_checkpoint(manifest,out):
    try: m=json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as e: return fail(f"manifest parse failed: {e}")
    p=m.get("package",{})
    if p.get("role_key")!=ROLE or p.get("training_version")!=VERSION: return fail("manifest role/version mismatch")
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(skeleton(digest(manifest)),indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"CHECKPOINT_TEMPLATE_CREATED","path":str(out)},sort_keys=True)); return 0

def validate_checkpoint(p):
    try: c=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e: return fail(f"checkpoint parse failed: {e}")
    miss=sorted(REQUIRED_CP-set(c))
    if miss: return fail("missing keys "+",".join(miss))
    if c.get("schema")!="BT2_MASA_OPERATIONAL_CHECKPOINT_V1" or c.get("role")!=ROLE: return fail("checkpoint identity mismatch")
    if c.get("training_source",{}).get("training_version")!=VERSION: return fail("training version mismatch")
    if c.get("continuity_claim")!="OPERATIONAL_RESUME_ONLY_NOT_UNINTERRUPTED_RUNTIME_OR_SUBJECTIVE_CONTINUITY": return fail("continuity claim invalid")
    for x in c.get("claim_ledger",[]):
        if x.get("class") not in {"OBSERVED","INFERRED","HISTORICAL","UNKNOWN"}: return fail("invalid claim class")
    print(json.dumps({"status":"CHECKPOINT_STRUCTURALLY_VALID","path":str(p)},sort_keys=True)); return 0

def main():
    ap=argparse.ArgumentParser(); s=ap.add_subparsers(dest="cmd",required=True)
    p=s.add_parser("verify-package"); p.add_argument("package_dir",type=Path)
    p=s.add_parser("new-checkpoint"); p.add_argument("--manifest",type=Path,required=True); p.add_argument("--output",type=Path,required=True)
    p=s.add_parser("validate-checkpoint"); p.add_argument("checkpoint",type=Path)
    a=ap.parse_args()
    if a.cmd=="verify-package": return verify_package(a.package_dir)
    if a.cmd=="new-checkpoint": return new_checkpoint(a.manifest,a.output)
    return validate_checkpoint(a.checkpoint)

if __name__=="__main__": raise SystemExit(main())
