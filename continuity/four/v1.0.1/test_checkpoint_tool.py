import json, subprocess, sys
from pathlib import Path

TOOL=Path(__file__).with_name("checkpoint_tool.py")
DIGEST="1070866d342043c21d06d9bc384fbf7cf78d231850ef2edef514b3e95229c332"
def payload():
    return {"schema":"FOUR_OPERATIONAL_CHECKPOINT_V1","role_key":"four","numerical_identity":4,"training_binding":{"version":"1.0.1","source_set_digest_sha256":DIGEST,"qualification_id":1},"governance_observation":{},"role_map_ref":"test","active_assignments":[],"exact_subjects":[],"package_state":{},"blockers":[],"write_authority_observations":[],"provider_objects":[],"verified_effects":[],"finding_families":[],"claim_ceilings":[],"next_safe_frontier":"none","provenance":[]}
def run(tmp_path,obj):
    p=tmp_path/"p.json"; p.write_text(json.dumps(obj),encoding="utf-8")
    return subprocess.run([sys.executable,str(TOOL),"verify",str(p)],capture_output=True,text=True)
def test_valid(tmp_path):
    r=run(tmp_path,payload()); assert r.returncode==0; assert json.loads(r.stdout)["valid"] is True
def test_wrong_role_fails(tmp_path):
    x=payload(); x["role_key"]="one"; assert run(tmp_path,x).returncode==2
def test_wrong_digest_fails(tmp_path):
    x=payload(); x["training_binding"]["source_set_digest_sha256"]="0"*64; assert run(tmp_path,x).returncode==2
def test_extra_field_fails(tmp_path):
    x=payload(); x["invented"]=True; assert run(tmp_path,x).returncode==2
