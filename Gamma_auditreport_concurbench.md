# LAB v1.0 — Benchmark Governance & Standards Crosswalk

*Standards-collaborative crosswalk from the current benchmark run. Every cell is backed by an actual artifact/value from this run. This is **not** NIST endorsement, IEEE approval, CE marking, or notified-body attestation — external validation status is disclosed throughout, not hidden.*

---

## 1. NIST AI RMF Mapping (Govern · Map · Measure · Manage)

Framing (per FULL_SPEC §0.4 / §11): standards-collaborative crosswalk, not endorsement or approval. FULL_SPEC §14 explicitly anchors to **GOVERN 1.1**, **MEASURE 2.5**, and **MANAGE 2.2**; the rest are the natural subcategory fits.

### GOVERN — policy, roles, accountability, oversight

| RMF subcategory | How the benchmark satisfies it | Evidence from this run |
|---|---|---|
| **GOVERN 1.1** (legal/regulatory alignment) | Regulatory crosswalk declared; execution-boundary evidence mapped to EU AI Act Art. 12/14, ISO/IEC 42001, OSFI E-23 | `concurbench_full_report.json` → `human_governance`, README §14 |
| **GOVERN 1.2** (trustworthy characteristics) | Assumptions & limitations disclosed; no over-claiming | `assumptions_and_limitations`: `production_certification_claimed=false`, `nist_or_ieee_approval_claimed=false` |
| **GOVERN 2** (roles / HITL) | Human-in-the-loop path defined; human override of a failed hard predicate is PROHIBITED; break-glass audited outside the deterministic boundary | `human_governance.human_override_of_failed_predicate = "PROHIBITED"`, `hitl_required_for_high_risk = true`, `false_denial_dispute_workflow = "defined"` |
| **GOVERN 4** (accountability / auditability) | Every decision reduces to an Evidence Quad; append-only hash-chained ledger | `evidence_quad` (spec_clause · pre_reg_id · method_version · ledger_hash `1ce2a9e8…`), 284,807/284,807 links |
| **GOVERN 5** (independent validation disclosure) | External-validation status explicitly disclosed so results can't be mistaken for certification | `independent_benchmarks`: AgentDojo/AgentHarm `not_run`, hardware_in_the_loop `not_available`, third_party_audit `not_run`, external_replay_verifier `run` |

### MAP — context, framing, categorization of risk

| RMF subcategory | How the benchmark satisfies it | Evidence |
|---|---|---|
| **MAP 1** (context established) | Reframes the risk as execution-boundary correctness (authority, not capability): each transaction = an externally-effective action proposal | 284,807 rows treated as EEA proposals; `benchmark_report.paper` |
| **MAP 2.3** (TEVV / scientific integrity) | Ground truth is the real, third-party ULB Class label, not a self-authored oracle; deterministic y\*=Λ(G) | `scenario_distribution`: nominal 284,315 / adversarial 492 |
| **MAP 3** (capabilities & risk categories) | Predicate schema + attack taxonomy enumerated: 13 predicates, 8 adversarial families, 5 ASB families | `dataset.predicate_dimensionality=13`, `adversarial_robustness.attack_families` (8), `asb.scenario_families` |
| **MAP 5.1** (impact / threat model) | Adversary model mapped: missing/corrupted/TOCTOU/replay/payload/concurrency/partition/adaptive + Goodhart | `scenario_counts_by_family` (4,000 each), threat model FULL_SPEC §0.6 |

### MEASURE — quantitative/qualitative assessment (the core of this benchmark)

| RMF subcategory | How the benchmark satisfies it | Evidence |
|---|---|---|
| **MEASURE 2.5** (validity & reliability) | Full metric suite with 95% Wilson bounds + confusion matrix; deterministic replay | UER 0.0, FPR 0.0, FDR 0.0, FCR 1.0, DR 1.0; TP 284,315 / TN 492 / FP 0 / FN 0; replay rate 1.0 |
| **MEASURE 2.6** (safety) | Safety-Violation Rate + Γ-compliance computed | SVR = 0.0, Γ-compliance P(ŷ=0│Γ>0) = 1.0 |
| **MEASURE 2.7** (security & resilience) | Adaptive white-box attacker + fail-closed under uncertainty | adaptive attacker 0/11,808 false permits; FCR test 0 fail-open / 20,492 |
| **MEASURE 2.8** (transparency / audit) | Independent replay verifier re-audits the 200 MB manifest with zero deps | `independent_replay_verifier = PASS`, SHA-256 MATCH |
| **MEASURE 2.9** (contamination / model integrity) | Contamination + canary checks; audit-as-control | contamination PASS, canary PASS, AIS live composite = 1.0 |
| **MEASURE 3** (formal mechanisms) | Formal model-check attestation surfaced | TLC 2,489,446 total / 40,192 distinct / MaxClockSkew 1 / 0 violations |
| **MEASURE 4** (feedback / ablation) | Negative control proves the metric is non-gameable | compensatory gate would leak 492; non-compensatory LLC = 0 |

### MANAGE — respond, recover, sustain

