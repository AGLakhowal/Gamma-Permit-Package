# LAB v1.0 — Runtime Enforcement Verification Harness

A self-contained Python harness that simulates a **runtime reference monitor** for AI-agent
actions and measures how reliably it issues **Permit-to-Act** for legitimate requests while
holding **SAFE_STATE** on adversarial ones. It implements the paper-aligned **LAB v1.0** checks
for the **L-DREA** design (Lakhowal Deterministic Runtime Enforcement Architecture) and produces
terminal reports, a signed JSON proof receipt, and self-contained HTML dashboards.

> **Scope / honesty note.** This is a *software simulator* of the architecture's structural
> claims, plus a real cryptographic enforcement core. It does **not** run external harnesses
> (AgentDojo / AgentHarm) or hardware-in-the-loop FPGA/SGX tests, and it uses **no real customer,
> financial, or sanctions data**. See [Provenance](#provenance--what-is-real-vs-simulated).

---

## Two entry points

| Script | What it produces |
|--------|------------------|
| [maincode.py](maincode.py) | The **four-section verification run** (Runtime Enforcement, stress scenarios, quantitative metrics, benchmark reproduction) → terminal report + [maincodedashboard.html](maincodedashboard.html) |
| [lab_benchmark.py](lab_benchmark.py) | The underlying **LAB v1.0 engine**: full 1.2M-item suite, custom-CSV mode, dashboard generator, and a local upload-and-test web server → [ertuple_audit_manifest.json](ertuple_audit_manifest.json) + [dashboard.html](dashboard.html) |

```bash
python3 maincode.py            # run all four sections, write the dashboard
python3 maincode.py --open     # also open the dashboard in a browser
python3 maincode.py --fresh    # regenerate Section 4 by running lab_benchmark.py LIVE
```

Requires **Python 3** only (standard library — no dependencies).

---

## The enforcement model

Runtime Enforcement sits in front of a sensitive action (e.g. a `WIRE_TRANSFER`) and emits one
of two **transport-agnostic** outcomes for every request:

- **`PERMIT`** — Permit-to-Act granted.
- **`SAFE_STATE`** — Execution Authorization denied; the system holds safe (fail-closed).

It is **non-compensatory**: a strong score on one axis cannot buy back a failure on another.

### Γ — Predicate Failure Count

**`Γ` = the number of constitutional predicates that failed** (a severity counter — *not* a
probability, a score, or "Gamma the architecture"). `Γ = 0` means every predicate passed.

> **`Γ = 0` is NECESSARY but NOT SUFFICIENT for Permit-to-Act.** A request is permitted only when
> **all** of the following hold:
> - `Γ = 0`, and
> - a valid, unexpired, correctly-scoped, non-revoked, non-replayed capability token
>   (HMAC-SHA256 signed), and
> - a live liveness watchdog, and
> - no active persistent class-level veto (Theorem 6 persistence), and
> - the request is not a Permit-to-Adapt blocked by κ(op) coupling under risk.
>
> Anything else → **SAFE_STATE**. (The stress scenarios deliberately show `Γ = 0` still resolving
> to SAFE_STATE under a persistent class flag — that is by design, not a contradiction.)

---

## What `maincode.py` reports — the four sections

### Section 1 — Runtime Enforcement
Runs the real cryptographic monitor over the full **1,217,906-proposal** corpus
(857,906 nominal + 360,000 adversarial) and reports: **0 unauthorized permits**,
**replay determinism** over every cycle, the per-family **mutation-control** leak counts, the
**weak-baseline leak rate**, and an **adaptive-attacker** run (0 permits / 120,000 attempts).

> **Two distinct baseline metrics — never merged:**
> - **Weak-baseline leak rate** (≈ **85.0%**, e.g. 305,933 / 360,000): a *node-risk-only*
>   comparator that ignores every other check, measured on this run's adversarial corpus. This
>   is a **leak rate**, not an FPR.
> - **Paper negative-control FPR** (**6.4%**): a separately-reported figure with a different
>   baseline definition, sample set, and denominator.
>
> When both are present and differ by > 5 percentage points, the report emits a
> **reconciliation warning** rather than implying they are comparable. See
> [test_baseline_metrics.py](test_baseline_metrics.py).

### Section 2 — Stress-test scenarios (Runtime Enforcement Outcome)
Replays four documented scenarios from the *Lakhowal Stress-Test Analysis* through the
non-compensatory formula and confirms each reproduces its documented outcome:

| ID | Scenario | Outcome |
|----|----------|---------|
| P1 | Ghost Treasury Transfer ($28M deepfake-CFO wire) | Γ=6 → SAFE_STATE |
| P2 | Sanctions Drift Cascade (feed lag / stale truth / class drift) | SAFE_STATE, **DOCUMENTED SCOPE LIMITATION**, SAFE_STATE |
| P3 | Multi-Agent Liquidity Panic (aggregate velocity + class flag + κ(op)) | SAFE_STATE ×4 |
| EDGE | Sovereign Cascade Edge Case (compound failure) | Γ=5 → SAFE_STATE |

Legend: **GREEN = Permit-to-Act · RED = SAFE_STATE · YELLOW = Documented Scope Limitation**.
The YELLOW case (P2 stale-truth oracle gap) is a *documented limitation* the gate honestly
reproduces — it is not hidden.

### Section 3 — Quantitative metrics (measured locally)
- **Latency / throughput** — mean, P95, P99, max, ops/s, measured on this machine.
- **Ablations** — false-permit rate when each control (non-compensatory gating, TOCTOU
  revalidation, class-level veto, hardware interlock) is disabled in isolation.
- **Replay determinism** — observed rate plus a one-sided 95% statistical bound.
- **Goodhart resistance** — class-drift leak rate with the macro-veto off vs on, with a Wilson interval.

### Section 4 — Benchmark reproduction (reference implementation)
Maps the [lab_benchmark.py](lab_benchmark.py) LAB v1.0 results (over the 1,200,000-item corpus) to
each L-DREA benchmark claim and shows the reference implementation reproducing them under the
documented benchmark configuration — **not** an independent validation of the paper. By default it
reads the cached manifest; `--fresh` runs the suite **live** this session.

---

## The five adversarial classes (LAB-A1 … LAB-A5)

| Class | Attack modeled | Control that catches it |
|-------|----------------|-------------------------|
| LAB-A1 | Signature detachment / missing token issuance | hardware interlock |
| LAB-A2 | Token tampering — scope escalation, expiration, signature substitution | hardware interlock / TOCTOU |
| LAB-A3 | Context tampering & structured-field smuggling | non-compensatory gating |
| LAB-A4 | Expired-token use and revocation races (TOCTOU) | TOCTOU revalidation |
| LAB-A5 | Class-level "Goodhart" drift — gaming aggregate metrics | class-level veto |

Plus a large **NOMINAL** population of legitimate requests that *should* all be permitted.

In `maincode.py`, each adversarial item's family is drawn from a **declared distribution** via a
fixed seed (reproducible), so the per-family counts are **measured, not hand-set**.

---

## How it works

- **`LakhowalLLCEngine`** ([lab_benchmark.py](lab_benchmark.py)) is the reference-monitor
  simulator. It issues and verifies HMAC capability tokens, tracks consumed/revoked tokens,
  computes the non-compensatory `Γ`, enforces class-level veto persistence, and commits every
  decision into a SHA-256 **hash-chained ledger** so the run is tamper-evident and replayable.
- **`run_lab_suite`** generates a deterministic population (default 1.2M), runs each through
  `evaluate_cycle`, and aggregates metrics: FPR/FDR, Wilson 95% upper bounds (with a
  cluster/design-effect correction), a negative control, ablations, an adaptive-attacker run,
  replay determinism, and structural invariant checks.
- **`maincode.py`** wraps a real cryptographic enforcement core around a seeded adversarial corpus
  and produces the four-section report + dashboard described above.

Everything is **deterministic** — a fixed seed (`20260623`) means the same input always yields the
same results and the same ledger root hash.

---

## Files

| File | Purpose |
|------|---------|
| [maincode.py](maincode.py) | Four-section verification harness, dashboard generator, and corpus generate/run modes |
| [maincodedashboard.html](maincodedashboard.html) | Generated dashboard for the `maincode.py` run |
| [lab_corpus.jsonl](lab_corpus.jsonl) | A **real, saved** dataset — concrete proposals each with a live HMAC-SHA256 signature |
| [test_baseline_metrics.py](test_baseline_metrics.py) | Unit tests for the weak-baseline vs negative-control metric separation |
| [test_corpus_enforcement.py](test_corpus_enforcement.py) | Tests that run enforcement over a **saved corpus file** and re-verify signatures |
| [lab_benchmark.py](lab_benchmark.py) | LAB v1.0 engine, full suite, custom-CSV mode, dashboard generator, web server |
| [lab_benchmarkpart2.py](lab_benchmarkpart2.py) | Companion runner demonstrating a **failing** run from a deliberately mislabeled CSV |
| [sample_input.csv](sample_input.csv) | Example custom proposals (all correctly labeled) |
| [sample_input_fail.csv](sample_input_fail.csv) | Example with mislabeled rows → `REVIEW_REQUIRED` verdict |
| [ertuple_audit_manifest.json](ertuple_audit_manifest.json) | Proof receipt from the full LAB run (`COMPLIANT_PASS`) |
| [dashboard.html](dashboard.html) / [dashboard_part2.html](dashboard_part2.html) | Generated `lab_benchmark.py` visual reports |

---

## Usage

```bash
# === maincode.py (four-section verification) ===
python3 maincode.py                 # all four sections → maincodedashboard.html
python3 maincode.py --open          # also open the dashboard
python3 maincode.py --fresh         # Section 4 runs lab_benchmark.py LIVE (1.2M items)

# === lab_benchmark.py (engine / suite) ===
python3 lab_benchmark.py            # full LAB suite (1.2M) → manifest + dashboard
python3 lab_benchmark.py --items 50000 --open
python3 lab_benchmark.py --input sample_input.csv      # grade your own CSV
python3 lab_benchmark.py --serve                       # browser upload-and-test at http://127.0.0.1:8000
python3 lab_benchmarkpart2.py --open                   # demonstrate a FAILING run

# === real saved test data: generate -> save -> run on the saved file ===
python3 maincode.py --emit-data lab_corpus.jsonl --data-items 10000   # write real signed records
python3 maincode.py --run-data  lab_corpus.jsonl                       # enforce the SAVED file

# === tests ===
python3 -m unittest test_baseline_metrics test_corpus_enforcement
```

### Real saved test data

`--emit-data` materializes the corpus to a **JSONL file on disk** — each line is a concrete
proposal carrying a genuine HMAC-SHA256-signed capability token (you can open and inspect it).
`--run-data` loads that file and runs Runtime Enforcement over it, **re-verifying every signature
cryptographically** and grading each decision against the saved `expected` outcome. This makes the
test data a real, persisted, auditable artifact rather than in-memory ephemera.
[test_corpus_enforcement.py](test_corpus_enforcement.py) generates a fresh dataset, saves it, runs
enforcement on the saved file, and asserts 0 unauthorized permits, 0 false denials, and that the
stored signatures verify (and that forged ones do not).

### Key options (`lab_benchmark.py`)

| Flag | Default | Description |
|------|---------|-------------|
| `--items` | `1200000` | Number of LAB proposals to generate |
| `--seed` | `20260623` | Deterministic generator seed |
| `--input` | — | CSV of custom proposals to test instead of generated data |
| `--manifest` | `ertuple_audit_manifest.json` | Output JSON proof receipt |
| `--dashboard` | `dashboard.html` | Output self-contained HTML dashboard |
| `--serve` / `--host` / `--port` | `127.0.0.1:8000` | Start the local upload-and-test web server |
| `--open` | off | Open the dashboard in your browser when finished |

### Custom CSV format

```
id,op,node_risk,node_threshold,class_name,class_risk,class_threshold,token_kind,watchdog,expected
1,WIRE_TRANSFER,0.10,0.50,finance,0.01,0.10,valid,true,allow
2,WIRE_TRANSFER,0.10,0.50,finance,0.01,0.10,forged,true,block
```

`token_kind` can be `valid`, `forged`, `expired`, `revoked`, `missing`, or `scope_mismatch`.
`expected` is the ground-truth `allow` / `block` the engine's decision is graded against.

---

## Output & verdicts

Each run prints a terminal report and generates a self-contained HTML dashboard. The
`audit_verdict` is:

- **`COMPLIANT_PASS`** — zero unauthorized permits, 100% replay determinism, adaptive attacker
  contained, and all invariants hold.
- **`REVIEW_REQUIRED`** — decisions disagreed with the expected labels (see the part-2 example).

The `final_ledger_root_hash` is the tamper-evident root of the decision ledger; with a fixed seed
and input it is reproducible across runs.

---

## Provenance — what is real vs simulated

| Component | Status |
|-----------|--------|
| Gate logic / cryptography (HMAC-SHA256) | **Measured by the reference implementation** — executed on every evaluated item |
| Section 1 / 3 metrics (leaks, latency, ablations, Goodhart) | **Measured** from the live run |
| Section 1 adversarial corpus | **Simulated** — drawn from a declared distribution; fixed by the documented seed and fully reproducible |
| Section 2 predicate verdicts | **Transcribed** from the documented Stress-Test Analysis; the enforcement **decision** is computed live |
| Section 4 lab suite | **Real `lab_benchmark.py` output** (cached, or live via `--fresh`) — never hand-typed |

No real customer, financial, or sanctions data is used anywhere in this harness. The local
software latency (sub-millisecond) is far below the paper's hardware-in-the-loop reference figure,
by design.
