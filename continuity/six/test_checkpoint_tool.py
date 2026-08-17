#!/usr/bin/env python3
import importlib.util
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("six_checkpoint_tool", HERE / "checkpoint_tool.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)

def valid_payload():
    return {
        "schema":"SIX_OPERATIONAL_RESUME_CHECKPOINT_V1",
        "role_key":"six",
        "numerical_identity":6,
        "training_binding":{
            "version":"1.0.0",
            "source_set_digest_sha256":"ef44176582819750193c7d591e9ee449ea8c3d6743a8bff3eb5228baf4fad1cc",
            "qualification_id":None,
        },
        "governance_observation":{},
        "role_map_ref":"UNRESOLVED",
        "active_assignments":[],
        "operator_evidence":[],
        "target_runtime":{},
        "blockers":[],
        "service_warden_map":{},
        "write_authority_observations":[],
        "provider_objects":[],
        "verified_effects":[],
        "historical_constraints":[],
        "direct_addresses":[],
        "handoffs_and_escalations":[],
        "claim_ceilings":[],
        "do_not_rerun":[],
        "next_safe_frontier":"UNRESOLVED",
        "provenance":[],
        "unknowns":[],
    }

class CheckpointToolTests(unittest.TestCase):
    def test_valid_payload(self):
        self.assertEqual(MOD.validate(valid_payload()), [])
    def test_wrong_role_rejected(self):
        p = valid_payload()
        p["role_key"] = "nine"
        self.assertTrue(any("role_key" in e for e in MOD.validate(p)))
    def test_wrong_training_digest_rejected(self):
        p = valid_payload()
        p["training_binding"]["source_set_digest_sha256"] = "0" * 64
        self.assertTrue(any("source_set_digest" in e for e in MOD.validate(p)))
    def test_digest_is_deterministic(self):
        p = valid_payload()
        a = MOD.digest_text(MOD.canonical_text(p))
        b = MOD.digest_text(MOD.canonical_text(dict(reversed(list(p.items())))))
        self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()
