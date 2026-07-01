#!/usr/bin/env python3
"""
run_all.py - one command to run the entire Gamma / ConcurBench suite.
=====================================================================

Pipeline (in order):

  1. Base LAB v1.0 benchmark        (gamma_test_runner.py)   [--full or if missing]
       -> gamma_lab_v1_report.json, gamma_summary.json,
          gamma_replay_manifest.jsonl, gamma_terminal_full.txt
  2. ConcurBench full conformance   (concurbench_full.run)   -> concurbench_full_report.json
  3. Financial stress test          (stress_test.run)        -> stress_test_report.json
  4. Fail-Closed Rate test          (fcr_test.run)           -> fcr_test_report.json
  5. Unified dashboard              (gamma_report_page.render) -> gamma_report.html
       (base LAB sections + ConcurBench + stress + FCR, all in one page)

Usage:
  python run_all.py                 # run EVERYTHING end-to-end (default; nothing skipped)
  python run_all.py --reuse         # fast path: reuse existing base artifacts, run layers 2-5
  python run_all.py --no-open       # don't auto-open the dashboard
  python run_all.py --input FILE    # base benchmark input CSV
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LAB_REPORT = ROOT / "gamma_lab_v1_report.json"
SUMMARY = ROOT / "gamma_summary.json"
TERMINAL = ROOT / "gamma_terminal_full.txt"
DASHBOARD = ROOT / "gamma_report.html"


def _hr(title: str) -> None:
    print("\n" + "#" * 70 + f"\n#  {title}\n" + "#" * 70)


def run_base(input_csv: str | None) -> None:
    _hr("STEP 1/5  base LAB v1.0 benchmark (gamma_test_runner.py)")
    cmd = [sys.executable, str(ROOT / "gamma_test_runner.py"), "--no-open"]
    if input_csv:
        cmd += ["--input", input_csv]
    print("  $", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the full Gamma / ConcurBench suite.")
    ap.add_argument("--reuse", action="store_true",
                    help="Fast path: skip the heavy base benchmark and reuse "
                         "existing artifacts (default runs everything).")
    ap.add_argument("--no-open", action="store_true",
                    help="Do not auto-open the dashboard in a browser.")
    ap.add_argument("--input", default=None,
                    help="Base benchmark input CSV.")
    args = ap.parse_args()
    t0 = time.time()

    # 1. base benchmark — run by default so nothing is hidden; only skipped when
    #    --reuse is passed AND the artifacts already exist.
    if args.reuse and LAB_REPORT.exists() and SUMMARY.exists():
        _hr("STEP 1/5  base LAB v1.0 benchmark  [SKIPPED — --reuse]")
        print(f"  reusing {LAB_REPORT.name} + {SUMMARY.name} "
              f"(omit --reuse to run the full benchmark)")
    else:
        run_base(args.input)

    # imported lazily so a missing base artifact fails with a clear message first
    import concurbench_full
    import stress_test
    import fcr_test
    import gamma_report_page

    # 2. ConcurBench full conformance
    _hr("STEP 2/5  ConcurBench full conformance (concurbench_full.py)")
    concurbench = concurbench_full.run(write=True)

    # 3. stress test
    _hr("STEP 3/5  financial-services stress test (stress_test.py)")
    stress = stress_test.run(write=True)

    # 4. FCR test
    _hr("STEP 4/5  Fail-Closed Rate test (fcr_test.py)")
    fcr = fcr_test.run(write=True)

    # 5. unified dashboard
    _hr("STEP 5/5  unified dashboard (gamma_report_page.py)")
    lab = json.loads(LAB_REPORT.read_text())
    summary = json.loads(SUMMARY.read_text())
    terminal_txt = TERMINAL.read_text() if TERMINAL.exists() else ""
    gamma_report_page.render(
        lab, summary, DASHBOARD, terminal_txt=terminal_txt,
        open_browser=not args.no_open,
        extra={"concurbench": concurbench, "stress": stress, "fcr": fcr},
    )

    dt = time.time() - t0
    _hr("SUITE COMPLETE")
    print(f"  ConcurBench verdict      : {concurbench.get('overall_verdict')}")
    print(f"  Stress weighted tackled  : "
          f"{stress['aggregate']['weighted_effectively_tackled_pct']}%")
    print(f"  FCR                      : {fcr['overall']['FCR']} "
          f"(fail-open={fcr['overall']['fail_open_events']})")
    print(f"  Dashboard                : {DASHBOARD.name}")
    print(f"  Artifacts                : concurbench_full_report.json, "
          f"stress_test_report.json, fcr_test_report.json")
    print(f"  Elapsed                  : {dt:.1f}s")


if __name__ == "__main__":
    main()