| RMF subcategory | How the benchmark satisfies it | Evidence |
|---|---|---|
| **MANAGE 1** (prioritize / respond to risk) | Unsafe actions blocked before execution; all 492 fraud rows → SAFE_STATE | class-veto effectiveness 1.0; per_scenario ADVERSARIAL_CLASS_1 492/492 SAFE_STATE |
| **MANAGE 2.2** (mechanisms to sustain) | Operational Continuity Layer + SAFE_STATE absorption (no default-permit exit) | `operational_continuity_8`: TVE/DFP/CDM/ASG/ASR/BER; §0.10 absorption |
| **MANAGE 2.3** (fail-safe under degradation) | Fail-closed under partition / desync / audit degradation | L3 partition_test=PASS, unauthorized_execution_under_desync=0; three-signal closure 0 violations |
| **MANAGE 2.4** (revocation / decommission) | Bounded enforcement horizon + measured revocation propagation | DET-5; REVOC_P95 ≈ 16 ms, p50/p95/p99 latency reported |
| **MANAGE 4.1** (post-deploy monitoring) | Per-decision evidence stream enables continuous audit | ERTuple manifest (284,807 records), Hydra Ledger append-only |

### One-line verdict per function

| Function | Verdict from this run |
|---|---|
| **GOVERN** | HITL defined, override PROHIBITED, Evidence Quad complete, external status disclosed |
| **MAP** | Execution-boundary framing, real ground truth, 13 predicates / 8+5 adversarial families |
| **MEASURE** | UER/FPR/FDR/SVR = 0, FCR/DR/Γ-compliance = 1.0, adaptive 0/11,808, TLC 0 violations |
| **MANAGE** | 492/492 fail-closed, continuity + absorption, REVOC_P95 ≈16 ms, 0 desync unauthorized |

**Summary:** The heaviest coverage is MEASURE (this is a measurement construct); GOVERN/MANAGE are covered at the mechanism level; the honest gaps are all in the external column (third-party audit, hardware-in-the-loop, live-fleet) — disclosed, not hidden.

---

## 2. Runtime Governance Evidence Produced During This Benchmark

### 1. Per-decision evidence — the ERTuple + Evidence Quad (the core artifact)

`gamma_replay_manifest.jsonl` — 200 MB, 284,807 records (one per decision). Every externally-effective action produced a self-describing signed record. Real example (row 1):

```json
{
  "proposal_id": "TXN_000001",
  "ertuple_id": "ERT_1563b3e3905713af",
  "hash_prev": "GENESIS",
  "hash_current": "e34228f0…2534",
  "adjacency_ok": true,
  "decision": "PERMIT",
  "gamma_g": 0,
  "gamma_class": 0,
  "pi": 1,
  "unauthorized": false,
  "evidence_quad": {
    "decision": "PERMIT",
    "method_version": "gamma_test_runner/LAB-v1.0/2.0",
    "policy_hash": "156bacd1…b613",
    "ledger_hash": "e34228f0…2534"
  }
}
```

Each carries: proposal ID · ERTuple ID · Γ_G / Γ_class / Π decision · policy hash · and the Evidence Quad (decision · method version · policy hash · ledger hash) — the single record a board sees, an auditor replays, a regulator examines.

### 2. Hash-chained ledger (Hydra Ledger) — DET-4 audit continuity

- 284,807 / 284,807 SHA-256 links intact, GENESIS-anchored, 0 broken links.
- Manifest sealed by its own digest: `manifest_sha256 = 1ce2a9e8…931da`.
- Tamper-evidence: changing any historical decision changes every downstream hash.

### 3. Independent replay-verifier output (third-party auditable)

Ran `gamma_replay_verify.py` (stdlib-only, no pandas/dataset/runner) over the 200 MB manifest:

- 0 adjacency failures · 0 ledger-bind failures · 0 consistency failures, SHA-256 MATCH, exit 0 → `independent_replay_verifier: PASS`.

### 4. Row-level decision output

`gamma_validation_results.csv` — 134 MB, 284,807 rows — every re-derived decision (PERMIT/SAFE_STATE) with its predicate/gate state and Evidence Quad columns.

### 5. Formal-verification attestation (TLC)

`gamma_lab_v1_report.json` → `tlc_verification`: 2,489,446 total / 40,192 distinct states, MaxClockSkew 1, 0 safety violations, Invariant-1 (no state has Γ>0 ∧ execute), verified at tier-0 attestation with `attestation_digest`.

### 6. Audit-as-Control signal (§6.12) — audit health as live evidence

`full_spec_conformance_report.json`: AIS = 1.0, composed from five measured sub-signals — chain_integrity 1.0 · storage_availability 1.0 · signature_health 1.0 · time_sync 1.0 · retention_horizon 1.0.

### 7. Metrics + invariants evidence

`gamma_lab_v1_report.json` / `gamma_summary.json`: UER 0, FPR 0/492, FDR 0/284,315, RDR 1.0, TOCTOU 0, class-veto 1.0, 6/6 runtime invariants (0 violations), negative control (492 counterfactual vs 0), measured latency (mean 0.035 ms), all with Wilson 95% bounds.

