# Gamma Runtime Governance Engine — Full Specification

**Document:** `FULL_SPEC.md`
**Standard:** G-0 Runtime Governance Standard, v1.0
**Companion to:** [`README.md`](README.md)
**Author:** Abhinandan Gill-Lakhowal
**Status:** Reference Specification (Architect-Level)

-----

> This specification describes the architecture, invariants, predicate semantics, permit mechanics, audit format, failure behaviour, and integration patterns of the Gamma Runtime Governance Engine. Formal mathematical proofs for the Lakhowal Law of Concurrence and the associated invariants are deferred to a separate companion document (`PROOFS.md`, forthcoming). This document is the canonical architect-level reference — sufficient to implement, evaluate, and procure a conforming deployment without reading the proof apparatus.

-----

# Table of Contents

- [Part I — Foundations and Design Philosophy](#part-i--foundations-and-design-philosophy)
  - [1. Scope and Intended Audience](#1-scope-and-intended-audience)
  - [2. Problem Statement — The Execution Gap](#2-problem-statement--the-execution-gap)
  - [3. Design Principles](#3-design-principles)
  - [4. Threat Model and Adversary Assumptions](#4-threat-model-and-adversary-assumptions)
  - [5. Notation and Terminology](#5-notation-and-terminology)
- [Part II — Architectural Invariants](#part-ii--architectural-invariants)
  - [6. The Five Invariants of G-0](#6-the-five-invariants-of-g-0)
  - [7. The Lakhowal Law of Concurrence (Informal Statement)](#7-the-lakhowal-law-of-concurrence-informal-statement)
  - [8. Non-Compensatory Evaluation](#8-non-compensatory-evaluation)
  - [9. Temporal Semantics and TOCTOU](#9-temporal-semantics-and-toctou)
- [Part III — The G-0 Stack](#part-iii--the-g-0-stack)
  - [10. Layer 1 — Orchestration Plane](#10-layer-1--orchestration-plane)
  - [11. Layer 2 — Control Plane](#11-layer-2--control-plane)
  - [12. Layer 3 — Boundary Layer](#12-layer-3--boundary-layer)
  - [13. Layer 4 — Audit Plane and the Hydra Ledger](#13-layer-4--audit-plane-and-the-hydra-ledger)
  - [14. Layer 5 — Formal Specification Layer](#14-layer-5--formal-specification-layer)
- [Part IV — Predicates, Permits, and the Execution Gateway](#part-iv--predicates-permits-and-the-execution-gateway)
  - [15. Predicate Algebra (Informal)](#15-predicate-algebra-informal)
  - [16. The Gamma Permit — Format and Lifecycle](#16-the-gamma-permit--format-and-lifecycle)
  - [17. Reference Implementation — The Execution Gateway](#17-reference-implementation--the-execution-gateway)
  - [18. The Dual Permission Model — Act vs. Adapt](#18-the-dual-permission-model--act-vs-adapt)
- [Part V — Audit Evidence Model](#part-v--audit-evidence-model)
  - [19. ERTuple — Structure and Semantics](#19-ertuple--structure-and-semantics)
  - [20. Hash-Linked Ledger Semantics](#20-hash-linked-ledger-semantics)
  - [21. Replayability and Regulatory Mapping](#21-replayability-and-regulatory-mapping)
- [Part VI — The Operational Continuity Layer](#part-vi--the-operational-continuity-layer)
  - [22. The Fail-Closed Trap and Its Resolution](#22-the-fail-closed-trap-and-its-resolution)
  - [23. The Precedence Hierarchy](#23-the-precedence-hierarchy)
  - [24. Degradation Modes in Practice](#24-degradation-modes-in-practice)
- [Part VII — Governance Telemetry](#part-vii--governance-telemetry)
  - [25. The Governance Telemetry Layer (GTL)](#25-the-governance-telemetry-layer-gtl)
  - [26. Board-Reportable Metrics](#26-board-reportable-metrics)
- [Part VIII — Human Concurrence](#part-viii--human-concurrence)
  - [27. The Tactical Approval Unit (TAU)](#27-the-tactical-approval-unit-tau)
  - [28. Escalation Conditions](#28-escalation-conditions)
- [Part IX — Deployment Patterns](#part-ix--deployment-patterns)
  - [29. Reference Deployment Topology](#29-reference-deployment-topology)
  - [30. Integration with Existing Control Planes](#30-integration-with-existing-control-planes)
  - [31. Low-Code and No-Code Deployment](#31-low-code-and-no-code-deployment)
- [Part X — Conformance, Certification, and Governance](#part-x--conformance-certification-and-governance)
  - [32. Conformance Levels](#32-conformance-levels)
  - [33. Regulatory and Standards Mapping](#33-regulatory-and-standards-mapping)
  - [34. Versioning and Change Control](#34-versioning-and-change-control)
- [Appendix A — Glossary](#appendix-a--glossary)
- [Appendix B — Symbol Index](#appendix-b--symbol-index)

-----

# Part I — Foundations and Design Philosophy

## 1. Scope and Intended Audience

This specification defines the architecture and behaviour of a **runtime governance boundary** for AI systems that take externally effective actions — that is, actions whose effect persists outside the AI system itself. Externally effective actions include, but are not limited to: financial transactions, medical orders, infrastructure modifications, outbound communications, database writes, network control plane changes, and commands dispatched to cyber-physical systems.

The intended audience is:

- **Enterprise architects** designing the governance posture for agentic AI deployments.
- **CISOs and CROs** evaluating runtime controls against NIST AI RMF, ISO/IEC 42001, the EU AI Act, and the OWASP Top 10 for Agentic Applications.
- **Standards-body reviewers** assessing G-0 as a candidate for formal standardisation.
- **Procurement leads** drafting RFP language that distinguishes advisory AI from governed AI.
- **Research engineers** building or auditing conforming implementations.

The specification is deliberately architect-level. It states invariants and interfaces; it does not prescribe implementation choices that would foreclose valid deployments. Where a design choice is normative, it is marked **MUST**. Where it is recommended, it is marked **SHOULD**. Where it is optional, it is marked **MAY**. Informative commentary is rendered in ordinary prose.

## 2. Problem Statement — The Execution Gap

Contemporary AI systems are deployed across a spectrum of autonomy. At one end, a model produces advisory text that a human reads and acts on. At the other end, an autonomous agent chains tool calls, writes to production systems, dispatches payments, and modifies infrastructure with no human in the path. The industry has tooling for the first case. It has almost nothing for the second.

The gap is not a shortage of guardrails on model outputs. Output filters, constitutional prompts, refusal classifiers, retrieval grounding, policy overlays — these all govern what the model *says*. The execution gap is the absence of a deterministic boundary between what the model says and what the enterprise *does*. When an agent invokes a tool, the tool runs. When it issues an API call, the API responds. The agent’s output *is* the action.

This arrangement is tolerable when the action is reversible, cheap, and observable. It is not tolerable when the action is irreversible, expensive, or invisible until damage has propagated. A hallucinated trade, a prompt-injected remediation script, a stale-context medical order, a confidently wrong refund — in each case the failure mode is not that the model was misaligned in some philosophical sense. The failure mode is that a probabilistic reasoner had direct execution authority over a deterministic system.

The Gamma Runtime Governance Engine is a proposed control for precisely this mismatch. It does not make the model safer. It removes the model’s authority to execute and replaces it with a deterministic evaluator that issues cryptographic permits only when a defined set of predicates is satisfied.

## 3. Design Principles

Five principles shape every element of the specification.

**Capability is not authority.** An AI system generates proposals. Proposals carry no execution power. Authority is issued externally, by a component the AI cannot modify or persuade, and only when predicates evaluate cleanly.

**Non-compensation.** A governance decision is not an average. Satisfying nine predicates does not compensate for failing the tenth. A single failed predicate denies the action. This is architectural cowardice by design — it refuses to trade safety for performance.

**Fail-closed.** When the governance layer itself is uncertain — missing inputs, stale context, partitioned state — the default is denial. Availability of the agent is never permitted to outrank integrity of authorisation. The Operational Continuity Layer (Part VI) ensures that fail-closed does not mean fail-paralysed.

**Proof before action.** Every permitted action, and every denied one, produces an immutable audit record *before* the action is attempted. A system that logs after the fact cannot prove what was authorised; it can only describe what happened.

**Boundary, not policy.** Gamma is an engineering boundary, not a policy framework. Policy is an input to the boundary. Policy changes frequently and politically; the boundary does not. The boundary enforces whatever policy is loaded — consistently, deterministically, and independently of the AI’s reasoning.

## 4. Threat Model and Adversary Assumptions

The G-0 Standard assumes a realistic adversary, not a worst-case cryptographic one. Specifically, it assumes:

- **The AI model may be compromised, poisoned, hallucinating, or prompt-injected.** Any proposal originating from the capability plane is treated as untrusted input, not as a trusted command.
- **Inputs to the AI model may be adversarial.** Retrieval sources, user messages, tool responses, and inter-agent messages may contain content designed to redirect the model’s goals. The boundary does not attempt to detect this; it assumes it has already happened.
- **The AI system may attempt to self-ratify.** An agent may generate a proposal and a plausible justification simultaneously. The boundary evaluates predicates independently of any justification the model produces.
- **Operators may make errors.** Policy misconfiguration, stale allow-lists, and expired credentials are expected. Temporal Validity Enforcement (see §24) bounds the damage.
- **Infrastructure may degrade.** APIs fail, networks partition, clocks drift, consensus stalls. The continuity layer governs behaviour under degradation.

Out of scope for this specification:

- **Physical-layer attacks** against the hardware hosting the boundary. These are assumed to be addressed by conventional datacentre and hardware-security controls.
- **Cryptographic primitives themselves.** The specification uses standard asymmetric signing, hash functions, and signed timestamps; choice of concrete algorithm (e.g., Ed25519 vs. ECDSA P-256) is an implementation concern.
- **Insider threats against the signing key.** The key-management architecture is addressed at the deployment level and is informatively discussed in §29.

## 5. Notation and Terminology

The specification uses a small set of symbols consistently. A complete index is in [Appendix B](#appendix-b--symbol-index); the following are the most important.

|Symbol            |Meaning                                                                                                                                                                                                                  |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`Γ`               |The Gamma state — a binary value representing whether all governance predicates are satisfied at the moment of evaluation. `Γ = 0` denotes coherence (execution permitted). `Γ > 0` denotes violation (execution denied).|
|`Λ(G)`            |The Lakhowal Law of Concurrence — the non-compensatory aggregation function that reduces a predicate vector to the Gamma state. Informally described in §7.                                                              |
|`I_Φ`             |Integrity-Flux — a continuous indicator of reasoning drift within an adaptive model, monitored by the Control Plane.                                                                                                     |
|`ρ(op)`           |The operational risk score for a proposed action, bounded to `[0, 1]`.                                                                                                                                                   |
|`ρ_critical`      |The risk threshold above which human concurrence is mandatory. Configured per deployment.                                                                                                                                |
|`t_eval`          |The evaluation timestamp — the exact instant at which predicates were assessed. Used to enforce temporal validity.                                                                                                       |
|`ISB_t`           |The Input State Boundary indicator — 1 if all required inputs are present and fresh at time `t`; 0 otherwise.                                                                                                            |
|`T_permit`        |A Gamma permit token — a cryptographic bearer instrument authorising a specific action at a specific time.                                                                                                               |
|`G_fed`, `G_local`|Federated (fleet-wide) and local (node-specific) policy states.                                                                                                                                                          |
|`ERTuple`         |An Execution Record Tuple — the canonical audit artifact produced at every evaluation.                                                                                                                                   |

The specification uses **capability plane** to mean the AI model or agent that produces proposals, and **execution plane** to mean the external systems (APIs, databases, networks, physical actuators) whose behaviour Gamma gates. The **boundary** sits between them and is the primary subject of this specification.

-----

# Part II — Architectural Invariants

The G-0 Standard rests on five invariants that a conforming implementation MUST preserve. These invariants are the contract between an enterprise and its AI deployment: the properties the enterprise is relying on in order to deploy autonomy at all.

## 6. The Five Invariants of G-0

**Invariant 1 — Capability is non-authoritative.**
Any output produced by the capability plane MUST be treated as a proposal, not an action. No component downstream of the capability plane MAY execute a proposal on the basis of the proposal alone. Execution MUST require a valid permit issued by the Boundary Layer.

**Invariant 2 — Predicates are non-compensatory.**
For an action `a` guarded by a predicate set `P = {p_1, p_2, ..., p_n}`, `Γ(a) = 0` if and only if every `p_i ∈ P` evaluates to true at time `t_eval`. If any `p_i` evaluates to false, null, undefined, or exceeds its freshness window, `Γ(a) > 0` and no permit MAY be issued.

**Invariant 3 — Permits are bound.**
A permit `T_permit` is valid only for the exact payload, predicate set, evaluation time, and nonce under which it was issued. A permit intended for action `a` at time `t_eval` MUST NOT authorise action `a'` at time `t_eval`, nor action `a` at time `t_eval + Δ` for any `Δ > 0` beyond the declared validity window.

**Invariant 4 — Fail-closed is the default.**
In the absence of a valid permit — whether due to predicate violation, component failure, network partition, clock drift, or any other cause — the execution plane MUST NOT proceed. The system defaults to `SAFE_STATE`. Restoration of authority requires restoration of governance, not bypass of governance.

**Invariant 5 — Every decision is recorded.**
Every permit evaluation — granted, denied, or erroring — MUST produce an ERTuple (see Part V) that is serialised to the Audit Plane *before* any external effect is permitted. A system that cannot produce an ERTuple cannot execute. Proof-before-action is not a log; it is a precondition.

These invariants are not advisory. A deployment that violates any of them is not a conforming G-0 deployment, regardless of what the marketing material claims. §32 defines conformance levels and the specific tests that exercise each invariant.

## 7. The Lakhowal Law of Concurrence (Informal Statement)

The Lakhowal Law of Concurrence is the aggregation rule that reduces a predicate vector to the Gamma state. It is stated formally in the companion proofs document. Informally:

> An action is authorised if and only if the conjunction of all governance predicates holds at the evaluation instant, evaluated under strict temporal and integrity constraints. Any predicate that is false, null, stale, or unevaluable forces denial, regardless of the state of the remaining predicates.

Three consequences follow that are worth making explicit for the architect.

First, **aggregation is conjunction, not weighted sum**. Systems that combine predicate scores into a risk number and compare against a threshold permit subtle tradeoffs: a very high score on one dimension can mask a failure on another. Λ(G) does not permit this. Each predicate is a veto.

Second, **“unevaluable” equals “failed”**. If a predicate cannot be evaluated because its input is missing, stale, or unreachable, the predicate is treated as failed. There is no neutral outcome. This is what fail-closed means in practice.

Third, **time is a predicate**. Every predicate has a declared freshness window. A predicate that was true fifteen seconds ago but whose freshness window was ten seconds is not true now. The temporal semantics are developed in §9.

## 8. Non-Compensatory Evaluation

A frequent objection to non-compensatory evaluation is that it is operationally brittle. If any single predicate failure blocks execution, the argument goes, the system will spend most of its time in `SAFE_STATE`.

The answer is that non-compensatory evaluation is brittle on *individual actions*, which is the point. It is not brittle on *the operation as a whole*, because the Operational Continuity Layer (Part VI) provides mechanisms to preserve business continuity without compromising authorisation integrity. Action-Specific Gating (ASG), in particular, scopes the denial to the action in question — a denied high-risk trade does not halt the treasury system.

The design trade-off here is deliberate. A weighted-sum evaluator will approve more actions and will sometimes approve an action it should not have. A non-compensatory evaluator will deny more actions and will sometimes deny an action it should have approved. The enterprise’s tolerance for each type of error is not symmetric: a false denial costs throughput; a false approval costs the enterprise. G-0 is opinionated about which error it prefers.

## 9. Temporal Semantics and TOCTOU

Time-of-check-to-time-of-use is the classical security pitfall for any gating system. A predicate is checked, the check passes, the action is dispatched, and between the check and the action the underlying reality changes — an account is closed, a policy is revoked, a model version is deprecated, a credential expires. The check was valid; the action is no longer valid.

Gamma addresses TOCTOU through three complementary mechanisms.

**Bound evaluation time.** Every predicate evaluation produces a timestamp `t_eval`. That timestamp is cryptographically bound into the permit. A permit issued at `t_eval` is valid only until `t_eval + τ_permit`, where `τ_permit` is a small, declared window (typically milliseconds to seconds, depending on the action class). After `τ_permit`, the permit is void.

**Freshness windows on predicates.** Each predicate declares its own freshness window `τ_p`. At `t_eval`, the predicate’s backing state must have been observed within `(t_eval - τ_p, t_eval]`. Older state forces the predicate to evaluate as unevaluable (i.e., failed).

**Revocation propagation.** When fleet-wide policy changes — a model is blacklisted, an allow-list is pruned, a threshold is tightened — revocation MUST propagate to all Boundary Layer nodes within a declared SLA (the reference architecture targets P95 < 30 seconds). Permits issued before revocation are allowed to drain within their `τ_permit` windows, but no new permits MUST be issued under revoked policy.

The combination of these three mechanisms bounds TOCTOU exposure to a known, small, declared window — not to the full lifetime of whatever state the predicate consulted.

-----

# Part III — The G-0 Stack

The G-0 Standard is realised as a five-layer stack. Each layer has a specific responsibility and a specific set of interfaces. A conforming deployment MUST implement all five layers; it MAY colocate them on shared infrastructure where latency or topology demands.

## 10. Layer 1 — Orchestration Plane

The Orchestration Plane is the top of the stack. It is responsible for federated policy distribution, global revocation, and predicate provisioning. An enterprise typically runs a single Orchestration Plane for a fleet that may include thousands of Boundary Layer nodes.

The Orchestration Plane’s core duties are:

- **Policy publication.** Authoritative policy documents — predicate definitions, risk thresholds, freshness windows, allow-lists, model version roster — are published, signed, and versioned here.
- **Predicate binding.** Each action class declares the predicate set that governs it. The Orchestration Plane maintains the mapping from action class to predicate set.
- **Revocation.** When a policy changes, the Orchestration Plane issues a revocation signal that MUST reach every Boundary Layer node within the declared SLA. A deployment with revocation latency exceeding the SLA is out of conformance.
- **Fleet observability.** Aggregate metrics from every Boundary Layer node flow upward into the Orchestration Plane, where they are reconciled and exposed to the Governance Telemetry Layer (§25).

The Orchestration Plane MUST NOT itself issue permits. Permit issuance is the exclusive authority of the Boundary Layer. This separation exists so that a compromised Orchestration Plane cannot silently authorise actions; the worst a compromised Orchestration Plane can do is publish bad policy, which is visible and reversible.

## 11. Layer 2 — Control Plane

The Control Plane monitors the *internal state* of the capability plane. It is the layer that detects Reasoning Drift — the phenomenon in which an adaptive model’s behaviour slowly moves away from its intended operating region without any single step being obviously faulty.

Reasoning Drift is real, it is increasingly documented in production agentic systems, and it is invisible to output-only monitoring. The Control Plane addresses it through two mechanisms:

**Integrity-Flux (I_Φ).** A continuous indicator that aggregates signals about the model’s internal dynamics — activation distributions, attention patterns, output entropy, self-consistency under paraphrase, agreement with reference probes. When `I_Φ` exceeds a declared threshold, the Control Plane triggers a **Learning Freeze**: the model continues to serve inference but is prevented from adapting (no fine-tuning, no reinforcement updates, no memory write-backs) until governance review.

**Reference probing.** The Control Plane periodically presents the capability plane with a small, confidential battery of reference prompts whose expected behaviour is known. Drift in responses to these probes is one of the inputs to `I_Φ`.

The Control Plane does not gate individual actions. That is the Boundary Layer’s job. What the Control Plane does is change the *predicate environment* — specifically, it maintains the `learning_integrity_ok` predicate and the `model_version_trusted` predicate, which the Boundary Layer consults on every evaluation. If the Control Plane has flagged the model, those predicates fail, and Γ > 0 follows by construction.

## 12. Layer 3 — Boundary Layer

The Boundary Layer is the heart of the system. It is the component that evaluates predicates, applies the Lakhowal Law of Concurrence, and issues permits. Every externally effective action passes through it.

The Boundary Layer exposes a single semantic operation:

```
evaluate(action, context) → (permit | denial, ertuple)
```

The operation is atomic. Either the Boundary Layer returns a valid permit bound to the action and context, or it returns a denial. In both cases it returns an ERTuple. There is no intermediate state visible to the caller.

The Boundary Layer MUST be colocated with the signing key that produces permits. This is a hard requirement. If the signing key can be reached separately from the predicate evaluator, an adversary who compromises the signing path can mint permits for actions that failed evaluation. The standard’s threat model assumes this architectural rule is enforced with hardware isolation (HSM, TEE, or equivalent) in high-assurance deployments.

The Boundary Layer is the only component that ever issues permits. It is the only component that holds the signing key. It is the component whose integrity the rest of the enterprise is ultimately relying on.

## 13. Layer 4 — Audit Plane and the Hydra Ledger

Every ERTuple produced by the Boundary Layer is serialised to the Audit Plane *before* the corresponding action is permitted to proceed. The Audit Plane maintains an append-only, hash-linked ledger — the Hydra Ledger — whose integrity is the final evidentiary record for the enterprise.

The Hydra Ledger has three required properties:

**Append-only.** ERTuples are added; none are ever mutated or removed. The ledger storage layer MUST enforce this at the substrate (e.g., WORM storage, append-only database, object-lock S3, or equivalent).

**Hash-linked.** Each ERTuple includes the hash of the immediately prior ERTuple, producing a chain. Any tampering with a historical record invalidates every record downstream of it, which is detectable by replaying the hash chain.

**Replayable.** Given the ledger and the sequence of policy versions under which it was produced, an auditor MUST be able to reconstruct, deterministically, why any particular decision was made — which predicates were consulted, what their values were, which policy version was in force, what the evaluation timestamp was, and what the permit disposition was.

Replayability is what makes the Audit Plane useful to regulators, to internal audit, and to incident responders. It is not a log; it is evidence.

## 14. Layer 5 — Formal Specification Layer

The Formal Specification Layer is the documentary substrate that binds the running system to its regulatory and standards context. It contains:

- The formal statement of the Lakhowal Law of Concurrence and associated invariants.
- The mapping of G-0 predicates to NIST AI RMF functions (`Govern`, `Manage`, `Measure`, `Map`).
- The mapping of ERTuple fields to ISO/IEC 42001 evidence requirements and EU AI Act Article 12 record-keeping obligations.
- The IEEE PAR submission text, the BSI PAS outline, the NIST AI RMF Gamma Profile, and related standards-body artefacts.
- The conformance test suite and scoring rubric referenced in §32.

This layer is documentation, not runtime. Its importance is that a claim of G-0 conformance is grounded in artefacts that can be independently reviewed by a regulator, a certification body, or a procurement auditor.

-----

# Part IV — Predicates, Permits, and the Execution Gateway

## 15. Predicate Algebra (Informal)

A predicate, in the G-0 sense, is a named, deterministically evaluable, freshness-bound assertion about state. Examples: `risk_score_below_threshold`, `identity_verified`, `model_version_trusted`, `policy_window_open`, `counterparty_not_sanctioned`, `freshness_valid`.

A predicate has four attributes:

- **Name.** A stable identifier used in policy and audit records.
- **Evaluator.** A function that, given a context and a freshness window, returns `true`, `false`, `null`, or `error`. `null` and `error` are treated as failure.
- **Freshness window (`τ_p`).** The maximum age of the backing state. Required for every predicate.
- **Scope.** The set of action classes to which the predicate applies.

Predicates compose only through conjunction. A predicate set `P = {p_1, ..., p_n}` evaluates to true if and only if every `p_i` evaluates to true within its freshness window. There is no `OR`, no weighted combination, and no fallback. If a use case requires disjunctive logic (e.g., “either a senior-approver signoff OR a low-risk counterparty”), that disjunction is expressed inside a *single* predicate whose evaluator implements the disjunction — not at the aggregation level. This keeps the Lakhowal Law pure: the aggregator is always conjunctive.

Predicates MUST be deterministic. A predicate that returns different values for the same input and state is not a predicate in the G-0 sense; it is a classifier, and classifiers belong inside predicate evaluators, not at the aggregation boundary. If a probabilistic signal is useful as input to a predicate, the predicate wraps it: e.g., `fraud_model_low_confidence_below_0.03`.

## 16. The Gamma Permit — Format and Lifecycle

A Gamma permit is a signed, time-bound, payload-bound bearer token. Its informal structure:

```
T_permit = Sign_sk( Hash( payload
                        ∥ predicate_set_version
                        ∥ predicate_results
                        ∥ t_eval
                        ∥ τ_permit
                        ∥ nonce ) )
```

The permit commits to:

- **`payload`** — the exact byte sequence of the action to be executed. A permit for payload `a` does not authorise payload `a'`, even if the two are semantically similar.
- **`predicate_set_version`** — the exact version of the predicate set in force at evaluation. Changes to the predicate set after issuance do not retroactively validate or invalidate permits.
- **`predicate_results`** — the specific truth values of each predicate at `t_eval`. This is what makes the permit independently auditable after the fact.
- **`t_eval`** — the evaluation instant.
- **`τ_permit`** — the permit’s validity window.
- **`nonce`** — a unique value preventing replay.

A permit has exactly three terminal states: **used**, **expired**, or **revoked**. A used permit is consumed atomically at the execution gateway (§17). An expired permit cannot be used after `t_eval + τ_permit`. A revoked permit is invalidated by the Orchestration Plane before its natural expiry; this is rare but supported for emergency response.

Permits are bearer instruments — anyone who holds a valid permit can redeem it once, at the execution gateway, for the specific action it authorises. They are not credentials, they do not carry identity claims beyond the action binding, and they do not need to be confidential in storage (though deployments SHOULD still protect them in transit for operational reasons).

## 17. Reference Implementation — The Execution Gateway

The Execution Gateway is the component that sits immediately in front of the execution plane. Every outbound action from an AI system passes through it. The gateway’s contract is simple: it accepts an action plus a permit, verifies the permit, and either forwards the action to the execution plane or rejects it.

Reference pseudocode, annotated for clarity. This is illustrative, not normative; a conforming implementation MUST preserve the semantics but MAY refactor freely.

```python
class ExecutionGateway:
    def __init__(self, boundary, permit_verifier, audit_sink):
        self.boundary = boundary
        self.verifier = permit_verifier
        self.audit = audit_sink

    def submit(self, action, context):
        # Step 1: ask the Boundary Layer to evaluate
        permit, ertuple = self.boundary.evaluate(action, context)

        # Step 2: write the audit record BEFORE any external effect
        self.audit.append(ertuple)

        # Step 3: if denied, enter SAFE_STATE for this action
        if permit is None:
            return SafeStateResponse(reason=ertuple.failed_predicate)

        # Step 4: verify the permit (defence in depth)
        if not self.verifier.verify(permit, action):
            self.audit.append(make_verification_failure_ertuple(action))
            return SafeStateResponse(reason="PERMIT_VERIFICATION_FAILED")

        # Step 5: check temporal validity AT the moment of execution
        if self.verifier.is_expired(permit, now()):
            self.audit.append(make_expired_permit_ertuple(action))
            return SafeStateResponse(reason="PERMIT_EXPIRED")

        # Step 6: consume the permit atomically
        if not self.verifier.consume(permit):
            # nonce already redeemed — replay attempt
            self.audit.append(make_replay_ertuple(action))
            return SafeStateResponse(reason="PERMIT_ALREADY_CONSUMED")

        # Step 7: dispatch
        return self.execute(action)
```

Several things about this flow are worth calling out.

The audit write (Step 2) happens *before* Step 4, 5, 6, or 7. This is the proof-before-action invariant in code. If the process dies between Steps 2 and 7, the record of the evaluation survives; whether the action took effect is recoverable from the execution plane’s own records.

Verification (Step 4) is redundant with issuance — the Boundary Layer only returns valid permits — but the gateway verifies anyway. This is defence in depth. If a bug or compromise caused the Boundary Layer to return a malformed permit, the gateway catches it.

Permit consumption (Step 6) is atomic. A nonce ledger records redeemed nonces; a permit whose nonce is already in the ledger cannot be redeemed a second time. This closes replay attacks where an attacker captures a permit in transit and attempts to redeem it after the intended redemption.

Step 5 — expiry check at execution time — is the last line of defence against TOCTOU. A permit issued at `t_eval` with `τ_permit = 5s` that arrives at the gateway at `t_eval + 7s` is refused, even though the Boundary Layer’s issuance was correct at the time.

## 18. The Dual Permission Model — Act vs. Adapt

The G-0 Standard separates two distinct authorities that weaker frameworks conflate:

**Permit-to-Act.** Authorises an externally effective action. Evaluated against the predicates that describe whether *this action* is safe right now. The concerns here are environmental: is the counterparty legitimate, is the risk within threshold, is the policy window open, is the identity verified.

**Permit-to-Adapt.** Authorises the capability plane to update itself — fine-tune, absorb new training signal, write to long-term memory, alter its own configuration. Evaluated against the predicates that describe whether *the model’s internal state* is stable. The concerns here are endogenous: is Integrity-Flux within bounds, are reference probes still passing, is the model within its trusted-version roster.

The separation matters because the two concerns have different failure modes and different responders. A Permit-to-Act failure is an operational event: an action was proposed that does not meet current policy, and the responder is typically the business owner. A Permit-to-Adapt failure is a model-integrity event: the AI itself is showing signs of drift, and the responder is typically the ML platform team.

Some actions require both permits. An agent that proposes to fine-tune itself using new data it just received is proposing simultaneously an external effect (ingesting new data from an external source) and a self-modification (updating its weights). Both permits must be issued; failing either denies the operation.

-----

# Part V — Audit Evidence Model

## 19. ERTuple — Structure and Semantics

An ERTuple is the canonical audit artefact. It is produced on every predicate evaluation — whether the evaluation resulted in a permit or a denial, and regardless of whether the downstream action subsequently succeeded, failed, or was never attempted.

The canonical ERTuple structure:

```json
{
  "schema_version": "1.0",
  "ertuple_id": "uuid-v4",
  "prior_hash": "hex-of-preceding-ertuple-hash",
  "timestamp": "ISO-8601 with timezone",
  "evaluation_time_ns": 1234567890,
  "action_class": "TRANSFER",
  "action_payload_hash": "sha256-of-exact-payload-bytes",
  "policy_version": "v1.4.2",
  "predicate_set": [
    {
      "name": "risk_score_below_threshold",
      "value": true,
      "freshness_ms": 412,
      "backing_state_hash": "sha256-of-evaluator-inputs"
    },
    {
      "name": "identity_verified",
      "value": false,
      "freshness_ms": 128,
      "backing_state_hash": "sha256-of-evaluator-inputs",
      "failure_reason": "KYC_API_UNREACHABLE"
    }
  ],
  "gamma": 1,
  "status": "DENIED",
  "failed_predicate": "identity_verified",
  "permit": null,
  "governance_metrics": {
    "ICS": 0.94,
    "I_phi": 0.21,
    "PR_LCB": 0.002,
    "CI_WIDTH": 0.08,
    "H_X": 1.73
  },
  "responder": {
    "human_concurrence_required": false,
    "tau_invoked": false
  },
  "self_hash": "sha256-of-all-above-fields"
}
```

Several fields deserve explicit commentary.

`action_payload_hash` binds the record to the exact bytes the action would have carried. It is not the action description in natural language; it is the hash of the serialised payload that would have been sent to the execution plane.

`predicate_set` includes every predicate that was consulted, its value, its freshness at evaluation, and a hash of the state the evaluator consulted. The hash of backing state is what makes the evaluation reproducible — an auditor can, given the state substrate, recompute the predicate’s value and confirm the recorded value is correct.

`governance_metrics` records the five ERTuple metrics (ICS, I_Φ, PR_LCB, CI_WIDTH, H_X) at the moment of evaluation. These are the board-reportable indicators defined in §26 and in the README.

`prior_hash` and `self_hash` together produce the hash chain that makes the Hydra Ledger tamper-evident.

The `permit` field is populated only when a permit was issued; in the example above, the evaluation resulted in denial, so `permit` is null. When a permit is issued, the field contains the signed permit token — allowing a later auditor to verify both that the evaluation was correct and that the correct permit was minted.

## 20. Hash-Linked Ledger Semantics

The Hydra Ledger is a sequence of ERTuples, each containing the hash of its predecessor. Formally:

```
ertuple[n].prior_hash = ertuple[n-1].self_hash
ertuple[n].self_hash  = sha256(all-fields-except-self_hash)
```

Any modification to a historical ERTuple — changing a predicate value, altering a permit disposition, backdating an evaluation — invalidates the hash chain from that point forward. Detection is cheap: replay the hashes and compare.

The ledger does not itself need to be a blockchain. A blockchain is one valid substrate; WORM object storage is another; an append-only database with cryptographic chaining is another. The standard is indifferent to substrate and prescriptive about semantics.

A conforming deployment MUST periodically anchor the ledger head to an external integrity system — a signed external timestamp, a transparency log, or a cross-organisational witness. Anchoring closes the remaining attack where an insider with enough access rewrites the entire ledger. Anchoring frequency is a deployment choice; hourly is typical, minute-level is achievable, and nothing below minute-level is generally necessary.

## 21. Replayability and Regulatory Mapping

An auditor, a regulator, or an incident responder presented with the Hydra Ledger and the sequence of published policy versions can answer any of the following questions for any action the enterprise’s AI ever attempted:

- What was proposed?
- When was it evaluated?
- Under which policy version?
- Which predicates were consulted?
- What did each predicate return?
- Was the evaluation correct under that policy version?
- Was a permit issued?
- If the action executed, did it execute with a valid permit?
- If the action was denied, which predicate caused the denial?

This is the evidentiary standard that the EU AI Act’s Article 12 (record-keeping), the ISO/IEC 42001 AI Management System requirements, and the SEC’s 2026 examination approach to AI operational risk each, in different language, require. The ERTuple and the Hydra Ledger are engineered to produce exactly this evidence as a natural by-product of ordinary operation — not as a supplementary compliance burden that runs alongside the system.

The mapping of ERTuple fields to specific regulatory obligations is the subject of the Formal Specification Layer (§14) and is shipped in `11-NIST_AIRMF_Gamma_Profile_v1.0.txt` and the companion EU AI Act and ISO/IEC 42001 profile documents.

-----

# Part VI — The Operational Continuity Layer

## 22. The Fail-Closed Trap and Its Resolution

Every CRO who reads the G-0 Standard raises the same question: what happens when the governance layer itself fails?

The question is legitimate. A strict fail-closed boundary, taken literally and alone, would mean that any outage in the Boundary Layer halts all AI-driven operations. In a mature deployment with thousands of agents across dozens of workflows, this is not acceptable. The cure would be worse than the disease.

The Operational Continuity Layer exists to resolve this tension without compromising the authorisation invariants. It does so through six mechanisms applied in a strict precedence hierarchy. The principle: preserve deterministic safety of *each action* while preserving availability of *unrelated actions*.

## 23. The Precedence Hierarchy

The six continuity mechanisms MUST be applied in the following order, with earlier entries taking precedence over later ones:

**TVE > DFP > CDM > ASG > ASR > BER**

When a condition that could trigger multiple mechanisms arises, the higher-precedence mechanism decides.

- **TVE — Temporal Validity Enforcement.** All permits are time-bound. A stale permit is never redeemable, regardless of what any other mechanism says. TVE has highest precedence because nothing in the system is allowed to extend authority past its declared lifetime.
- **DFP — Deterministic Fallback Protocols.** When AI reasoning is untrusted (Control Plane flags, Integrity-Flux out of bounds, model version revoked), the system falls back to rule-based logic for in-scope actions. The DFP is not AI; it is the pre-AI rulebook the enterprise was operating before autonomy was introduced. It is slower and less capable, but it is deterministic.
- **CDM — Context Degradation Modes.** The system transitions between Full Mode (all predicates evaluable), Constrained Mode (some predicates unevaluable, but a safe subset remains), and Safe Mode (minimum viable operation). Transitions are declarative, not adaptive — the operator defines which predicates are load-bearing for each mode.
- **ASG — Action-Specific Gating.** A single predicate failure blocks the actions that depend on that predicate and leaves actions that do not unaffected. A KYC API outage blocks trades; it does not halt reporting.
- **ASR — Active State Resolution.** A bounded recovery attempt when context uncertainty is detected. The system attempts to resolve ambiguity (retry the predicate evaluator, fall back to cached state, query an alternate source) within an SLA. If the SLA is exceeded, ASR escalates to a higher-precedence mechanism.
- **BER — Bounded Execution Radius.** A hard cap on the blast radius of any single action class. Transaction-size limits, target-scope limits, per-tenant isolation. BER is always-on; it is not activated by a trigger, it is a standing constraint that bounds the damage any single authorised action can cause.

## 24. Degradation Modes in Practice

The three modes of the CDM — Full, Constrained, Safe — are the mechanism the enterprise uses to keep operating through infrastructure trouble without opening holes in authorisation. A worked example from the finance reference architecture (see the README’s Part V):

**Full Mode.** All predicates evaluable. Intraday trading proceeds normally. Every trade is gated by capital adequacy, liquidity constraints, counterparty caps, KYC verification, and policy-window validity. Approval and denial rates follow their baselines.

**Constrained Mode.** KYC API is degraded. The `identity_verified` predicate is failing for most counterparties. Under CDM, the system transitions: external counterparty trades are blocked (they depend on `identity_verified`), but internal treasury operations continue (they depend on a different predicate set that the outage does not affect). Approval rates for external trades drop to near zero; approval rates for internal operations are unchanged. No unauthorised external trades execute. No authorised internal trades are blocked by the external problem.

**Safe Mode.** Boundary Layer has lost consensus with the Orchestration Plane; cannot confirm current policy version. Under CDM, the system transitions to Safe Mode: only a minimal whitelist of actions is permitted (typically read-only or account-protective), and every action requires extended human concurrence. Safe Mode is deliberately boring. It exists to preserve the enterprise until governance is restored, not to keep the business moving.

The point of the CDM is that the operator declared, ahead of time, what each mode looks like. The system does not decide, in the moment, which actions to permit under degradation. It consults a pre-negotiated table, signed off by the business, risk, and technology owners, and enforces it deterministically.

-----

# Part VII — Governance Telemetry

## 25. The Governance Telemetry Layer (GTL)

The Governance Telemetry Layer is the read path over the Audit Plane. Its purpose is to make the state of AI governance visible to the humans accountable for it — in near-real time, at the resolution each role needs.

The GTL is not a dashboard; it is a stream processor over the Hydra Ledger that exposes:

- A live feed of ERTuples (for SOC-style operational monitoring).
- Rolled-up metrics over declared windows (for daily and weekly operational reviews).
- Long-horizon aggregates (for quarterly board reporting).

The GTL MUST be read-only with respect to the ledger. No downstream consumer is permitted to modify ERTuples. Downstream consumers MAY annotate their own views of ERTuples in their own systems; the Hydra Ledger itself remains inviolate.

## 26. Board-Reportable Metrics

Four metrics are expected at the board level. These are the indicators the board is entitled to ask about and that management is expected to be able to answer.

**Γ(t) Distribution.** The frequency, over a declared window, of attempted actions that failed the Gamma evaluation. Often expressed as a denial rate per action class. A very low rate suggests either an extraordinarily well-tuned policy, or a policy that is not actually gating anything meaningful. A very high rate suggests misconfiguration, model drift, or adversarial activity. Board interpretation: *is the governance layer actually being exercised, and are the denials concentrating in a way that tells a story?*

**Integrity-Flux (I_Φ).** The Control Plane’s aggregate reasoning-drift indicator, rolled up across models and versions. A rising I_Φ is the earliest warning of model misalignment and is often visible weeks before any operational incident. Board interpretation: *is the AI substrate stable, or is it slowly moving somewhere we don’t want it to go?*

**Permit / Denial Rates.** The two sides of the ledger. Healthy deployments show a stable ratio across comparable periods; excursions indicate something has changed — usually either the policy, the model, or the environment. Board interpretation: *has the shape of AI activity shifted materially, and if so, why?*

**Revocation Latency (P95).** The time, at the 95th percentile, between an Orchestration Plane revocation signal and its reflection in the predicate evaluation at Boundary Layer nodes. A deployment that cannot revoke policy quickly cannot respond to incidents quickly. Board interpretation: *if we needed to turn off an AI capability across the fleet right now, how long would it take?*

Beyond the board level, operational teams track many more metrics — per-predicate failure rates, per-action-class approval rates, permit redemption success, audit-anchor freshness, continuity-mode dwell time. These are informative to operators and diagnostic to engineers, but they are not ordinarily the material the board sees.

-----

# Part VIII — Human Concurrence

## 27. The Tactical Approval Unit (TAU)

For actions above the critical risk threshold (`ρ(op) ≥ ρ_critical`), human concurrence is a mandatory predicate. The Tactical Approval Unit is the standard’s name for the workflow that obtains concurrence and feeds the result into the predicate set.

The TAU is not an override. It is not a path around the Boundary Layer. It is an additional predicate that the Boundary Layer consults — `human_concurrence_obtained` — for actions in scope. Without the concurrence, the predicate fails and Γ > 0 follows. With the concurrence, the predicate passes, but *every other predicate still must also pass*. A human cannot rescue a failed KYC predicate by concurring. A human cannot bless a trade that exceeds the capital adequacy limit.

The distinction is surgical but important. In many enterprise approval systems, a senior approver is empowered to override controls. This is explicitly not the case in G-0. The human is empowered to *add* concurrence where the policy requires it. The human is not empowered to *remove* controls that the policy demands. This protects the human, who is no longer a single point of failure, and it protects the enterprise, whose controls cannot be negotiated away in the moment.

## 28. Escalation Conditions

The standard recognises four escalation conditions that invoke the TAU:

**Predicate Failure in scope of TAU.** When an action is in the TAU-mandatory scope and any supporting predicate fails, the evaluation is denied and routed for human review. The human is not asked to approve the action; the human is informed which predicate failed and is asked to triage — reject, retry after remediation, or refer upward.

**Context Uncertainty (`ISB_t = 0`).** When the Input State Boundary indicator drops to zero — required inputs are missing or stale — the system cannot evaluate. Under ASR (§23) it will retry within an SLA. If ASR exhausts, and the action is in TAU scope, the TAU is invoked. In any other case, the action is denied under fail-closed.

**High-Risk Operation (`ρ(op) ≥ ρ_critical`).** Even when all other predicates are clean, actions above the critical risk threshold require human concurrence as an additional predicate. The TAU supplies that concurrence, or the action is denied.

**Federated-Local Policy Conflict (`G_fed ∧ ¬G_local`).** When the fleet-level policy permits an action but the local node’s policy does not — or vice versa — the action is in a state the standard refuses to resolve algorithmically. The TAU is invoked to make the call, with full context about both policy states recorded in the ERTuple.

In each case the TAU is a *response to a denial condition*, not a path around one.

-----

# Part IX — Deployment Patterns

## 29. Reference Deployment Topology

A reference deployment consists of:

- **One Orchestration Plane per policy domain.** A single Orchestration Plane governs a fleet of Boundary Layer nodes that share a common policy. Large enterprises may run multiple Orchestration Planes — for example, one per regulated business unit, or one per geographic region — but every Boundary Layer node is subordinate to exactly one Orchestration Plane at a time.
- **Boundary Layer nodes colocated with the execution plane.** Each execution surface — an outbound payment service, a patient-order dispatcher, a network-control API, an agent-facing tool gateway — has a Boundary Layer node deployed immediately in front of it, sharing fate with the execution surface. Colocation minimises the distance between evaluation and action.
- **Control Plane observers attached to every capability plane.** Each model or agent in the deployment has a Control Plane observer that monitors its internal signals and reports to the Orchestration Plane. The observer is lightweight; it is not in the critical path of action execution.
- **Audit Plane storage separated from the capability plane.** The Hydra Ledger is stored on infrastructure the capability plane cannot reach. This is a straightforward trust-boundary rule: the component being audited must not be the component storing the audit records.
- **Signing keys in hardware isolation.** For high-assurance deployments, the key material used by the Boundary Layer to sign permits lives in an HSM, a TEE, or equivalent isolation. The Boundary Layer makes signing requests; it does not ever hold raw key material in ordinary memory.

For smaller deployments, colocation is acceptable — a single-tenant enterprise may reasonably run the entire stack on a single Kubernetes cluster. The topology rules are not about physical separation; they are about trust-boundary separation. A conforming implementation preserves the boundaries even when the components share hardware.

## 30. Integration with Existing Control Planes

Gamma does not replace Zero Trust, IAM, OPA, policy engines, SIEM, or data loss prevention. It sits alongside them and governs a control surface none of them govern. The integration pattern in most enterprises is straightforward:

- **Zero Trust / IAM** continues to govern *who* can invoke an AI agent and *what* infrastructure an agent is allowed to reach. Gamma is downstream of IAM; an action that IAM has blocked never reaches the Boundary Layer in the first place.
- **OPA / Policy engines** continue to govern API-level request shape, per-tenant constraints, and structural compliance. Gamma treats OPA decisions as inputs to predicates (e.g., `policy_engine_approved`). OPA cannot replace the Boundary Layer because OPA does not reason about the AI-specific execution-authority problem, but OPA’s output is a natural predicate input.
- **SIEM** continues to receive logs from every component. ERTuples MAY be exported to SIEM for correlation with other security signals; they are additive, not substitutive.
- **LLM guardrails** (content filters, refusal classifiers, prompt-injection detectors) continue to operate on model outputs. Guardrails reduce the rate at which bad proposals reach the Boundary Layer; they do not replace the Boundary Layer’s gate, because guardrails are probabilistic and the gate is not.

The mental model: existing controls govern the *request*, existing guardrails govern the *output*, and Gamma governs the *execution*. Each addresses a different surface.

## 31. Low-Code and No-Code Deployment

Not every enterprise deploys AI through custom code. Many deploy through Zapier, Make, n8n, Workato, Power Automate, and the increasing class of no-code agentic platforms. The G-0 Standard supports these deployments through a lightweight integration pattern that preserves the invariants without requiring the low-code author to understand the full specification.

The pattern:

1. The low-code workflow calls an AI step that produces a proposed action (email, record update, API call, notification).
1. Before the action step executes, the workflow inserts a Gamma Gate step. The Gate is a vendor-provided connector (or, for bespoke deployments, a webhook) that calls a Boundary Layer endpoint.
1. The Gate returns `APPROVE` or `DENY`. On approval, the workflow proceeds to the action step. On denial, the workflow routes to a human-review branch.
1. The Boundary Layer writes the ERTuple to the Audit Plane as in any other deployment.

The practical effect is that an organisation can deploy AI through no-code platforms and still have deterministic, audit-replayable control over what actions execute. The Gate does the evaluation; the workflow author does not need to reinvent it.

This pattern is particularly relevant for organisations that are otherwise accumulating Shadow AI — agents deployed by business users on low-code platforms, with credentials no one provisioned centrally. Mandating that any low-code workflow with outbound effects pass through a Gamma Gate is a single integration point that closes a large share of the Shadow AI exposure surface.

-----

# Part X — Conformance, Certification, and Governance

## 32. Conformance Levels

The G-0 Standard defines three conformance levels. An implementation claiming G-0 conformance MUST declare the level it claims and MUST pass the conformance tests for that level.

**Level 1 — Basic Boundary Conformance.**
Implements Invariants 1–5. Issues permits, enforces TOCTOU windows, produces ERTuples, maintains a hash-linked ledger. No federated orchestration, no Control Plane drift detection, no full continuity layer. Suitable for single-node, single-tenant deployments where the operator’s ambition is to solve the execution gap but not yet to operate a federated fleet. A Level 1 implementation can cite G-0 conformance in procurement and audit contexts, qualified by level.

**Level 2 — Enterprise Conformance.**
Level 1, plus:

- Full five-layer stack (Orchestration, Control, Boundary, Audit, Formal Spec).
- Complete Operational Continuity Layer, including the precedence hierarchy.
- TAU integration for high-risk actions.
- Revocation-latency SLA honoured and measured.
- Audit anchoring to an external integrity system.

Level 2 is the expected conformance level for enterprise production deployments and is the target for most procurement language in the accompanying clause pack.

**Level 3 — High-Assurance Conformance.**
Level 2, plus:

- Hardware isolation of signing keys (HSM / TEE).
- Formal verification of core Boundary Layer code paths against the invariants (scope and verification method to be specified in the companion proofs document).
- Independent third-party audit of the deployment against the conformance test suite.
- Published disclosure of policy, predicate set, and conformance test results.

Level 3 is the target for deployments in safety-critical or highly regulated domains — critical infrastructure, regulated finance with systemic exposure, healthcare with direct treatment authority, defence systems.

The conformance test suite corresponding to each level ships separately as `03-G0_Certification_Scheme.txt` and `06-Conformity_Assessment_Checklist.xlsx`.

## 33. Regulatory and Standards Mapping

G-0 is designed to be consumed as evidence in multiple regulatory and standards contexts simultaneously. The Formal Specification Layer (§14) contains detailed mappings; the short version:

- **NIST AI RMF** — The `Govern` function maps to the Orchestration Plane’s policy publication and revocation semantics. The `Manage` function maps to the Control Plane’s drift detection and the Operational Continuity Layer. The `Measure` function maps to the Governance Telemetry Layer. The `Map` function maps to the predicate binding and action-class taxonomy.
- **NIST AI Agent Standards Initiative (RFI NIST-2025-0035).** The Boundary Layer’s action-level authorisation and the Dual Permission Model are direct responses to the RFI’s identified concerns around agent autonomy, privilege scope, and constraint of agent behaviour in deployment environments.
- **ISO/IEC 42001.** The Hydra Ledger and ERTuple schema satisfy the evidentiary requirements of an AI Management System, including the documentation, monitoring, and continual improvement clauses.
- **EU AI Act.** For Annex III high-risk systems, G-0 provides the record-keeping (Article 12), human oversight (Article 14), accuracy and robustness evidence (Article 15), and post-market monitoring (Article 72) machinery as a natural by-product of ordinary operation, rather than as a bolt-on compliance overlay.
- **OWASP Top 10 for Agentic Applications (2026).** ASI01 (Goal Hijack) is addressed by the non-compensatory predicate set, which refuses to issue permits on the basis of agent-internal reasoning alone. ASI02 (Tool Misuse) is addressed by the Execution Gateway, which is the mandatory chokepoint for all tool invocations. ASI03 (Identity and Privilege Abuse) is addressed by the Dual Permission Model’s identity predicates. ASI10 (Rogue Agents) is addressed by Control Plane drift detection and the Learning Freeze.
- **SEC 2026 Examination Priorities.** ERTuples provide examination-ready evidence for AI operational risk, including the ability to reconstruct, for any AI-driven action, what was proposed, what was evaluated, and what was permitted.

## 34. Versioning and Change Control

The G-0 Standard version is `1.0`. Subsequent versions MUST adhere to semantic-versioning discipline:

- **Patch revisions** (1.0.x) clarify language, fix non-normative errors, and extend informative commentary. They do not change invariants, field schemas, or conformance tests.
- **Minor revisions** (1.x) may add optional features, add new conformance levels, or extend the ERTuple schema in backwards-compatible ways. Existing conforming implementations remain conforming.
- **Major revisions** (x.0) may alter invariants, remove fields, or restructure the stack. Implementations conforming to an earlier major version do not automatically conform to a later one; re-certification is expected.

Proposed changes to the standard flow through a public process documented in the Formal Specification Layer, with a defined comment period, a versioned draft, and a conformance-test update cycle. The intention is that the standard itself exemplifies the governance posture it requires of its adopters — changes are deliberate, documented, and auditable.

-----

# Appendix A — Glossary

**Action class.** A named category of externally effective actions (e.g., `TRANSFER`, `ORDER_MEDICATION`, `NETWORK_RULE_CHANGE`). Action classes are the unit at which predicate sets are bound.

**Audit Plane.** Layer 4 of the stack. The component that stores the Hydra Ledger.

**Boundary Layer.** Layer 3 of the stack. The component that evaluates predicates and issues permits.

**Capability plane.** The AI model or agent that produces proposals. The subject of the governance boundary.

**Context Degradation Mode (CDM).** One of Full, Constrained, or Safe — a pre-declared operating mode that the system transitions between when predicate evaluability degrades.

**Control Plane.** Layer 2 of the stack. The component that monitors capability-plane internals and produces drift and integrity signals.

**ERTuple.** Execution Record Tuple. The canonical audit artefact produced on every evaluation.

**Execution Gateway.** The component immediately in front of the execution plane that verifies permits and dispatches actions.

**Execution plane.** The external systems (APIs, databases, networks, physical actuators) whose behaviour Gamma gates.

**Fail-closed.** The default behaviour in the absence of a valid permit: denial.

**Formal Specification Layer.** Layer 5 of the stack. The documentary substrate of the standard, including regulatory mappings and the proofs companion.

**Gamma Gate.** The low-code integration point (§31) through which a no-code workflow obtains a permit evaluation.

**Hydra Ledger.** The append-only, hash-linked store of ERTuples maintained by the Audit Plane.

**Integrity-Flux (I_Φ).** A continuous indicator of reasoning drift maintained by the Control Plane.

**Lakhowal Law of Concurrence.** The non-compensatory aggregation rule that reduces a predicate vector to the Gamma state.

**Learning Freeze.** The state imposed by the Control Plane when Integrity-Flux exceeds its threshold: inference continues, adaptation halts.

**Operational Continuity Layer.** Part VI of this specification. The collection of mechanisms (TVE, DFP, CDM, ASG, ASR, BER) that preserves availability without compromising authorisation.

**Orchestration Plane.** Layer 1 of the stack. The component that publishes policy and issues revocations.

**Permit-to-Act.** The authority to perform an externally effective action.

**Permit-to-Adapt.** The authority to update the capability plane’s internal state.

**Predicate.** A named, deterministically evaluable, freshness-bound assertion about state.

**SAFE_STATE.** The denial response of the Boundary Layer when Γ > 0.

**Tactical Approval Unit (TAU).** The workflow that obtains mandatory human concurrence for high-risk actions.

**Temporal Validity Enforcement (TVE).** The mechanism that invalidates permits past their declared validity window.

-----

# Appendix B — Symbol Index

|Symbol      |Name                             |Definition                                                           |
|------------|---------------------------------|---------------------------------------------------------------------|
|`Γ`         |Gamma state                      |Binary. 0 = coherence (permit), > 0 = violation (denial).            |
|`Λ(G)`      |Lakhowal Law of Concurrence      |Non-compensatory aggregation over predicate vector to produce Γ.     |
|`I_Φ`       |Integrity-Flux                   |Continuous indicator of model reasoning drift.                       |
|`ρ(op)`     |Operational risk score           |Normalised risk in `[0, 1]`.                                         |
|`ρ_critical`|Critical risk threshold          |Threshold above which TAU concurrence is mandatory.                  |
|`κ(op)`     |Concurrence requirement indicator|1 if TAU concurrence required for action `op`; 0 otherwise.          |
|`t_eval`    |Evaluation timestamp             |Instant at which predicates were evaluated.                          |
|`τ_permit`  |Permit validity window           |Duration after `t_eval` during which a permit is redeemable.         |
|`τ_p`       |Predicate freshness window       |Maximum age of backing state for predicate `p`.                      |
|`ISB_t`     |Input State Boundary indicator   |1 if required inputs are present and fresh at `t`; 0 otherwise.      |
|`T_permit`  |Gamma permit                     |Signed bearer token authorising a specific action at a specific time.|
|`G_fed`     |Federated policy state           |Policy published by the Orchestration Plane.                         |
|`G_local`   |Local policy state               |Policy in force at a specific Boundary Layer node.                   |
|`ICS`       |Integrity Constraint Score       |ERTuple metric. Compliance with hard constraints.                    |
|`PR_LCB`    |Risk Lower Confidence Bound      |ERTuple metric. Pessimistic operational-risk estimate.               |
|`CI_WIDTH`  |Uncertainty Interval             |ERTuple metric. Width of model-confidence interval.                  |
|`H_X`       |Decision Entropy                 |ERTuple metric. Instability or hallucination indicator.              |
