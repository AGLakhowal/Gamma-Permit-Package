#!/usr/bin/env python3
"""Tests that run Runtime Enforcement over a REAL, saved corpus file.

These prove the saved data is genuine (every record carries a live HMAC-SHA256
signature that is re-verified on load) and that enforcement behaves correctly on
the persisted file - not on in-memory ephemera.

Run:  python3 -m unittest -v test_corpus_enforcement
"""

import importlib.util
import os
import tempfile
import unittest

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maincode.py")
_spec = importlib.util.spec_from_file_location("maincodemod", _PATH)
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)


class TestSavedCorpusEnforcement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate and SAVE a real dataset to a temp file, then load it back.
        cls.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
        cls.tmp.close()
        cls.info = mc.save_corpus(cls.tmp.name, n_nominal=1400, n_adversarial=600)
        cls.records = list(mc.load_corpus(cls.tmp.name))
        cls.metrics = mc.run_enforcement_on_corpus(cls.records)

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.tmp.name)

    def test_file_round_trips(self):
        self.assertEqual(len(self.records), 2000)
        self.assertEqual(self.info["total"], 2000)

    def test_no_unauthorized_permits(self):
        self.assertEqual(self.metrics["unauthorized_permits"], 0)

    def test_no_false_denials(self):
        self.assertEqual(self.metrics["false_denials"], 0)

    def test_perfect_accuracy_and_pass(self):
        self.assertEqual(self.metrics["accuracy"], 1.0)
        self.assertEqual(self.metrics["verdict"], "COMPLIANT_PASS")

    def test_weak_baseline_leaks_but_node_breach_does_not(self):
        self.assertGreater(self.metrics["weak_baseline_leaked"], 0)
        # node_risk_breach is the family the weak baseline also catches -> never leaks.
        self.assertNotIn("node_risk_breach", self.metrics["per_family_leak"])

    def test_records_carry_real_verifiable_signatures(self):
        # Every NOMINAL token's stored signature must match a fresh HMAC re-sign.
        checked = 0
        for rec in self.records:
            if rec["category"] != "nominal":
                continue
            tok = rec["token"]
            expected = mc._sign(tok["top_id"], tok["scope"],
                                tok["issued_at"], tok["expires_at"], tok["nonce"])
            self.assertEqual(tok["signature"], expected, f"bad sig on id={rec['id']}")
            checked += 1
        self.assertGreater(checked, 0)

    def test_forged_family_signature_does_not_verify(self):
        # signature_substitution records must carry a signature that fails re-verify.
        forged = [r for r in self.records if r["family"] == "signature_substitution"]
        self.assertGreater(len(forged), 0, "expected some forged records in the draw")
        for rec in forged:
            tok = rec["token"]
            expected = mc._sign(tok["top_id"], tok["scope"],
                                tok["issued_at"], tok["expires_at"], tok["nonce"])
            self.assertNotEqual(tok["signature"], expected)

    def test_committed_corpus_if_present(self):
        # If a committed lab_corpus.jsonl exists, it must also pass enforcement.
        path = os.path.join(os.path.dirname(_PATH), "lab_corpus.jsonl")
        if not os.path.exists(path):
            self.skipTest("lab_corpus.jsonl not present")
        m = mc.run_enforcement_on_corpus(mc.load_corpus(path))
        self.assertEqual(m["unauthorized_permits"], 0)
        self.assertEqual(m["false_denials"], 0)
        self.assertEqual(m["verdict"], "COMPLIANT_PASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