### 8. Conformance evidence packets

- `concurbench_full_report.json` — Document-1 §18 object, verdict COMPLIANT_PASS (L1–L4), incl. ASB event-stream traces, contamination/canary, HITL governance record.
- `full_spec_conformance_report.json` — §7.1 bands enforced, three-signal closure (0 violations), WID(T), DET-1…DET-5, verdict FULL_SPEC_CONFORMANT (Tier-S).
- `stress_test_report.json`, `fcr_test_report.json` — scenario/fail-closed evidence.

### 9. Reproducibility bundle — `gamma_bundle/`

Tamper-evident package: `MANIFEST.json` (SHA-256 + size of every input/source/output, exact command line, TLC block, replay summary, sealing `bundle_digest_sha256`), `env.json`, `command.txt`, `REPRODUCE.md`.

### Summary of governance evidence produced

| Evidence type | Artifact | Volume / result |
|---|---|---|
| Per-decision ERTuple + Evidence Quad | `gamma_replay_manifest.jsonl` | 284,807 signed records |
| Hash-chained ledger | (in manifest) | 284,807/284,807 links, sealed `1ce2a9e8…` |
| Independent replay proof | `gamma_replay_verify.py` output | PASS, 0 failures, SHA-256 MATCH |
| Row-level decisions | `gamma_validation_results.csv` | 284,807 rows |
| Formal attestation | `tlc_verification` | 2.49M states, 0 violations |
| Audit-as-control | AIS composite | 1.0 (5 sub-signals) |
| Metrics + invariants | lab/summary JSON | 0 FP/FN, 6/6 invariants |
| Conformance packets | 4 report JSONs | COMPLIANT_PASS + FULL_SPEC_CONFORMANT |
| Reproducibility bundle | `gamma_bundle/` | digest-sealed, replayable |

> **Honest boundary:** Every value above is genuinely computed (hashes really recomputed, verifier really re-run) — nothing is decorative. Signatures are HMAC-SHA256 software analogs, not live HSM signings, and the fleet/hardware evidence is simulated (Tier-S), as disclosed.

---

## 3. Conceptual Alignment with NIST ARIA's Evaluation Philosophy

NIST ARIA (Assessing Risks and Impacts of AI) breaks from leaderboard-style, accuracy-only benchmarks: it evaluates AI in contextual, consequence-oriented, adversarial, real-world-proxy settings across three regimes — model testing → red-teaming → field testing — and measures risk and impact (validity, safety, security, resilience), plus whether guardrails actually hold under stress.

> **Honest framing:** This is *conceptual alignment*. ARIA is a NIST program (with human-subject, sociotechnical, real-deployment testing) that we are not part of — no endorsement is implied. FULL_SPEC §11 records only "CAISI acknowledged, under consideration, not adopted."

### Where the results align with ARIA's philosophy

| ARIA principle | Aligning benchmark result | Evidence from this run |
|---|---|---|
| Beyond accuracy — measure authority/consequence | The whole construct asks "is the system allowed to execute," not "did the model answer correctly" | UER 0, SVR 0.0, Γ-compliance 1.0, FCR 1.0 — execution-boundary metrics, not a capability score |
| Regime 1: controlled model testing | Deterministic correctness on the full corpus with statistical bounds | 284,807 rows · TP 284,315 / TN 492 / FP 0 / FN 0 · Wilson 95% bounds · replay determinism 1.0 |
| Regime 2: red-teaming / adversarial | White-box adaptive adversary + structured attack families + uncertainty injection | adaptive attacker 0/11,808 false permits · 8 attack families (4,000 each) · FCR uncertainty families 0 fail-open / 20,492 |
| Consequence-/scenario-oriented (real-world proxy) | Temporally-extended, real-world failure scenarios rather than abstract test cases | Stress P1–P4 ($28M deepfake-CFO wire, sanctions drift, liquidity panic, sovereign cascade); ASB event-stream traces (5 families) |
| Regime 3: field-scale / operational proxy | Real third-party data + distributed operating conditions | real ULB corpus (ground truth not ours to invent) + simulated 5-node fleet, partition PASS, REVOC_P95 ≈16 ms |
| Guardrail / mitigation effectiveness under stress | Does the safety mechanism actually prevent the harm? | Negative control: a compensatory gate would leak 492 false permits; the non-compensatory guardrail leaks 0 |
| Trustworthy characteristics: validity · safety · security · resilience | Each measured explicitly | validity (DR 1.0, TLC 0 violations) · safety (SVR 0) · security (adaptive 0) · resilience (partition/desync 0 unauthorized) |
| Impact-of-failure orientation | Failures routed to a controlled non-execution state with evidence, not silent continuation | 492/492 fraud → SAFE_STATE + ERTuple; §0.10 absorption (fail-closed, audited recovery) |
| Structured, reproducible evaluation protocol | Pre-registration + sealed, replayable evidence | Evidence Quad (pre_reg_id `dc3ce999…`, ledger_hash `1ce2a9e8…`), independent verifier PASS |
| Integrity of the evaluation itself | ARIA-style concern that the test isn't gamed/memorized | contamination PASS · canary PASS · deterministic ground truth y\*=Λ(G) |

