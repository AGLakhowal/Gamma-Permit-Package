"""LAB v1.0 benchmark — Part 2 (failing-example run).

Companion to lab_benchmark.py. Where `python3 lab_benchmark.py` runs the
generated LAB suite (everything passes), this script runs a CSV that contains
deliberately mislabeled rows so the engine's decision disagrees with the
expected verdict — i.e. it shows what a FAILING run looks like.

Usage:
    python3 lab_benchmarkpart2.py                 # uses sample_input_fail.csv
    python3 lab_benchmarkpart2.py --input my.csv  # any CSV you like
    python3 lab_benchmarkpart2.py --open          # open the dashboard when done
"""

import argparse
import json
import os
import webbrowser

from lab_benchmark import (
    DEFAULT_SEED,
    build_custom_manifest,
    build_dashboard_html,
    format_custom_report,
    load_custom_rows,
    run_custom_suite,
)

DEFAULT_INPUT = "sample_input_fail.csv"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the LAB v1.0 benchmark against a failing-example CSV."
    )
    parser.add_argument("--input", default=DEFAULT_INPUT,
                        help=f"CSV of proposals to test (default {DEFAULT_INPUT}).")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="Deterministic generator seed.")
    parser.add_argument("--manifest", default="ertuple_audit_manifest_part2.json",
                        help="Output JSON proof receipt.")
    parser.add_argument("--dashboard", default="dashboard_part2.html",
                        help="Output self-contained HTML dashboard.")
    parser.add_argument("--open", action="store_true",
                        help="Open the HTML dashboard in the default browser when done.")
    args = parser.parse_args()

    print("[INIT] Initializing Lakhowal deterministic runtime enforcement test engine...")
    rows = load_custom_rows(args.input)
    print(f"[DATA] Loaded {len(rows):,} custom proposals from {args.input} (seed {args.seed})...")

    results = run_custom_suite(rows, args.seed)
    manifest = build_custom_manifest(results, args.seed, args.input)
    report_text = format_custom_report(manifest)

    print("\n" + report_text)

    with open(args.manifest, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"[SUCCESS] Proof validation manifest generated: {args.manifest}")

    dashboard_html = build_dashboard_html(manifest, report_text)
    with open(args.dashboard, "w", encoding="utf-8") as handle:
        handle.write(dashboard_html)
    dashboard_path = os.path.abspath(args.dashboard)
    print(f"[SUCCESS] Visual dashboard generated: {dashboard_path}")

    verdict = manifest.get("audit_verdict", "")
    print(f"[VERDICT] {verdict}")
    if args.open:
        webbrowser.open(f"file://{dashboard_path}")


if __name__ == "__main__":
    main()
