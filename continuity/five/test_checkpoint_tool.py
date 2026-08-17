#!/usr/bin/env python3
import importlib.util
import pathlib
import unittest

HERE=pathlib.Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("five_checkpoint_tool", HERE / "checkpoint_tool.py")
MOD=importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)

def valid_payload():
    return {
        "schema":"FIVE_OPERATIONAL_RESUME_CHECKPOINT_V1",
        "role_key":"five",
        "numerical_identity":5,
        "training_binding":{"version":"1.0.0","source_set_digest_sha256":"80d2aab944ee8c8e13b83ae99aacc4ba530bc42cda69ed6c9ab21958a64e55f8","qualification_id":None},
        "governance_observation":{}, "role_map_ref":"UNRESOLVED", "active_assignments":[],
        "source_registry_state":{}, "artifact_registry_state":{}, "custody_subjects":[], "blockers":[],
        "service_warden_map":{}, "write_authority_observations":[], "provider_objects":[], "verified_effects":[],
        "finding_families":[], "claim_ceilings":[], "direct_addresses":[], "handoffs_and_escalations":[],
        "do_not_rerun":[], "next_safe_frontier":"UNRESOLVED", "provenance":[], "unknowns":[]
    }

class CheckpointToolTests(unittest.TestCase):
    def test_valid_payload(self): self.assertEqual(MOD.validate(valid_payload()), [])
    def test_wrong_role_rejected(self):
        p=valid_payload(); p["role_key"]="four"; self.assertTrue(any("role_key" in e for e in MOD.validate(p)))
    def test_wrong_digest_rejected(self):
        p=valid_payload(); p["training_binding"]["source_set_digest_sha256"]="0"*64; self.assertTrue(any("source_set_digest" in e for e in MOD.validate(p)))
    def test_extra_field_rejected(self):
        p=valid_payload(); p["surprise"]=1; self.assertTrue(any("unexpected" in e for e in MOD.validate(p)))
    def test_digest_deterministic(self):
        p=valid_payload(); self.assertEqual(MOD.digest_text(MOD.canonical_text(p)), MOD.digest_text(MOD.canonical_text(dict(reversed(list(p.items()))))))

if __name__=="__main__": unittest.main()