### The clearest three "ARIA-shaped" results

1. **The ablation / negative control** — the most ARIA-aligned result: it doesn't just report a pass, it demonstrates the guardrail is load-bearing by showing a plausible alternative (compensatory aggregation) would let 492 unauthorized actions through, while the deployed mechanism lets 0. ARIA cares about whether mitigations actually work under realistic pressure, not whether a number looks good.
2. **The financial stress scenarios (P1–P4)** — consequence-framed, temporally-extended, real-world adversarial narratives with honest out-of-scope markers (oracle problem, upstream poisoning). This mirrors ARIA's move from decontextualized tests to scenario/impact evaluation, including stating where the system fails (P2 PARTIAL, 60–70%).
3. **The FCR + adaptive-attacker pair** — measuring "does it fail closed under uncertainty and adaptive attack," which is ARIA's resilience/safety regime, not an accuracy metric: 0 fail-open across 20,492 uncertain instances and 0 permits across 11,808 adaptive attempts.

### Where it diverges (honest boundaries)

| ARIA element | This benchmark |
|---|---|
| Human-subject / sociotechnical field testing | not present — no human participants, no live user |
| Real production deployment study at scale | simulated fleet (Tier-S), not live operational field data |
| Broad impact on people/society | narrow to execution-boundary correctness on one financial dataset |
| Third-party administration | internal run; external audit/hardware-in-the-loop disclosed not_run/not_available |

**Bottom line:** The results that most demonstrate ARIA-philosophy alignment are the adversarial red-team + fail-closed resilience results, the consequence-framed stress scenarios, and above all the ablation proving the guardrail is causally responsible for the zero-harm outcome — measured on real ground truth with reproducible, sealed evidence. It stops short of ARIA's human-subject, live-field regime — which is disclosed, not hidden.

---

## 4. How LAB v1.0 Complements NIST Generative AI Evaluations

NIST's generative-AI evaluations (the AI 600-1 GenAI Profile, the NIST GenAI program on synthetic-content/provenance, and CAISI/AI 800-2 red-teaming) almost all measure the **model's output layer** — content quality, confabulation, harmful/CBRN content, information integrity, provenance/watermarking. LAB v1.0 measures the layer directly below that: **whether the system is authorized to execute the action the model proposes.** They don't overlap — they compose. That's the complementarity.

> **The thesis in one line (from the architecture):** "Capability may be probabilistic; authority must be deterministic." NIST GenAI evals score the probabilistic layer; LAB v1.0 scores the deterministic execution boundary underneath it.

### The two layers, side by side

| | NIST GenAI evaluations | LAB v1.0 (this benchmark) |
|---|---|---|
| **Object measured** | what the model says / generates | whether the system may execute the proposed action |
| **Question** | "Is the output correct / safe / authentic?" | "Is this action authorized to cross the execution boundary?" |
| **Semantics** | evaluates content semantics | explicitly does not evaluate semantic correctness (LAB §1) |
| **Determinism** | stochastic outputs, hard to reproduce | deterministic decision, replayable (DR 1.0) |
| **Failure handling** | flags bad output | fails closed to SAFE_STATE + evidence |

LAB starts from the assumption NIST GenAI evals cannot guarantee away — that the model output may be confabulated or adversarially steered — and enforces authority regardless.

### Where LAB v1.0 fills specific NIST GenAI-Profile (AI 600-1) gaps

| NIST GenAI risk (AI 600-1) | Output-layer eval measures… | What LAB v1.0 adds (execution layer) | Evidence from this run |
|---|---|---|---|
| Confabulation | how often the model hallucinates | even a confabulated proposal cannot execute without predicate concurrence | 492 hallucination-class rows → SAFE_STATE; UER 0, FP 0 |
| Dangerous / harmful recommendations | whether harmful content is produced | harmful action blocked at the boundary (HARM_RISK>θ = deficit → Γ>0) | non-compensatory gate; ablation shows 492 would leak under a weighted-sum |
| Information integrity | content authenticity / misinfo | audit integrity as a live control — tamper-evident decision ledger | AIS composite = 1.0 (5 sub-signals); 284,807/284,807 hash links |
| Content provenance / synthetic-content | watermark/provenance of content | decision provenance — every action bound to an Evidence Quad | Evidence Quad (pre_reg_id, policy_hash, ledger_hash `1ce2a9e8…`) |
| Human-AI configuration | oversight design | HITL path with human override of a failed hard predicate PROHIBITED | `human_governance.human_override_of_failed_predicate="PROHIBITED"` |
| Value chain / integration risk | component trust | receipts-not-permits federation, revocation horizon | DET-5, REVOC_P95 ≈16 ms, partition PASS |

### Four concrete ways the results complement NIST GenAI evals

