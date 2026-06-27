#!/usr/bin/env python3
"""Unit tests for the baseline-metric separation in maincode.py.

Proves that the local weak-baseline LEAK RATE (305,985 / 360,000 = 85.0%) is
computed and labelled distinctly from the paper's negative-control FPR (6.4%),
and that a reconciliation warning fires when the two disagree.

Run:  python3 test_baseline_metrics.py        (or: python3 -m unittest -v test_baseline_metrics)
"""

import importlib.util
import os
import unittest

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maincode.py")
_spec = importlib.util.spec_from_file_location("maincodemod", _PATH)
trymod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(trymod)

LEAKED = 305_985
TOTAL = 360_000


class TestWeakBaselineLeakRate(unittest.TestCase):
    def test_internal_precision(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertAlmostEqual(m["weak_baseline_leak_rate_percent"], 84.99583333333334, places=9)

    def test_explicit_formula(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertEqual(
            m["weak_baseline_leak_rate_percent"], LEAKED / TOTAL * 100
        )

    def test_one_decimal_display(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertEqual(f"{m['weak_baseline_leak_rate_percent']:.1f}", "85.0")

    def test_named_count_fields(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertEqual(m["weak_baseline_leaked_count"], LEAKED)
        self.assertEqual(m["weak_baseline_total_count"], TOTAL)

    def test_zero_total_is_safe(self):
        m = trymod.compute_baseline_metrics(0, 0)
        self.assertEqual(m["weak_baseline_leak_rate_percent"], 0.0)


class TestPaperNegativeControlFPR(unittest.TestCase):
    def test_constant_unchanged(self):
        self.assertEqual(trymod.PAPER_NEGATIVE_CONTROL_FPR_PERCENT, 6.4)

    def test_carried_through_unchanged(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertEqual(m["negative_control_fpr_percent"], 6.4)

    def test_two_metrics_are_distinct(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        self.assertNotEqual(
            round(m["weak_baseline_leak_rate_percent"], 1),
            m["negative_control_fpr_percent"],
        )


class TestNotLabelledFPR(unittest.TestCase):
    def test_leak_rate_key_is_not_named_fpr(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        # The 85% value must live under a *leak_rate* key, and the only *fpr*
        # key must hold the paper's 6.4 value - never the 85% leak rate.
        self.assertIn("weak_baseline_leak_rate_percent", m)
        self.assertEqual(m["negative_control_fpr_percent"], 6.4)
        for k, val in m.items():
            if "fpr" in k.lower():
                self.assertNotAlmostEqual(val or 0.0, 85.0, places=1)

    def test_dashboard_template_labels_weak_value_as_leak_rate(self):
        tpl = trymod._DASHBOARD_TEMPLATE
        # Weak value is bound to the "Weak-baseline leak rate" label...
        self.assertIn("Weak-baseline leak rate", tpl)
        self.assertIn("weak_baseline_leak_rate_percent", tpl)
        # ...and the old mislabel that called the 85% an FPR is gone.
        self.assertNotIn("DATA.neg_fpr", tpl)
        self.assertNotIn('"Negative-control FPR"', tpl)

    def test_report_line_does_not_call_leak_rate_an_fpr(self):
        # Re-create the two Section-1 baseline lines exactly as main() builds them.
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)
        weak_line = (
            f"Weak-baseline run       : {m['weak_baseline_leaked_count']:,} / "
            f"{m['weak_baseline_total_count']:,} = "
            f"{m['weak_baseline_leak_rate_percent']:.1f}% leak rate (NOT an FPR)"
        )
        paper_line = f"Paper negative-control  : {m['negative_control_fpr_percent']}% FPR"
        self.assertIn("85.0% leak rate", weak_line)
        self.assertIn("NOT an FPR", weak_line)
        self.assertNotIn("FPR", weak_line.split("(NOT an FPR")[0])  # no FPR before the disclaimer
        self.assertIn("6.4% FPR", paper_line)


class TestReconciliationWarning(unittest.TestCase):
    def test_warning_present_when_both_present_and_far_apart(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL)  # 85.0% vs 6.4% -> 78.6pp gap
        self.assertIsNotNone(m["baseline_mismatch_warning"])
        self.assertIn("Baseline mismatch", m["baseline_mismatch_warning"])

    def test_no_warning_when_within_tolerance(self):
        # 23,040 / 360,000 = 6.4% leak rate, matches the paper FPR -> no warning.
        m = trymod.compute_baseline_metrics(23_040, TOTAL, negative_control_fpr_percent=6.4)
        self.assertEqual(f"{m['weak_baseline_leak_rate_percent']:.1f}", "6.4")
        self.assertIsNone(m["baseline_mismatch_warning"])

    def test_no_warning_when_paper_value_absent(self):
        m = trymod.compute_baseline_metrics(LEAKED, TOTAL, negative_control_fpr_percent=None)
        self.assertIsNone(m["baseline_mismatch_warning"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
