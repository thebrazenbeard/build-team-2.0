#!/usr/bin/env python3
import hashlib
import unittest

import checkpoint_tool as tool


def valid_payload():
    return {
        "schema": tool.SCHEMA,
        "role_key": tool.ROLE_KEY,
        "numerical_identity": tool.NUMERICAL_IDENTITY,
        "training_binding": {
            "version": tool.PACKAGE_VERSION,
            "source_set_digest_sha256": tool.SOURCE_SET_DIGEST,
            "qualification_id": None,
        },
        "governance_observation": {},
        "role_map_ref": {},
        "active_assignments": [],
        "corrections_pipeline": {},
        "blockers": [],
        "service_warden_map": {},
        "write_authority_observations": [],
        "provider_objects": [],
        "verified_effects": [],
        "historical_constraints": [],
        "finding_families": [],
        "claim_ceilings": [],
        "next_safe_frontier": "refresh currentness before work",
        "provenance": [],
    }


class CheckpointToolTests(unittest.TestCase):
    def test_valid_payload_passes(self):
        self.assertEqual([], tool.validate(valid_payload()))

    def test_canonical_digest_is_deterministic(self):
        payload = valid_payload()
        a = tool.canonical_text(payload)
        b = tool.canonical_text(dict(reversed(list(payload.items()))))
        self.assertEqual(a, b)
        self.assertEqual(tool.digest_text(a), hashlib.sha256(a.encode("utf-8")).hexdigest())

    def test_wrong_role_fails(self):
        payload = valid_payload()
        payload["role_key"] = "one"
        self.assertTrue(any("role_key" in e for e in tool.validate(payload)))

    def test_wrong_digest_fails(self):
        payload = valid_payload()
        payload["training_binding"]["source_set_digest_sha256"] = "0" * 64
        self.assertTrue(any("source_set_digest_sha256" in e for e in tool.validate(payload)))

    def test_extra_field_fails(self):
        payload = valid_payload()
        payload["invented_authority"] = True
        self.assertTrue(any("unexpected top-level" in e for e in tool.validate(payload)))

    def test_boolean_qualification_id_fails(self):
        payload = valid_payload()
        payload["training_binding"]["qualification_id"] = True
        self.assertTrue(any("qualification_id" in e for e in tool.validate(payload)))


if __name__ == "__main__":
    unittest.main()