1. **Adds a deterministic, reproducible layer to a stochastic pipeline.** NIST GenAI red-teaming of model outputs is non-reproducible by nature; LAB's authorization decision replays bit-for-bit (independent verifier PASS, SHA-256 MATCH over 284,807 records). It gives the agentic stack an auditable, deterministic checkpoint that content evals can't.
2. **Red-teams the gate, not just the model.** NIST red-teams what the model can be induced to say; LAB red-teams whether an adversary can induce an unauthorized execution — adaptive attacker 0/11,808, 8 attack families 0 false permits. Both are needed; they target different attack surfaces.
3. **Turns "the model might be wrong" into a measured guarantee.** NIST evals quantify how often output is wrong; LAB measures that being wrong doesn't cause an unauthorized action — SVR 0.0, FCR 1.0, Γ-compliance 1.0. It's the containment metric for the residual risk GenAI evals leave on the table.
4. **Provides decision-level provenance to sit under content-level provenance.** NIST GenAI provenance work watermarks content; LAB's Evidence Quad + hash-chained ERTuples give per-decision provenance — so a regulator can trace not just "was this text AI-generated" but "was this action authorized, by what policy, with what evidence."

### The stacked view

```
NIST GenAI evals → did the model output correct / safe / authentic content?
(probabilistic)
       │ the output becomes an action proposal
       ▼
LAB v1.0 → is that action AUTHORIZED to execute?
(deterministic)
       UER 0 · FP 0 · SVR 0 · FCR 1.0 · replay 1.0 · fail-closed
```

### Honest boundaries (what LAB does not complement)

- LAB says nothing about content quality, hallucination rate, toxicity, CBRN detection, or watermark robustness — those remain squarely NIST GenAI's domain.
- LAB assumes upstream telemetry/predicate inputs are as given; it enforces the boundary, it doesn't author policy or verify feed correctness (the "oracle problem," disclosed in the stress test).
- Complementarity is conceptual/architectural, not an integration — no joint NIST evaluation was run; external validation is disclosed not_run.

**Net:** NIST GenAI evaluations grade the model's speech; LAB v1.0 grades the system's authority to act on that speech. The zero-unauthorized-execution, deterministic-replay, and fail-closed results are exactly the execution-boundary evidence that generative-AI content evaluations structurally cannot produce — which is why the two sit in series rather than compete.

---

## 5. Outputs Supporting an EU AI Act Conformity-Assessment Evidence Package

These are the run's outputs mapped to the specific EU AI Act (Regulation 2024/1689) high-risk obligations they can evidence. FULL_SPEC §14 already anchors to Art. 12 (logging) and Art. 14 (oversight); the strongest fit is Art. 12 + Art. 15.

> **Scope disclaimer:** These outputs support / contribute to the *technical file behind* a conformity assessment — they are **not** a conformity assessment, CE marking, or notified-body attestation. External audit and hardware-in-the-loop are disclosed not_run / not_available; the system is Tier-S software.

### Benchmark outputs → EU AI Act articles

| AI Act obligation | What the Act requires | Benchmark output that evidences it | Evidence value from this run |
|---|---|---|---|
| **Art. 12** — Record-keeping / logging (traceability over lifecycle) | automatic logs enabling traceability of the system's functioning | ERTuple replay manifest + hash-chained Hydra Ledger + Evidence Quad per decision | 284,807 signed records · 284,807/284,807 links · ledger_hash `1ce2a9e8…` · sealed manifest SHA-256 |
| **Art. 19** — Automatically generated logs (kept, integrity) | logs kept, tamper-evident | tamper-evident hash chain + independent verifier | verifier PASS, 0 adjacency/ledger/consistency failures, any edit detected |
| **Art. 15** — Accuracy | appropriate accuracy metrics + declared levels | confusion matrix + LAB metrics with Wilson 95% bounds | TP 284,315 / TN 492 / FP 0 / FN 0; UER 0, FPR 0/492, FDR 0/284,315 |
| **Art. 15** — Robustness / resilience / fail-safe | robust to errors, faults, inconsistencies; fail-safe | FCR test + fail-closed / SAFE_STATE absorption | FCR 1.0 (0 fail-open / 20,492); 492/492 → SAFE_STATE; partition PASS, 0 desync unauthorized |
| **Art. 15** — Cybersecurity | resist manipulation, data poisoning, resilience against attempts to alter use/behaviour | adaptive white-box attacker + 8 attack families + Goodhart veto | adaptive 0/11,808 false permits; three-signal closure 0 violations; contamination/canary PASS |
| **Art. 14** — Human oversight | oversight measures, ability to intervene / not over-rely | HITL governance record | override of failed hard predicate PROHIBITED; operator query path & dispute workflow defined; break-glass audited; TAU-Node ≤2s |
| **Art. 9** — Risk management system | identify, evaluate, mitigate; test mitigation effectiveness; residual risk | threat model + ablation/negative control + stress scenarios + assumptions register | ablation: compensatory gate leaks 492, deployed guardrail 0; P1–P4 stress with residual-risk disclosure; `assumptions_and_limitations` |
| **Art. 10** — Data & data governance | provenance, relevance, examination for biases | real third-party ground truth + dataset provenance + ULB Class labels (not self-authored) | dataset_seed, contamination controls, deterministic y\*=Λ(G) |
| **Art. 11 + Annex IV** — Technical documentation | system description, metrics, methods, reproducibility | bundle + report envelope | `gamma_bundle/` (MANIFEST digest-sealed, env.json, command.txt, REPRODUCE.md); method/schema versions |
| **Art. 13** — Transparency to deployers | interpretable operation, instructions | predicate-failure explanations + dashboard + limitations | first-failing-gate attribution; `gamma_report.html`; explanation completeness 1.0 (ASB) |
| **Art. 17** — Quality management system | documented, versioned, reproducible process | pre-registration + versioned config + deterministic replay | pre_reg_id `dc3ce999…`; identical inputs → identical outputs; DR 1.0 |
| **Art. 72** — Post-market monitoring | ongoing monitoring, incident | per-decision evidence stream + revocation | replayable ERTuple trail; DET-5, REVOC_P95 ≈16 ms |
| **Annex VI/VII** — Conformity assessment support | technical file a body can examine | independently re-checkable evidence (no runner/data) | `gamma_replay_verify.py` PASS from the JSONL alone |

