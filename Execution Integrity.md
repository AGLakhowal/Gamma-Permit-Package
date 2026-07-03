# Execution Integrity

**A Runtime Governance Evaluation Framework**

ConcurBench · Adversarial Scenario Benchmarking · LAB v1.0

*Standards Alignment & Benchmark Architecture*

Prepared by Gillian Holdings Incorporated
Version 1.0 · July 2026

---

## Contents

1. [Executive Summary](#1-executive-summary)
2. [The Execution Integrity Stack](#2-the-execution-integrity-stack)
3. [Standards Alignment & Regulatory Positioning](#3-standards-alignment--regulatory-positioning)
4. [The Execution Integrity Evaluation Framework](#4-the-execution-integrity-evaluation-framework)
5. [ConcurBench Benchmark Architecture](#5-concurbench-benchmark-architecture)
6. [Relationship Between the Modules](#6-relationship-between-the-modules)
7. [Adversarial Scenario Benchmarking (ASB)](#7-adversarial-scenario-benchmarking-asb)
8. [Maturity Notes & Open Items](#8-maturity-notes--open-items)
9. [Integrated Positioning](#9-integrated-positioning)

---

## 1. Executive Summary

Most AI evaluation measures what a model can *generate* — the believability of its text, the reliability of its code, the quality of its output. **Execution Integrity** measures something different and downstream: whether a system with the power to take *externally effective actions* executes only those actions it is actually authorized to take. It is the governance layer that sits after generation and before consequence.

This document defines Execution Integrity as a measurement construct and describes the two evaluation methodologies that operationalize it — **ConcurBench**, a controlled and reproducible benchmark, and **Adversarial Scenario Benchmarking (ASB)**, a real-world adversarial framework. It then describes **LAB v1.0**, the reference implementation that produces the measurable evidence these methodologies define.

> **Positioning at a glance**
>
> LAB v1.0 is an implementation artifact, not a regulatory standard, certification scheme, or conformity assessment. It produces structured technical evidence that can support AI governance, risk management, audit preparation, and future conformity-assessment activities — but does not, on its own, constitute regulatory approval, certification, or endorsement by any standards body.

---

## 2. The Execution Integrity Stack

The framework is best understood as four distinct levels, each answering a different question. Conflating them is the most common source of confusion, so the hierarchy is stated explicitly before anything else.

![The four-level Execution Integrity stack, from measurement construct to implementation artifact]<img width="1600" height="992" alt="figure1-execution-integrity-stack" src="https://github.com/user-attachments/assets/33b033fc-3826-4132-a283-3f46fb6acef1" />

*Figure 1 — The four-level Execution Integrity stack, from measurement construct to implementation artifact.*

| Level | Name | Role |
|---|---|---|
| Construct | **Execution Integrity** | Defines what is measured: whether only authorized actions execute. |
| Methodology | ConcurBench | Defines how EI is measured under controlled, reproducible conditions. |
| Methodology | ASB | Defines how EI is stress-tested under realistic, temporally extended adversarial conditions. |
| Artifact | **LAB v1.0** | The reference implementation that runs the evaluations and emits measurable evidence. |

---

## 3. Standards Alignment & Regulatory Positioning

LAB v1.0 aligns with emerging AI governance frameworks by producing deterministic authorization decisions, replayable audit evidence, adversarial evaluation results, and execution-boundary metrics. The alignment described below is *evidentiary*, not certificatory: the framework generates artifacts that may feed governance processes, and nothing in this section should be read as participation in, or endorsement by, the named bodies.

### 3.1 NIST AI RMF 1.0

The NIST AI Risk Management Framework is organized around four core functions. Execution Integrity evidence maps to each of them as follows.

| RMF Function | Execution Integrity Evidence |
|---|---|
| **Govern** | Runtime authorization policies, governance rules, and retained audit evidence. |
| **Map** | Threat model, catalogue of externally effective actions, and predicate definitions. |
| **Measure** | UER, FPR, FDR, replay determinism, latency, and Gamma compliance. |
| **Manage** | SAFE_STATE transitions, fail-closed execution, and replay verification. |

### 3.2 NIST ARIA

LAB v1.0 is conceptually aligned with NIST ARIA in that both emphasize measurable AI behavior under realistic risk conditions. ARIA assesses the risks and impacts of AI systems once deployed — validity, reliability, safety, security, privacy, and fairness. LAB v1.0 contributes a narrower execution-boundary layer: whether externally effective actions are authorized, auditable, replayable, and fail closed. **This is conceptual alignment only, developed independently of the ARIA program, and should not be interpreted as NIST endorsement, approval, or certification.**

### 3.3 NIST Generative AI Evaluations

NIST GenAI evaluations focus on generative capability and its limits — text believability, image indistinguishability, code reliability. LAB v1.0 is complementary rather than competing: it measures what happens after generation, namely whether a proposed action is permitted, denied, replayable, and auditable before it executes.

### 3.4 EU AI Act

LAB v1.0 can generate technical evidence relevant to high-risk AI governance obligations under the EU AI Act — particularly where systems require risk controls, logging, traceability, human-oversight support, robustness, and cybersecurity evidence. Article 43 concerns conformity-assessment procedures for high-risk systems; LAB v1.0 evidence may support such a package but **does not itself constitute a conformity assessment.**

**Future Harmonised Standards.** Benchmark outputs are designed to be mappable to emerging European harmonised AI standards supporting the EU AI Act, including evidence for risk management, technical documentation, logging, transparency, human oversight, robustness, accuracy, and cybersecurity.

**External Validation.** Future versions of LAB v1.0 may be evaluated within AI Testing and Experimentation Facilities (TEFs), third-party benchmark environments, or enterprise pilot deployments to obtain independent validation under real deployment conditions.

### 3.5 Standards Positioning Summary

| Framework | Relationship |
|---|---|
| NIST AI RMF 1.0 | Runtime governance evidence mapped to Govern, Map, Measure, and Manage. |
| NIST ARIA | Conceptually aligned with adversarial and deployed-risk evaluation philosophy; independent of the ARIA program. |
| NIST GenAI Evaluations | Complementary evaluation layer applied after model generation. |
| EU AI Act (Art. 43) | Technical evidence that may support conformity-assessment activities; not itself an assessment. |
| EU Harmonised Standards | Benchmark outputs mappable to emerging AI governance requirements. |
| AI Testing & Experimentation Facilities | Prospective environment for future independent validation. |

> **A note on NIST agent-standards activity**
>
> Where earlier drafts referenced a "proposed" construct within a NIST AI agent-standards initiative, this version states the relationship conservatively: the construct is potentially relevant to such activity. Absent a docket number or acknowledged submission, no claim of formal proposal or participation is made.

---

## 4. The Execution Integrity Evaluation Framework

Execution Integrity is the primary measurement construct for AI systems capable of externally effective actions: it measures whether a system executes only those actions authorized under defined evaluation conditions. It is operationalized through two complementary methodologies.

- **ConcurBench** — a controlled, reproducible benchmark for execution-boundary correctness.
- **Adversarial Scenario Benchmarking (ASB)** — a real-world adversarial framework for temporally extended operational conditions.

Together they provide measurable evidence of runtime authorization correctness, robustness, replayability, auditability, and distributed consistency. ConcurBench establishes what is true under laboratory control; ASB establishes whether those same invariants survive contact with realistic adversaries.

![Two evaluation lanes converge into a single LAB v1.0 evidence package that may support downstream governance frameworks]<img width="1600" height="896" alt="figure2-evidence-package" src="https://github.com/user-attachments/assets/8b3c359d-7ad7-4a33-bd36-ce9cdb1099dd" />

*Figure 2 — Two evaluation lanes converge into a single LAB v1.0 evidence package that may support downstream governance frameworks.*

---

## 5. ConcurBench Benchmark Architecture

ConcurBench is a modular execution-boundary benchmark. Rather than measuring model capability, it evaluates whether a runtime governance layer correctly authorizes, records, and coordinates externally effective actions. It is structured as four progressively stronger modules, each evaluating a distinct property while building on the guarantees of those beneath it:

> Authorization Correctness → Adversarial Robustness → Replay & Auditability → Distributed Consistency

The ordering reflects a genuine dependency, not mere presentation. Deterministic replay has little value if the underlying authorization decision is wrong, and distributed consistency is meaningful only once single-node authorization, robustness, and replay have each been demonstrated.

![The cumulative assurance hierarchy. Higher modules assume the guarantees established below them]<img width="1600" height="1024" alt="figure3-assurance-hierarchy" src="https://github.com/user-attachments/assets/88fb25f6-7733-4384-9207-940b6ea29550" />

*Figure 3 — The cumulative assurance hierarchy. Higher modules assume the guarantees established below them.*

### 5.1 Module 1 — Authorization Correctness

**Purpose.** Module 1 evaluates whether the runtime authorization engine consistently makes correct permit and deny decisions according to the Gamma authorization model.

> **Core question:** Does the runtime permit only authorized actions and deny every unauthorized action?

**Primary measurements**

| Metric | Purpose |
|---|---|
| **Unauthorized Execution Rate (UER)** | Measures unauthorized executions that slipped through. |
| **False Permit Rate (FPR)** | Measures incorrect authorizations. |
| **False Denial Rate (FDR)** | Measures unnecessary denials of legitimate actions. |
| **Gamma Compliance** | Confirms every request with Γ > 0 is denied. |
| **Class-Veto Effectiveness** | Confirms prohibited classes remain blocked. |
| **TOCTOU Violations** | Confirms authorization remains valid through actuation. |

**Outcome.** Establishes authorization correctness at the execution boundary.

### 5.2 Module 2 — Adversarial & Fail-Closed Robustness

**Purpose.** Module 2 evaluates whether the Module 1 guarantees remain valid when the system faces uncertainty, adversarial manipulation, incomplete information, stale context, corrupted inputs, or runtime faults.

> **Core question:** Does the system continue to fail safely when operating under attack or uncertainty?

**Primary measurements**

| Metric | Purpose |
|---|---|
| **Fail-Closed Rate (FCR)** | Measures SAFE_STATE behavior under uncertainty. |
| **Adaptive Attacker Success** | Measures whether mutation strategies create false permits. |
| **PR_LCB Robustness** | Evaluates robustness-threshold behavior under a lower-confidence bound. |
| **Ablation Leakage** | Measures whether removing a safety control creates false permits. |
| **Controlled Adversarial Coverage** | Evaluates realistic attack scenarios under controlled conditions. |

**Outcome.** Demonstrates that authorization correctness is preserved under adverse operating conditions.

### 5.3 Module 3 — Replay & Audit Integrity

**Purpose.** Module 3 evaluates whether every authorization decision can be reconstructed, independently verified, and reproduced from recorded evidence.

> **Core question:** Can every authorization decision be replayed, verified, and audited deterministically?

**Primary measurements**

| Metric | Purpose |
|---|---|
| **Determinism Rate (DR)** | Measures identical replay outcomes across repeated runs. |
| **Replay Consistency Rate** | Confirms identical inputs produce identical decisions. |
| **Hash-Chain Continuity** | Verifies integrity of the decision ledger. |
| **ERTuple Completeness** | Verifies that each decision carries complete evidence. |
| **Independent Replay Verification** | Confirms replay pass/fail by a verifier independent of the runtime that produced the record. |

**Outcome.** Establishes deterministic auditability and replayable governance evidence.

### 5.4 Module 4 — Distributed Runtime Consistency

**Purpose.** Module 4 extends the benchmark beyond a single runtime instance to evaluate whether authorization remains consistent across multiple nodes operating as a coordinated deployment.

> **Core question:** Does runtime authorization remain correct across a distributed deployment?

**Primary measurements**

| Metric | Purpose |
|---|---|
| **Fleet Consistency** | Confirms identical authorization decisions across nodes. |
| **Cross-Node Replay Consistency** | Verifies replay equivalence throughout the fleet. |
| **Revocation Latency** | Measures propagation time for authorization revocations. |
| **Partition Safety** | Confirms no unauthorized execution during network partitions or split-brain conditions. |
| **Policy-Version Consistency** | Confirms identical policy enforcement across all nodes. |

**Outcome.** Establishes distributed execution integrity and federation readiness.

---

## 6. Relationship Between the Modules

The four modules are cumulative rather than independent. Each establishes a property and, in doing so, enables the assurance argument of the next.

| Module | Establishes | Enables |
|---|---|---|
| Module 1 | Correct authorization decisions | Safe runtime control |
| Module 2 | Robust authorization under attack and uncertainty | Trustworthy operational deployment |
| Module 3 | Deterministic replay and audit evidence | Independent verification and compliance evidence |
| Module 4 | Consistent authorization across distributed systems | Enterprise federation and large-scale deployment |

Read as a single argument: **Module 1** proves decisions are correct; **Module 2** proves they remain correct under adverse conditions; **Module 3** proves every decision can be independently verified; and **Module 4** proves those guarantees hold consistently across an enterprise fleet.

---

## 7. Adversarial Scenario Benchmarking (ASB)

ASB complements ConcurBench by evaluating Execution Integrity under realistic, temporally extended operational conditions. Where ConcurBench measures correctness under controlled benchmark conditions, ASB asks whether the same execution-boundary invariants are preserved when the environment turns hostile over time. Its scenario families are:

- **Identity and provenance deception** — forged or spoofed actor identity and action origin.
- **Runtime infrastructure drift** — gradual divergence of the runtime environment from its verified baseline.
- **Economic logic fragility** — exploitation of brittle value or incentive assumptions.
- **Cross-entity fraud propagation** — abuse that spreads across trust boundaries between entities.
- **Session or intent compromise** — hijacking of an authorized session or subversion of established intent.

ASB therefore extends benchmark validation from controlled execution to real-world operational resilience — the bridge between a passing lab result and a system that can be trusted in deployment.

---

## 8. Maturity Notes & Open Items

Two items are called out explicitly so that readers can calibrate the current maturity of the framework. Neither undermines the architecture; both are the natural next steps in moving from a metric catalogue to a fully specified benchmark.

### 8.1 Pass/fail thresholds

The modules define what is measured (UER, FPR, FDR, FCR, DR, and the rest) but do not yet fix the numeric acceptance criteria for each. A complete benchmark specifies target values — for example, whether acceptable UER is zero or a bounded non-zero rate — together with the sample sizes and confidence intervals under which those targets are judged. Establishing and publishing these thresholds is the primary open item.

### 8.2 Baseline and comparison conditions

Reported metrics are most meaningful against a reference. Future revisions should include an ungoverned or minimally governed control condition so that each score can be read relative to a baseline rather than in isolation, making the governance layer's contribution quantifiable.

---

## 9. Integrated Positioning

| Element | Role in the framework |
|---|---|
| **Execution Integrity** | Provides the measurement construct — what is being measured. |
| **ConcurBench** | Provides the controlled benchmark methodology. |
| **ASB** | Provides the real-world adversarial evaluation methodology. |
| **LAB v1.0** | Provides the implementation artifact and evidence-producing benchmark run. |

Together, these elements generate structured runtime evidence that can support governance, risk management, audit preparation, product validation, enterprise assurance, and future conformity-assessment activities. The framework measures not merely what an AI system *can generate*, but whether it is *authorized to execute* externally effective actions safely, deterministically, and auditably.

> **Closing positioning statement**
>
> Execution Integrity does not replace existing AI governance frameworks. It complements them by producing measurable execution-boundary evidence. While many AI evaluations focus on model capability or output quality, this framework measures whether externally effective actions are authorized, replayable, auditable, and fail closed under uncertainty. That evidence can support governance activities under frameworks such as NIST AI RMF 1.0 and the EU AI Act — but it does not constitute regulatory approval, certification, endorsement, or formal standards compliance on its own.
