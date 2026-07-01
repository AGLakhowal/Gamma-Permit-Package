# Reproducing this GAMMA G-0 / L-DREA LAB v1.0 run

Method version: `gamma_test_runner/LAB-v1.0/2.0`
Bundle digest (SHA-256): `8bd413fc3c07aa26df17d7c3b242acd3aa3442903d9df209475a115efc8b54eb`

## 1. Environment
- Python: `3.9.6 (default, Apr 17 2026, 18:15:52) `
- pandas: `2.3.3`
- Platform: `macOS-26.5.1-arm64-arm-64bit`

Install: `pip install pandas`

## 2. Verify the inputs are byte-identical
Check each SHA-256 in `MANIFEST.json` against your local copies, e.g.:

```
shasum -a 256 GAMMA_G0_CREDITCARD_FULL_mapped.csv
```

It must match the `input[].sha256` in `MANIFEST.json`.

## 3. Re-run the benchmark (regenerates every output)
```
/Library/Developer/CommandLineTools/usr/bin/python3 gamma_test_runner.py --input GAMMA_G0_CREDITCARD_FULL_mapped.csv --output gamma_validation_results.csv --summary gamma_summary.json --lab-report gamma_lab_v1_report.json --replay-manifest gamma_replay_manifest.jsonl --bundle gamma_bundle --html gamma_report.html --no-open
```

## 4. Independently verify the per-item replay manifest
No pandas required — pure stdlib:
```
python gamma_replay_verify.py gamma_replay_manifest.jsonl
```
Expect: `n_records=284807`, all adjacency links OK,
genesis-anchored, and manifest SHA-256 =
`1ce2a9e8d4330a0583a9d20a398de43297ea59c404e006e7f1161208481931da`.

## 5. TLC attestation
TLC verified: `True`;
attestation digest `8cb1369625e05e6ad00004be477ce50f6c0792f0c9913a234e2ddf0767207686`.
To cryptographically bind to source, re-run with
`--tla-spec <spec.tla> --tla-cfg <cfg.cfg>`; those SHA-256s must equal
`spec_hash`/`cfg_hash` in `MANIFEST.json`.

## 6. Compare outputs
Re-hash the regenerated outputs and compare to `outputs[].sha256` in
`MANIFEST.json`. Deterministic fields (decisions, gamma, hash-chain, evidence
quads) reproduce exactly; MEASURED latency fields are host-dependent and will
differ.
