#!/usr/bin/env python3
import hashlib
import unittest

import checkpoint_tool as tool


def valid_payload():
    return {
        "schema": tool.SCHEMA,
        "training": {
            "package_id": tool.PACKAGE_ID,
            "version": tool.PACKAGE_VERSION,
            "manifest_sha256": tool.MANIFEST_SHA256,
            "source_commit_or_digest": tool.SOURCE_SET_DIGEST,
        },
        "role_identity": {"label": tool.ROLE_LABEL, "numerical_identity": tool.NUMERICAL_IDENTITY},
        "current_governance": {},
        "foreground": {},
        "assignments": [],
        "immutable_subjects": [],
        "mutable_observations": [],
        "reconstructions_current": [],
        "reconstructions_superseded": [],
        "blockers": [],
        "authority_and_leases": [],
        "external_effects": [],
        "handoffs_and_escalations": [],
        "claim_ceilings": [],
        "do_not_rerun": [],
        "evidence_pointers": [],
        "unknowns": [],
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
        payload["role_identity"]["label"] = "One"
        self.assertTrue(any("role_identity.label" in e for e in tool.validate(payload)))

    def test_wrong_digest_fails(self):
        payload = valid_payload()
        payload["training"]["source_commit_or_digest"] = "0" * 64
        self.assertTrue(any("source_commit_or_digest" in e for e in tool.validate(payload)))

    def test_wrong_manifest_fails(self):
        payload = valid_payload()
        payload["training"]["manifest_sha256"] = "0" * 64
        self.assertTrue(any("manifest_sha256" in e for e in tool.validate(payload)))

    def test_extra_field_fails(self):
        payload = valid_payload()
        payload["invented_authority"] = True
        self.assertTrue(any("unexpected top-level" in e for e in tool.validate(payload)))

    def test_wrong_field_type_fails(self):
        payload = valid_payload()
        payload["assignments"] = {}
        self.assertTrue(any("assignments" in e for e in tool.validate(payload)))


if __name__ == "__main__":
    unittest.main()