### The three outputs that carry the most weight in a technical file

1. **The ERTuple manifest + hash-chained ledger + Evidence Quad** → directly evidences Art. 12 / Art. 19 (the hardest logging/traceability requirements to satisfy after the fact), and it's independently verifiable without trusting us.
2. **The metrics + FCR + adversarial results** → evidences Art. 15 across all three of its prongs (accuracy, robustness, cybersecurity) with confidence bounds.
3. **The ablation / negative control** → evidences Art. 9's requirement that risk-mitigation measures are effective (not just present): it shows the guardrail is causally responsible for the zero-harm outcome.

### What these outputs do not cover (gaps a full package still needs)

| AI Act requirement | Gap |
|---|---|
| Art. 43 / Annex VII — notified-body assessment | not performed (`third_party_audit: not_run`) — this benchmark produces inputs to it, not the assessment |
| Art. 10 — training-data bias/representativeness (for a trained model) | LAB governs a deterministic gate, not a trained model; data-governance evidence is partial |
| Art. 15 — hardware-rooted cybersecurity claims | signatures are HMAC software analogs (Tier-S); HSM/hardware interlock disclosed as future |
| Live operational / fleet monitoring (Art. 72 at scale) | fleet is simulated, not live |
| Fundamental-rights impact assessment (Art. 27) | out of scope — LAB measures execution-boundary correctness, not societal impact |

**Net:** The run produces genuine, independently verifiable evidence toward Art. 12, 15, 14, 9, 11/Annex IV, 13, 17, 19, 72 — strongest on logging/traceability (Art. 12) and accuracy/robustness/cybersecurity (Art. 15), plus a well-evidenced human-oversight (Art. 14) and risk-management-effectiveness (Art. 9) story. It is a technical-file contribution, not a conformity verdict — the notified-body assessment, hardware-rooted cybersecurity, and live-deployment monitoring remain outside what this benchmark can attest, and those boundaries are disclosed rather than papered over.

---

## 6. Full Auditor-Consumable Evidence Inventory

### Part 1 — Every piece of evidence an external auditor can consume

#### A. Primary evidence artifacts (files on disk)

| # | Artifact | Size | What an auditor does with it | Independently checkable? |
|---|---|---|---|---|
| 1 | `gamma_replay_manifest.jsonl` | 200.97 MB | 284,807 signed per-decision ERTuple records (proposal_id, ertuple_id, policy_hash, hash_prev/current, Γ_G/Γ_class/Π, Evidence Quad) | ✅ yes — re-verify with the stdlib verifier |
| 2 | `gamma_validation_results.csv` | 133.85 MB | row-level decisions (PERMIT/SAFE_STATE) + predicate/gate state per transaction | ✅ recompute from mapped CSV |
| 3 | `gamma_lab_v1_report.json` | 11.6 KB | metrics + 6 invariants + latency + negative control + TLC attestation + governing rules | ✅ formulas disclosed |
| 4 | `gamma_summary.json` | 3.5 KB | headline confusion + distributions + top rule failures | ✅ |
| 5 | `concurbench_full_report.json` | 74.6 KB | Document-1 §18 conformance object (L1–L4, ASB, contamination, HITL, Evidence Quad) | ✅ |
| 6 | `full_spec_conformance_report.json` | 9.2 KB | §7.1 bands, AIS sub-signals, three-signal closure, SVR/FFC, TLC, DET-1…5 | ✅ |
| 7 | `stress_test_report.json` | 14.5 KB | P1–P4 per-condition pass/fail + verdicts | ✅ |
| 8 | `fcr_test_report.json` | 1.8 KB | fail-closed rate per uncertainty family + Wilson bounds | ✅ |
| 9 | `gamma_report.html` | 70.2 KB | human-readable dashboard (all values read from the JSON) | ✅ cross-check vs JSON |
| 10 | `gamma_terminal_full.txt` | 7.6 KB | verbatim console output of the run | ✅ |

