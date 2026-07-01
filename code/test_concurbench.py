"""Conformance tests for the ConcurBench v1.0 evidence packet.

Validates that concurbench.build_concurbench_report(...) satisfies every
requirement in the Benchmark Verification Requirements (Document 1):
Levels 1-4 field presence + PASS thresholds, the standardized report envelope,
dataset block, contamination + canary, HITL governance, ASB event streams,
assumptions/limitations, independent-validation status, the Evidence Quad, the
section-17 thirty-item checklist, the section-18 top-level shape, and the
computed conformance verdict.

The report is built LIVE at a small scale so the tests exercise the real code,
not a cached file. A separate test also checks the committed full-scale
concurbench_report.json if present.
"""
import json
import os
import unittest

import concurbench as cb

_HERE = os.path.dirname(os.path.abspath(__file__))
_SMALL_ITEMS = 20_000


class TestConcurBenchConformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build a real report at reduced scale (structure/thresholds are
        # scale-invariant). Does not write concurbench_report.json.
        cls.r = cb.build_concurbench_report(_SMALL_ITEMS, cb.DEFAULT_SEED,
                                            "1970-01-01T00:00:00Z")

    # ----- Level 1 - authorization correctness (spec section 4) ----------- #
    def test_level1_fields_present(self):
        l1 = self.r["authorization_correctness"]
        for f in ("total_instances", "adversarial_subset_size", "true_permits",
                  "true_denials", "false_permits", "false_denials", "UER", "FPR",
                  "FDR", "FCR", "DR", "SVR", "confidence_interval_method",
                  "upper_bound_95"):
            self.assertIn(f, l1, f"Level 1 missing required field: {f}")

    def test_level1_confusion_matrix(self):
        cm = self.r["authorization_correctness"]["confusion_matrix"]
        for f in ("true_permits", "true_denials", "false_permits", "false_denials"):
            self.assertIn(f, cm)
        l1 = self.r["authorization_correctness"]
        # confusion matrix must be internally consistent
        self.assertEqual(cm["true_permits"] + cm["false_denials"]
                         + cm["true_denials"] + cm["false_permits"],
                         l1["total_instances"])

    def test_level1_pass_thresholds(self):
        l1 = self.r["authorization_correctness"]
        self.assertEqual(l1["false_permits"], 0)
        self.assertEqual(l1["UER"], 0.0)
        self.assertEqual(l1["FPR"], 0.0)
        self.assertEqual(l1["FCR"], 1.0)
        self.assertGreaterEqual(l1["DR"], 0.99999)
        self.assertGreater(l1["upper_bound_95"], 0.0)  # zero-event bound reported
        self.assertEqual(self.r["conformance_levels"]
                         ["level_1_authorization_correctness"], "PASS")

    # ----- Level 2 - adversarial robustness (spec section 5) -------------- #
    def test_level2_all_eight_attack_families(self):
        required = {"missing_predicate", "corrupted_input", "toctou", "replay_attack",
                    "payload_mutation", "concurrency_conflict",
                    "network_partition_or_delay", "adaptive_attacker"}
        fams = set(self.r["adversarial_robustness"]["attack_families"])
        self.assertTrue(required.issubset(fams),
                        f"missing families: {required - fams}")

    def test_level2_scenario_counts_and_adaptive(self):
        l2 = self.r["adversarial_robustness"]
        self.assertEqual(l2["adaptive_attacker_false_permits"], 0)
        self.assertIsNotNone(l2["adaptive_attacker_upper_bound_95"])
        self.assertTrue(l2["scenario_counts_by_family"])
        self.assertTrue(l2["synthetic_adversarial_tests_passed"])

    def test_level2_extended_families_zero_false_permits(self):
        ext = self.r["adversarial_robustness"]["extended_family_results"]
        self.assertEqual(ext["concurrency_conflict"]["false_permits"], 0)
        self.assertEqual(ext["network_partition_or_delay"]["false_permits"], 0)

    def test_level2_ablation_sensitivity(self):
        self.assertTrue(self.r["adversarial_robustness"]["ablation_shows_design_sensitivity"],
                        "ablations must show removing a control creates false permits")

    def test_level2_contamination_and_canary_present(self):
        l2 = self.r["adversarial_robustness"]
        self.assertIn(l2["contamination_check"], ("PASS", "FAIL", "NOT_RUN"))
        self.assertIn(l2["canary_string_check"], ("PASS", "FAIL", "NOT_RUN"))
        self.assertTrue(l2["asb_scenario_traces_included"])
        self.assertEqual(self.r["conformance_levels"]
                         ["level_2_adversarial_robustness"], "PASS")

    # ----- Level 3 - distributed consistency (spec section 6) ------------- #
    def test_level3_fields_and_pass(self):
        l3 = self.r["distributed_consistency"]
        for f in ("node_count", "testbed_type", "fleet_consistency",
                  "cross_node_replay_consistency", "policy_version_consistency",
                  "permit_state_consistency", "revocation_state_consistency",
                  "revocation_latency_p50_ms", "revocation_latency_p95_ms",
                  "revocation_latency_p99_ms", "partition_test", "clock_skew_bound_ms",
                  "quorum_rule", "node_failure_cases",
                  "distributed_desynchronization_cases"):
            self.assertIn(f, l3, f"Level 3 missing required field: {f}")
        self.assertGreaterEqual(l3["node_count"], 3)
        self.assertIn(l3["testbed_type"], ("simulated-fleet", "live-fleet"))
        self.assertEqual(l3["partition_test"], "PASS")
        self.assertEqual(l3["fleet_consistency"], 1.0)
        self.assertEqual(self.r["conformance_levels"]
                         ["level_3_distributed_consistency"], "PASS")

    def test_level3_is_labelled_simulated_not_live(self):
        # Honesty: never claim live-fleet.
        self.assertEqual(self.r["distributed_consistency"]["testbed_type"],
                         "simulated-fleet")

    # ----- Level 4 - replay + auditability (spec section 7) --------------- #
    def test_level4_replay_fields(self):
        l4 = self.r["replay_and_auditability"]
        for f in ("replay_attempts", "replay_passes", "replay_failures",
                  "replay_consistency_rate", "replay_verifier_version",
                  "replay_capsule_schema_version", "independent_replay_verifier",
                  "ertuple_count", "hash_chain_validation", "final_ledger_root_hash",
                  "audit_packet_export"):
            self.assertIn(f, l4, f"Level 4 missing required field: {f}")

    def test_level4_pass_thresholds(self):
        l4 = self.r["replay_and_auditability"]
        self.assertEqual(l4["replay_attempts"], self.r["authorization_correctness"]["total_instances"])
        self.assertEqual(l4["replay_failures"], 0)
        self.assertGreaterEqual(l4["replay_consistency_rate"], 0.99999)
        self.assertEqual(l4["hash_chain_validation"], "PASS")
        self.assertEqual(l4["audit_packet_export"], "PASS")
        self.assertIn(l4["independent_replay_verifier"], ("PASS", "FAIL", "NOT_RUN"))
        self.assertEqual(self.r["conformance_levels"]["level_4_replay_auditability"], "PASS")

    def test_evidence_quad_complete(self):
        quad = self.r["evidence_quad"]
        for f in ("spec_clause", "pre_reg_id", "method_version", "ledger_hash"):
            self.assertIn(f, quad)
            self.assertTrue(quad[f], f"Evidence Quad field empty: {f}")
        self.assertEqual(quad["method_version"], "LAB-v1.0")

    # ----- Report envelope + dataset (spec sections 8, 9) ----------------- #
    def test_report_envelope(self):
        env = self.r["benchmark_report"]
        for f in ("benchmark_version", "system_id", "evaluation_date", "evaluator",
                  "paper_source", "system_configuration_snapshot", "dataset_seed",
                  "predicate_schema_version", "token_schema_version",
                  "evaluation_protocol_version", "total_instances",
                  "adversarial_subset_size", "predicate_count", "scenario_distribution",
                  "contamination_test_outcome", "audit_verdict"):
            self.assertIn(f, env, f"envelope missing required field: {f}")
        self.assertEqual(env["benchmark_version"], "ConcurBench-v1.0")

    def test_dataset_block(self):
        d = self.r["dataset"]
        for f in ("generation_method", "dataset_seed", "dataset_generation_distribution",
                  "scenario_proportions", "predicate_dimensionality",
                  "adversarial_injection_rate", "monte_carlo_samples", "dataset_version",
                  "predicate_schema_version", "evaluation_protocol_version"):
            self.assertIn(f, d, f"dataset missing required field: {f}")

    # ----- Contamination (spec section 10) -------------------------------- #
    def test_contamination(self):
        c = self.r["contamination"]
        self.assertTrue(c["dynamic_generation"])
        self.assertEqual(c["static_dataset_exposure"], "NO")
        self.assertTrue(c["cryptographic_salting"])
        self.assertEqual(c["canary_string_validation"], "PASS")
        self.assertFalse(c["canary_leaked_into_ledger"])
        self.assertTrue(c["namespace_salt"])

    # ----- HITL governance (spec section 11) ------------------------------ #
    def test_human_governance(self):
        h = self.r["human_governance"]
        self.assertTrue(h["hitl_required_for_high_risk"])
        self.assertEqual(h["false_denial_dispute_workflow"], "defined")
        self.assertEqual(h["operator_query_path"], "defined")
        self.assertTrue(h["break_glass_protocol"])
        self.assertEqual(h["human_override_of_failed_predicate"], "PROHIBITED")
        self.assertEqual(len(h["denial_reason_categories"]), 5)

    # ----- ASB (spec section 12) ------------------------------------------ #
    def test_asb_families_and_metrics(self):
        a = self.r["asb"]
        required = {"identity_provenance_deception", "runtime_infrastructure_drift",
                    "economic_logic_fragility", "cross_entity_fraud_propagation",
                    "session_intent_compromise"}
        self.assertEqual(set(a["scenario_families"]), required)
        for f in ("event_stream_schema_version", "bounded_history_window",
                  "asb_pass_rate", "asb_unauthorized_execution_rate",
                  "asb_replay_consistency", "safe_state_transition_rate",
                  "predicate_failure_explanation_completeness"):
            self.assertIn(f, a)
        self.assertEqual(a["asb_unauthorized_execution_rate"], 0.0)

    def test_asb_event_schema(self):
        required_event_fields = {"event_id", "timestamp", "entity", "action",
                                 "resource", "provenance_score", "trust_score",
                                 "velocity_score", "infrastructure_integrity",
                                 "collateral_validity", "policy_context",
                                 "predicate_vector_G", "temporal_context",
                                 "system_decision", "ground_truth_authorization"}
        for scn in self.r["asb"]["scenarios"]:
            for ev in scn["events"]:
                self.assertTrue(required_event_fields.issubset(ev.keys()),
                                f"ASB event missing fields: {required_event_fields - set(ev)}")

    # ----- Assumptions + independent status (spec sections 13, 14) -------- #
    def test_assumptions_and_limitations(self):
        a = self.r["assumptions_and_limitations"]
        self.assertFalse(a["production_certification_claimed"])
        self.assertFalse(a["nist_or_ieee_approval_claimed"])
        self.assertTrue(a["semantic_correctness_not_measured"])
        self.assertIn("limitations_statement", a)

    def test_independent_benchmarks_disclosed(self):
        ib = self.r["independent_benchmarks"]
        for f in ("AgentDojo", "AgentHarm", "hardware_in_the_loop", "tla_plus_tlc",
                  "external_replay_verifier", "third_party_audit"):
            self.assertIn(f, ib, f"independent status missing: {f}")

    # ----- Verdict + top-level shape (spec sections 15, 18) --------------- #
    def test_overall_verdict_computed_compliant(self):
        self.assertEqual(self.r["overall_verdict"], "COMPLIANT_PASS")

    def test_section18_top_level_shape(self):
        for f in ("benchmark_report", "authorization_correctness",
                  "adversarial_robustness", "distributed_consistency",
                  "replay_and_auditability", "evidence_quad", "human_governance",
                  "asb", "contamination", "assumptions_and_limitations",
                  "independent_benchmarks", "conformance_levels", "overall_verdict"):
            self.assertIn(f, self.r, f"top-level object missing: {f}")

    # ----- Section 17 - thirty-item final checklist ----------------------- #
    def test_final_checklist_thirty_items(self):
        r = self.r
        env, l1, l4 = r["benchmark_report"], r["authorization_correctness"], r["replay_and_auditability"]
        checks = {
            "1 report envelope": bool(env),
            "2 UER": "UER" in l1, "3 SVR": "SVR" in l1, "4 FCR": "FCR" in l1,
            "5 FDR": "FDR" in l1, "6 DR": "DR" in l1,
            "7 replay_consistency_rate": "replay_consistency_rate" in l4,
            "8 confusion matrix": set(l1["confusion_matrix"]) >= {"true_permits", "true_denials", "false_permits", "false_denials"},
            "9 dataset seed": "dataset_seed" in env,
            "10 dataset gen distribution": "dataset_generation_distribution" in r["dataset"],
            "11 scenario distribution": "scenario_distribution" in env,
            "12 predicate schema version": "predicate_schema_version" in env,
            "13 token schema version": "token_schema_version" in env,
            "14 eval protocol version": "evaluation_protocol_version" in env,
            "15 system config snapshot": "system_configuration_snapshot" in env,
            "16 contamination/canary": r["contamination"]["canary_string_validation"] in ("PASS", "FAIL", "NOT_RUN"),
            "17 ASB traces": bool(r["asb"]["scenarios"]),
            "18 HITL workflow": "break_glass_protocol" in r["human_governance"],
            "19 distributed metrics": "fleet_consistency" in r["distributed_consistency"],
            "20 revocation latency": "revocation_latency_p95_ms" in r["distributed_consistency"],
            "21 replay attempts/passes/failures": all(k in l4 for k in ("replay_attempts", "replay_passes", "replay_failures")),
            "22 Evidence Quad": set(r["evidence_quad"]) >= {"spec_clause", "pre_reg_id", "method_version", "ledger_hash"},
            "23 independent replay verifier status": "independent_replay_verifier" in l4,
            "24 hardware-in-loop status": "hardware_in_the_loop" in r["independent_benchmarks"],
            "25 TLA+/TLC status": "tla_plus_tlc" in r["independent_benchmarks"],
            "26 AgentDojo/AgentHarm": "AgentDojo" in r["independent_benchmarks"] and "AgentHarm" in r["independent_benchmarks"],
            "27 third-party audit status": "third_party_audit" in r["independent_benchmarks"],
            "28 assumptions & limitations": "limitations_statement" in r["assumptions_and_limitations"],
            "29 public wording caution": r["assumptions_and_limitations"]["production_certification_claimed"] is False,
            "30 final conformance verdict": "overall_verdict" in r,
        }
        missing = [k for k, v in checks.items() if not v]
        self.assertEqual(missing, [], f"checklist items not satisfied: {missing}")
        self.assertEqual(len(checks), 30)


class TestCommittedFullReport(unittest.TestCase):
    def test_committed_report_if_present(self):
        path = os.path.join(_HERE, "concurbench_report.json")
        if not os.path.exists(path):
            self.skipTest("concurbench_report.json not present (run maincode.py or concurbench.py)")
        with open(path, encoding="utf-8") as fh:
            r = json.load(fh)
        self.assertEqual(r["benchmark_report"]["total_instances"], cb.DEFAULT_TOTAL_ITEMS)
        self.assertEqual(r["overall_verdict"], "COMPLIANT_PASS")
        self.assertEqual(r["authorization_correctness"]["false_permits"], 0)
        self.assertEqual(r["replay_and_auditability"]["replay_attempts"], cb.DEFAULT_TOTAL_ITEMS)
        self.assertEqual(r["distributed_consistency"]["testbed_type"], "simulated-fleet")


if __name__ == "__main__":
    unittest.main(verbosity=2)
