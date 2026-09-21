from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "training" / "ROLE_TRAINING_REGISTRY.json"

OVERLAY_PATHS = (
    "docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md",
    "training/PROTOCOL_V2_REGRESSION_SUITE.md",
)

STARTUP_PATHS = (
    "training/FRESH_CHAT_STARTUP.md",
    "training/FIVE_FRESH_CHAT_STARTUP.md",
    "training/SIX_FRESH_CHAT_STARTUP.md",
    "training/NINE_FRESH_CHAT_STARTUP.md",
)


class ProtocolV2GovernanceOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        self.overlay = self.registry["current_governance_overlay"]

    def test_registry_requires_current_overlay_before_work(self):
        self.assertTrue(self.overlay["required"])
        self.assertEqual(
            self.overlay["stage"],
            "AFTER_BASE_READY_AND_CHECKPOINT_RESOLUTION_BEFORE_OPERATIONAL_WORK",
        )
        self.assertEqual(self.overlay["authoritative_ref"], "main")
        self.assertEqual(self.overlay["precedence_path"], OVERLAY_PATHS[0])
        self.assertEqual(self.overlay["regression_path"], OVERLAY_PATHS[1])
        self.assertEqual(
            self.overlay["failure_disposition"],
            "CURRENT_GOVERNANCE_OVERLAY_UNRESOLVED",
        )

    def test_overlay_preserves_effect_boundary(self):
        semantics = set(self.overlay["semantics"])
        self.assertIn(
            "IMMUTABLE_ROLE_TRAINING_IS_COMPETENCE_SOURCE_NOT_CURRENT_GOVERNANCE",
            semantics,
        )
        self.assertIn(
            "CURRENT_OVERLAY_OVERRIDES_CONFLICTING_STALE_PERMISSION_OR_LEASE_FOLKLORE",
            semantics,
        )
        self.assertIn("OVERLAY_DOES_NOT_GRANT_PROTECTED_EFFECT_AUTHORITY", semantics)

    def test_every_effective_startup_route_loads_same_overlay(self):
        for relative in STARTUP_PATHS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                for overlay_path in OVERLAY_PATHS:
                    self.assertIn(overlay_path, text)
                self.assertIn("current-governance overlay", text.lower())
                self.assertIn("before operational work", text.lower())

    def test_generic_startup_orders_overlay_before_work(self):
        text = (ROOT / "training" / "FRESH_CHAT_STARTUP.md").read_text(
            encoding="utf-8"
        )
        chain = (
            "VERSIONED TRAINING SOURCE -> QUALIFIED FROZEN BASE -> "
            "VERIFIED OPERATIONAL CHECKPOINT -> CURRENT GOVERNANCE OVERLAY -> "
            "FRESH CURRENTNESS REFRESH -> WORK"
        )
        self.assertIn(chain, text)

    def test_registered_roles_cannot_opt_out_of_overlay(self):
        self.assertGreater(len(self.registry["roles"]), 0)
        for role_key, role in self.registry["roles"].items():
            with self.subTest(role=role_key):
                self.assertIn("fresh_chat_rule", role)
                self.assertIn("working_branch_rule", role)
                self.assertNotIn("current_governance_overlay", role)


if __name__ == "__main__":
    unittest.main()