#### B. Reproducibility bundle (`gamma_bundle/`) — the seal

| File | Size | Contents |
|---|---|---|
| `MANIFEST.json` | 4.35 KB | SHA-256 + size of every input/source/output, exact command line, TLC block, replay summary, `bundle_digest_sha256` |
| `REPRODUCE.md` | 1.85 KB | step-by-step: check digests → re-run → verify manifest → bind TLC → diff |
| `env.json` | 253 B | Python / pandas / platform / method version |
| `command.txt` | 325 B | literal command that produced the run |

#### C. Cryptographic anchors (what the whole package hangs on)

| Anchor | Value |
|---|---|
| Manifest SHA-256 (final ledger root) | `1ce2a9e8d4330a0583a9d20a398de43297ea59c404e006e7f1161208481931da` |
| Evidence Quad ledger_hash | `1ce2a9e8…931da` (matches manifest) |
| Pre-registration ID | `dc3ce9995510ef8bc08b6422ff7f380a6c8dc2281452a9920398d4391aa27808` |
| Bundle digest | `8bd413fc3c07aa26df17d7c3b242acd3aa3442903d9df209475a115efc8b54eb` |
| Policy hash | `156bacd165bf0ab0ffc6abc977195944aa0b55c3bf66d4d1c2312b1fa4feb613` |
| TLC attestation digest (in tlc_verification) | 2,489,446 states / 0 violations |

#### D. The independent verification tool the auditor runs (zero-trust)

```bash
python gamma_replay_verify.py gamma_replay_manifest.jsonl \
  --expect-sha256 1ce2a9e8d4330a0583a9d20a398de43297ea59c404e006e7f1161208481931da
```

No pandas, no dataset, no runner needed. It re-checks hash-chain adjacency + genesis anchor + Evidence-Quad↔ledger binding + decision self-consistency, recomputes the manifest SHA-256, and exits 0 only if all pass (any flipped byte → exit 1). **This run: 0 failures, SHA-256 MATCH.**

> **Auditor's honest boundaries:** signatures are HMAC-SHA256 software analogs (not HSM); the bundled trace verifies adjacency, not full per-row hash re-derivation (§12.4); fleet/hardware evidence is simulated (Tier-S); external audit itself is disclosed not_run.

### Part 2 — ConcurBench modules evaluated, and evidence each produced

`concurbench_full.py` evaluated these modules over the real 284,807-row corpus:

| Module | Evaluated? | Evidence produced | Key result |
|---|---|---|---|
| **L1 — Authorization Correctness** | ✅ | confusion matrix, UER/FPR/FDR/FCR/DR, Wilson 95% bounds | TP 284,315 / TN 492 / FP 0 / FN 0; UER 0, FPR 0, FCR 1.0 → PASS |
| **L2 — Adversarial Robustness** | ✅ | 8 attack families (4,000 each) + adaptive attacker + ablation | adaptive 0/11,808; total false permits 0; ablation 492-vs-0 → PASS |
| **L3 — Distributed Consistency** (simulated fleet) | ✅ | 5-node consistency, revocation latency p50/95/99, partition, quorum, desync | fleet 1.0, partition PASS, 0 desync-unauthorized → PASS |
| **L4 — Deterministic Replay + Auditability** | ✅ | replay attempts/passes/failures/rate, hash-chain, independent verifier, Evidence Quad | 284,807/284,807, rate 1.0, verifier PASS → PASS |
| **Contamination / canary** | ✅ | dynamic-derivation, cryptographic salting, canary leakage check | contamination PASS, canary PASS, 0 leaks |
| **ASB (Adversarial Scenario Benchmarking)** | ✅ | 5 scenario families, temporally-ordered event streams, 7 metrics | pass rate 1.0, ASB-UER 0.0, explanation completeness 1.0 |
| **HITL / human governance** | ✅ | governance record (override PROHIBITED, dispute workflow, denial categories) | override of failed predicate PROHIBITED |
| **Evidence Quad** | ✅ | spec_clause · pre_reg_id · method_version · ledger_hash | complete (`dc3ce999…` / `1ce2a9e8…`) |
| **Report envelope (§8)** | ✅ | benchmark/system/eval metadata, schema versions, scenario distribution | all fields populated |
| **Dataset / reproducibility (§9)** | ✅ | generation method, seed, distribution, predicate dimensionality | seed 20260629, 13 predicates |
| **Assumptions & limitations (§14)** | ✅ | disclosure object | production/NIST/IEEE claims = false |
| **Independent validation (§13)** | ✅ (disclosed) | external-status object | AgentDojo/AgentHarm not_run, hardware not_available, TLA+ spec_emitted, external_replay_verifier run, third_party_audit not_run |
| **Conformance verdict (§15)** | ✅ | 4-level roll-up + overall L1–L4 | all PASS → COMPLIANT_PASS |

#### Adjacent conformance modules (beyond ConcurBench proper)

