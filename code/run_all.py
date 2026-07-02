#!/usr/bin/env python3
"""run_all.py - one command to run the entire Gamma G-0 / LAB v1.0 pipeline.

Stages, in order:
  1. Materialize the real signed corpus (lab_corpus.jsonl) if missing.
  2. Run the LAB v1.0 engine   -> ertuple_audit_manifest.json + dashboard.html
  3. Run the main verification -> maincodedashboard.html + Section 5/6 evidence
     artifacts (LDREA.tla/.cfg, ertuple_replay_manifest.json,
     reproducibility_bundle.json, concurbench_report.json)
  4. Run the test suite (baseline, corpus enforcement, engine, ConcurBench).
  5. Print a consolidated verdict summary.

Usage:
    python3 run_all.py                 # full pipeline (ConcurBench included, ~3 min)
    python3 run_all.py --quick         # skip the ConcurBench packet (fast)
    python3 run_all.py --open          # open both dashboards when finished
    python3 run_all.py --skip-tests    # skip the unit tests
    python3 run_all.py --data-items N  # corpus size for stage 1 (default 10000)
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable or "python3"


def _path(name):
    return os.path.join(HERE, name)


def run_stage(title, cmd):
    print(f"\n{'=' * 72}\n[STAGE] {title}\n{'=' * 72}", flush=True)
    t0 = time.time()
    result = subprocess.run(cmd, cwd=HERE)
    dt = time.time() - t0
    ok = result.returncode == 0
    print(f"[{'OK ' if ok else 'FAIL'}] {title}  ({dt:.1f}s)", flush=True)
    return ok


def _read_json(name):
    try:
        with open(_path(name), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def main():
    ap = argparse.ArgumentParser(description="Run the full LAB v1.0 / ConcurBench pipeline.")
    ap.add_argument("--quick", action="store_true", help="skip the ConcurBench packet")
    ap.add_argument("--open", action="store_true", help="open dashboards when finished")
    ap.add_argument("--skip-tests", action="store_true", help="skip the unit tests")
    ap.add_argument("--data-items", type=int, default=10000, help="corpus size (stage 1)")
    args = ap.parse_args()

    t0 = time.time()
    results = {}

    # Stage 1 - corpus (only if absent, so we never clobber a committed one silently)
    if not os.path.exists(_path("lab_corpus.jsonl")):
        results["corpus"] = run_stage(
            "1/4  Materialize signed corpus (lab_corpus.jsonl)",
            [PY, "maincode.py", "--emit-data", "lab_corpus.jsonl",
             "--data-items", str(args.data_items)])
    else:
        print("[SKIP] 1/4  lab_corpus.jsonl already present")
        results["corpus"] = True

    # Stage 2 - LAB engine (manifest + dashboard.html)
    results["lab_benchmark"] = run_stage(
        "2/4  LAB v1.0 engine (manifest + dashboard.html)",
        [PY, "lab_benchmark.py"] + (["--open"] if args.open else []))

    # Stage 3 - main verification (Sections 1-6 + evidence artifacts)
    main_cmd = [PY, "maincode.py"]
    if args.quick:
        main_cmd.append("--no-concurbench")
    if args.open:
        main_cmd.append("--open")
    results["maincode"] = run_stage(
        "3/4  Main verification (Sections 1-6 + evidence bundle"
        + (" ; ConcurBench SKIPPED" if args.quick else " ; ConcurBench included") + ")",
        main_cmd)

    # Stage 4 - tests
    if args.skip_tests:
        print("[SKIP] 4/4  unit tests (--skip-tests)")
        results["tests"] = None
    else:
        tests = ["test_baseline_metrics", "test_corpus_enforcement", "lab_benchmark"]
        if not args.quick:
            tests.append("test_concurbench")
        results["tests"] = run_stage(
            "4/4  Unit tests (" + ", ".join(tests) + ")",
            [PY, "-m", "unittest"] + tests)

    # ----- consolidated summary ------------------------------------------- #
    manifest = _read_json("ertuple_audit_manifest.json")
    cb = _read_json("concurbench_report.json")
    print(f"\n{'=' * 72}\n  PIPELINE SUMMARY\n{'=' * 72}")
    print(f"  {'Corpus materialized':<34}: {'OK' if results['corpus'] else 'FAIL'}")
    print(f"  {'LAB engine run':<34}: {'OK' if results['lab_benchmark'] else 'FAIL'}")
    print(f"  {'Main verification run':<34}: {'OK' if results['maincode'] else 'FAIL'}")
    if results["tests"] is None:
        print(f"  {'Unit tests':<34}: skipped")
    else:
        print(f"  {'Unit tests':<34}: {'PASS' if results['tests'] else 'FAIL'}")
    if manifest:
        r = manifest.get("results", {})
        print(f"  {'LAB audit_verdict':<34}: {manifest.get('audit_verdict')}")
        print(f"  {'  false permits / adversarial':<34}: "
              f"{r.get('false_permits_count')} / {r.get('total_adversarial_items')}")
        print(f"  {'  Clopper-Pearson 95% UB':<34}: "
              f"< {r.get('clopper_pearson_95_upper_bound', float('nan')):.2e}")
    if cb:
        cl = cb.get("conformance_levels", {})
        print(f"  {'ConcurBench verdict':<34}: {cb.get('overall_verdict')}")
        print(f"  {'  levels L1/L2/L3/L4':<34}: "
              f"{cl.get('level_1_authorization_correctness')}/"
              f"{cl.get('level_2_adversarial_robustness')}/"
              f"{cl.get('level_3_distributed_consistency')}/"
              f"{cl.get('level_4_replay_auditability')}")
    elif args.quick:
        print(f"  {'ConcurBench verdict':<34}: skipped (--quick)")
    print("-" * 72)
    print("  Artifacts: maincodedashboard.html · dashboard.html · "
          "ertuple_audit_manifest.json")
    print("             concurbench_report.json · reproducibility_bundle.json · "
          "LDREA.tla/.cfg")
    print(f"  Total: {time.time() - t0:.1f}s")
    print("=" * 72)

    core_ok = all(v for k, v in results.items()
                  if k != "tests" and v is not None) and (results["tests"] in (True, None))
    sys.exit(0 if core_ok else 1)


if __name__ == "__main__":
    main()