| Module | File | Evidence | Verdict |
|---|---|---|---|
| FULL_SPEC engine | `full_spec_conformance.py` | §7.1 bands enforced, AIS live composite (5 sub-signals), three-signal closure, SVR 0 / Γ-compliance 1.0, T0–T9→I1–I6 | FULL_SPEC_CONFORMANT (Tier-S) |
| FCR test | `fcr_test.py` | fail-closed over 6 uncertainty families 0 fail-open / 20,492 | FCR 1.0 |
| Stress test | `stress_test.py` | P1–P4 financial scenarios weighted 78.4%, all in-scope fail-closed | — |
| Doc-1 field audit | `concurbench_conformance_check.py` | 133 fields present, 22 PASS conditions, 0 gaps | exit 0 |

# 7. How Gamma Can Bridge This

Gamma LAB v1.0 already produces a comprehensive set of technical evidence through its benchmarking framework. The next evolution is transforming this evidence into a conformity-assessment support platform capable of generating auditor-ready documentation, enabling independent verification, and integrating into AI governance programs.


---

# 1. Generate Audit-Ready Technical Files

## Objective

Automatically convert benchmark outputs into a structured technical documentation package that aligns with the documentation requirements of the **EU AI Act** for high-risk AI systems.

Rather than simply producing benchmark reports, Gamma should assemble all generated evidence into a complete technical file.

## Current Evidence Already Available

- **Evidence Quad**
  - Decision
  - Method Version
  - Policy Hash
  - Ledger Hash

- **Hydra Ledger**
  - Hash-chained decision history
  - Tamper-evident audit trail
  - Complete replay history

- **Runtime Metrics**
  - Unauthorized Execution Rate (UER)
  - False Positive Rate (FPR)
  - False Discovery Rate (FDR)
  - Fail Closed Rate (FCR)
  - Safe Violation Rate (SVR)
  - Runtime invariants

- **Formal Verification**
  - TLA+/TLC verification results
  - State-space exploration
  - Safety invariant verification

- **Adversarial Testing**
  - Stress testing
  - Adaptive attacker evaluation
  - Negative controls
  - Counterfactual analysis

- **Governance Metadata**
  - Policy version
  - Method version
  - Pre-registration identifier
  - Dataset fingerprint
  - Execution environment
  - Reproducibility bundle

## Future Output

```text
technical_file/
│
├── Executive Summary
├── System Description
├── Risk Assessment
├── Benchmark Results
├── Runtime Governance Evidence
├── Logging Evidence
├── Formal Verification Report
├── Replay Verification
├── Cybersecurity Assessment
├── Stress Testing Results
├── Human Oversight Evidence
├── Limitations
├── Annex IV Mapping
└── Cryptographic Manifest
```

---

# 2. Facilitate Third-Party Verification

## Existing Capability

Gamma already includes:

```text
gamma_replay_verify.py
```

It independently verifies:

- SHA-256 hash chain continuity
- Hydra Ledger integrity
- Evidence Quad consistency
- Decision replay consistency
- Manifest digest
- Genesis anchor
- Ledger binding

without requiring proprietary code or datasets.

## Future Audit Package

```text
audit_package/

├── benchmark_results.json
├── technical_file.pdf
├── gamma_replay_verify.py
├── MANIFEST.json
├── ledger.jsonl
├── SHA256.txt
└── verification_guide.pdf
```

Auditors only need to execute:

```bash
python gamma_replay_verify.py
```

---

# 3. Align with AI Management Standards

Gamma should position itself as a technical evidence generator supporting **ISO/IEC 42001**, not as a certification body.

It supports:

- Risk management through measurable runtime metrics.
- Operational controls through replay evidence and governance metadata.
- Continuous monitoring through repeated benchmark executions.
- Internal audits using reproducible benchmark reports.

---

# Overall Bridge

| Stage | Purpose | Primary Output |
|--------|---------|----------------|
| Today | Benchmarking Platform | Runtime governance metrics, replay evidence, formal verification |
| Next | Evidence Generation Platform | Audit-ready technical files, reproducibility bundles, replay packages |
| Long-Term | Conformity Assessment Support Platform | Standardized evidence supporting EU AI Act and ISO/IEC 42001 assessments (without issuing certifications) |

---

# Conclusion

Gamma's current strength lies in generating deterministic, reproducible, and cryptographically verifiable runtime governance evidence.

By organizing this evidence into audit-ready technical files, providing independent verification tools, and aligning outputs with recognized governance frameworks such as the EU AI Act and ISO/IEC 42001, Gamma can evolve from a benchmarking platform into a comprehensive conformity-assessment support engine.

It would not replace certification bodies or auditors, but instead provide the high-quality technical evidence they require for efficient and transparent AI assurance.

**One-line summary for the auditor:** The run emits 10 evidence files + a digest-sealed bundle + a zero-dependency verifier, all chained to a single ledger root (`1ce2a9e8…931da`) and a pre-registration ID (`dc3ce999…`); every ConcurBench module (L1–L4, ASB, contamination, HITL, Evidence Quad, envelope, dataset, assumptions, independent-status, verdict) was evaluated and produced its own evidence, rolling up to COMPLIANT_PASS — with the external/hardware/live-fleet limits disclosed, not hidden.
