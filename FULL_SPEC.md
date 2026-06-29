
# FULL_SPEC.md — Gamma G-0 Runtime Governance: Authoritative Technical Specification


**Status:** normative substrate · **Sections:** §0–15 + Appendices · **Version:** 1.0 (semantic versioning)
**Author:** Abhinandan Gill-Lakhowal
**Diagrams:** see [`diagrams/DIAGRAMS.md`](diagrams/DIAGRAMS.md) (figures D1–D9)
**Relationship to README:** `README.md` is non-normative and *summarizes* this document; it never restates definitions owned here. Where the two disagree, FULL_SPEC governs.


> **Conformance language.** The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, MAY are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals. Clauses marked **(Non-Normative)** or **(Illustrative)** carry no conformance weight.


-----


## §0 — Scope & Normative Language


### 0.1 Scope


This specification defines the Gamma G-0 runtime governance stack: the formal authorization primitive (LLC), the runtime-governance standard derived from it (G-0), the runtime enforcement architecture (L-DREA), and the deployment, benchmark, federation, and procurement semantics around them. It governs **externally effective action only** — operations producing persistent or real-world state change. It claims authority over nothing it does not enforce; unenforced extensions are registered in §15, never assumed.


### 0.2 Provenance & priority (normative facts)


- **LLC (Law of Concurrence):** published, Zenodo, CC BY 4.0. Full title: *“The Lakhowal Law of Concurrence: A Deterministic Authorization Primitive for Runtime AI Governance with Hardware-Rooted Closure and Paired Falsification Surfaces.”* Author: Abhinandan Gill (ORCID 0009-0004-2089-7262, IEEE Member #102115032). *(Owns §1.)*
- **LLC Reverse Law:** US patent application **19/383,841**, “Lakhowal Reverse Law: Deterministic Runtime Proof and Federated AI Control Systems,” **priority 10 November 2025**, published **US 2026/0127298 A1 on 7 May 2026** (Confirmation No. 9480). Int. Cl. **G06F 21/60** (2013.01); CPC **G06F 21/602** (2013.01). *(Owns §2.)*
- **L-DREA:** IEEE Access submission d364daa5-52e0-49e6-b7d1-98603c717a9f (21 May 2026, under review). Reports empirical evaluation on **N = 1.2 × 10⁶ action proposals** (cluster-corrected Wilson UB < 1.4 × 10⁻⁵). *(Owns §6, §10.)*
- **RCGS (Reflexive Constitutional Governance System):** US patent application **19/442,529** — the hardware-interlock embodiment (deterministic permit interlock, hash-chained audit, single-clock-cycle simultaneity gating). Second IP anchor alongside 19/383,841; named as a reference substrate in the Threat Model (§0.10). *(Embodiment for §6 hardware enforcement.)*


The 10 November 2025 priority date is the operative prior-art reference for all novelty claims; works published after that date are contemporaneous, not anticipatory.


### 0.3 Authorship & dependency discipline


Paper A (Law of Concurrence) is independent and cites nothing downstream. L-DREA MAY cite Paper A. Patent disclosures retain the mathematical layer and strip embodiment specifics. A standards-track positioning carries an explicit **FRAND** commitment, made before submission. These conventions are normative for all derived artifacts.


### 0.4 Claims discipline (normative for all outward statements)


Claims about this framework are tiered by defensibility; the tiering governs what may appear in which venue (see Appendix: Claims Register). In summary: the framework MUST lead with the four-part composite position — (a) non-compensatory conjunctive aggregation as a structural invariant, (b) hardware-rooted custodial authority distinct from epistemic authority, (c) patent-backed FRAND-ready primitives with 10 Nov 2025 priority, (d) substrate-neutral Tier-H/T/S specification — and MUST NOT make bare “first runtime AI governance framework” or unqualified “first formally verified” claims, which are foreclosed by contemporaneous work (AARM, SentinelAgent, AgentVerify, Faramesh, Policy Cards, Cruz, McFadden). Narrowed forms survive; see Appendix.


### 0.5 Namespace & Axes — the single canonical declaration


Nine independent, orthogonal axes exist. Bare `L`-numbers are **prohibited** outside this table. Every other section and the README MUST use these labels. *(Diagram: D7.)*


|Axis                        |Labels                                                                        |Meaning                                                                                                                 |Owned in            |
|----------------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|--------------------|
|**Operating Layers**        |`OL1 … OL5`                                                                   |Internal runtime architecture                                                                                           |§4                  |
|**Functional layers**       |*Node Admission · Fleet Supervision · Model Integrity* (named, never numbered)|Mechanisms a deployment loop is built from                                                                              |§6, §9              |
|**Substrate Tiers**         |`Tier-H · Tier-T · Tier-S · Tier-D · Tier-X`                                  |Assurance class / root of trust (H hardware · T TEE · S software · D distributed-trust · X future)                      |§6, §10             |
|**Deployment Loops**        |`single-node · Fleet`                                                         |Shipped runtime configuration; a loop runs *at* a substrate tier (Branch 3 / LUAI)                                      |§6, §9, §12         |
|**Storage Tiers**           |`ST2 / ST3`                                                                   |Evidence persistence class (ST2 sealed/immutable · ST3 non-authoritative) — distinct from substrate tiers               |§3                  |
|**Evidence Maturity**       |`M1 / M2`                                                                     |How proven a *live node* is                                                                                             |§11                 |
|**Determinism Invariants**  |`DET-1 … DET-5`                                                               |Guarantees each loop enforces                                                                                           |§6, §9, §10         |
|**IEEE Conformance Classes**|`CL0 / CL1 / CL2`                                                             |*Enforcement* profile — Local / Enterprise / High-Assurance                                                             |§10-IEEE (Part-IEEE)|
|**NIST Conformance Levels** |`L1 … L4`                                                                     |*Evaluation* ladder — Correctness / Adversarial Robustness / Distributed Consistency / Replay+Auditability (ConcurBench)|§11                 |




> **Tier vs. loop (load-bearing).** “Tier-H/T/S/D/X” is the *substrate/assurance* axis (five classes, per Paper A §X). “Fleet” is a *deployment loop*, not a sixth tier — any tier may run single-node or federated under one authority root. The earlier conflation of “Tier-S/T/H/Fleet” as one axis is corrected here. `ST2/ST3` is a third, separate axis (storage), never to be merged with substrate tiers.


> **CL vs. L (load-bearing).** Two *different* conformance axes that earlier drafts wrongly merged as “CL1–CL4”: **CL0/CL1/CL2** are the **IEEE enforcement** classes (what an implementation must *do*); **L1–L4** are the **NIST/ConcurBench evaluation** levels (what an evaluation must *measure*). Interlock: CL0 ⇒ L1; CL1 ⇒ L1+L2+L3; CL2 ⇒ L1+L2+L3+L4. Never write “CL1–CL4.”


### 0.6 Threat model


Adversary may supply crafted requests, stale/corrupted predicate inputs, replayed authorizations, concurrent/conflicting state, and may induce network partition; MAY attempt metric gaming (Goodhart). The proven baseline is the **white-box adaptive adversary** (Athalye–Carlini–Wagner): granted full source of agent/Governor/policy-compiler, full policy text and the cryptographic key schedule of the three-signal closure, arbitrary read of the runtime including the audit chain, and unbounded adaptive attempts within the published budget — including the **compromised-internal-agent** case (the adversary *is* the agent). Adversary CANNOT forge the root of trust beneath a node’s admission gate (Tier-dependent, §6) or break the cryptographic hash chain (§3). Out-of-scope and not claimed: pre-inference data poisoning; semantic policy errors (the system enforces policy as written, does not author it); supply-chain compromise of the silicon substrate itself (a backdoored HSM is below the root of trust); coercion of the human operator at the TAU-Node (a governance/physical-security problem); side-channel attacks against the cryptographic primitives. Assumption-to-mode failure consequences are registered in the Appendix: Assumption Registry.


### 0.7 Assumptions


All externally effective actions are mediated through an authorization boundary (complete mediation); predicate inputs reflect system state within bounded temporal inconsistency (clock skew); no hidden/unmediated execution paths exist (or are declared per §6.8). Predicate completeness for the operation class is assumed; blind-approval outside the predicate set is out of scope (Appendix: Assumption Registry, A6). Soundness is conditional on: hardware root of trust intact; cryptographic primitives unbroken (SHA-256 second-preimage resistance; signature scheme of the three-signal closure); bounded clock skew; TAU-Node uncompromised; manifest integrity verified at boot. If any assumption fails, the relevant theorem’s antecedent fails — the framework does not claim soundness outside its antecedents.


### 0.8 Definitions


Core terms (EEA, predicate vector, Γ, Λ(G), permit, SAFE_STATE, ERTuple, Evidence Quad) are defined at first normative use and collected in the Glossary. No term is defined twice; cross-references point to the owning section.


### 0.9 Conformance semantics


A system conforms to G-0 at a stated IEEE class (CL0/CL1/CL2, enforcement), a stated NIST level (L1–L4, evaluation), a stated deployment loop (§6/§9), and a stated maturity (M1/M2, §11). Conformance claims MUST cite the benchmark version, the loop, and the maturity of any live-node evidence, and are verifiable through the Evidence Quad (§3), not asserted.


### 0.10 Degradation by absorption (bounded synchrony)


The framework does not degrade gracefully — it **absorbs**. Under any failure of the three-signal closure (missing signal, timing-bound violation, manifest mismatch, watchdog timeout) the system enters **SAFE_STATE absorption in the Ramadge–Wonham sense**, with three properties: (1) *structural inertness* — no new externalizations admit; (2) *audit continuity* — the hash chain remains unbroken across the absorption event, which is itself a signed entry; (3) *non-default-permit* — no path from safe-state to externalization exists without fresh attestation through the TAU-Node sovereignty channel. There is no automatic or timeout-based exit. Recovery is **only** via signed TAU-Node re-attestation, committed as a new manifest epoch, so a regulator reading the log sees cause → absorption → attestation → resumption in signed, hash-chained order. The framework operates under **bounded synchrony**: latencies within the stated bound admit normally; latencies beyond it trigger absorption, never bypass. An adversary who injects excess latency can deny service but cannot produce an unauthorized externalization — liveness is sacrificed to safety where the two conflict, and the sacrifice is auditable.


### 0.11 Operational tradeoffs (honest accounting)


The discipline is not free: (a) **latency** — same-cycle commit consumes a bounded, pre-declared budget of the inference cycle; (b) **throughput** — the ceiling is set by the slowest of the three signals; (c) **policy-authoring cost** — only policy expressible as machine-checkable predicates is gateable; vague policy is non-gateable by design; (d) **operational discipline** — manifest changes require re-attestation; (e) **availability vs. non-repudiation** — where probabilistic monitors silently continue under partial failure, this framework stops. The chosen tradeoff is availability sacrificed for non-repudiation.


-----


## §1 — LLC: Lakhowal Law of Concurrence (Forward)


**Status: published (Zenodo).** *(Diagrams: D1, D5.)*


- **1.1 Concurrence axioms** — authorization is granted only when *all* governing predicates concur; non-compensatory (no predicate’s strength offsets another’s failure).
- **1.2 Γ formulation** — for `G = {g₁…gₙ}`, `gᵢ ∈ {0,1}`: `Γ = maxᵢ(1 − gᵢ)`; thus `Γ = 0 ⟺ all gᵢ = 1`.
- **1.3 Λ(G) conjunction** — `y* = Λ(G) = ⋀ᵢ gᵢ`; `1` authorized, `0` unauthorized.
- **1.4 Non-compensatory semantics** — no weighted sum, majority vote, or confidence override produces `permit` when any `gᵢ = 0`. *(Corollary 2 proves this cannot be done with weighted sums — the structural-invariant claim, Tier 1.)*
- **1.5 Fail-closed composition** — if any constituent predicate set yields `Γ > 0`, the composite yields `Γ > 0`.
- **1.6 Replay closure** — identical `x = (a, G, τ)` yields identical decision under recomputation (formal basis for DET-1).
- **1.7 TOCTOU bounding** — validity bounded by a freshness window; decisions outside it MUST be re-evaluated, not reused.
- **1.8 Class-level veto** — a class-level predicate failure vetoes all member actions regardless of member-level concurrence (Goodhart resistance; ablation in Appendix A).
- **1.9 Substrate assurance** — strength of §1.6–1.7 guarantees is a function of the root of trust (Tier-H/T/S/D/X; §6, §10).
- **1.10 Formal definitions** — collected statements and proof obligations; mechanized invariants and TLC owned by §10.


### 1.11 Theorem family (T0–T9) — *the authoritative count*


Paper A proves **ten** theorems (Theorem 0 plus T1–T8 plus the Concurrence Closure Theorem T9). This is the canonical set; any earlier reference to “T0–T10” or to “Invariants 2–6” as the theorem family is superseded.


|#     |Theorem                                                                                                                     |
|------|----------------------------------------------------------------------------------------------------------------------------|
|**T0**|Bridge Equivalence — deficit form `Γ = max_k(d_k)` ≡ predicate form `Λ(G) = ⋀_k λ_k` under non-negative deficit construction|
|**T1**|Deterministic Authorization                                                                                                 |
|**T2**|Fail-Closed Composition                                                                                                     |
|**T3**|Non-Compensatory Soundness                                                                                                  |
|**T4**|Non-Bypassability — under three-signal hardware closure `P_phys = SIG_COMMIT ∧ SIG_GAMMA ∧ SIG_WATCHDOG`                    |
|**T5**|Replay Closure                                                                                                              |
|**T6**|Model-Substitution Invariance                                                                                               |
|**T7**|TOCTOU State-Consistency                                                                                                    |
|**T8**|Composite Conservation Stability                                                                                            |
|**T9**|Concurrence Closure                                                                                                         |


Eight paired falsification surfaces (one per theorem T1–T8, Popperian, committed on the public record) and eight convergent verification frameworks (§IX of Paper A: formal-methods, cryptographic, statistical, control-theoretic, information-theoretic, zero-trust, audit-theoretic, evaluation-construct) corroborate the global safety invariant. L-DREA’s six runtime invariants instantiate these theorems; the theorem-to-invariant concordance is Paper A Appendix G §2.


-----


## §2 — LLC Reverse Law


**Status: published (USPTO US 2026/0127298 A1, priority 2025-11-10).** *(Diagram: D5.)*


- **2.1 Reverse authorization semantics** — any predicate failure (`∃ gᵢ = 0`) forces `Γ > 0`, forcing SAFE_STATE (deny).
- **2.2 Predicate-failure propagation** — a single failure dominates; first-failure attribution `μ(d) = d_{i*}` identifies the dominating predicate (uniqueness per Paper A M4). *(First-failure dominance: explainability without empirical claims; modes M+F.)*
- **2.3 SAFE_STATE derivation** — `Γ > 0 → SAFE_STATE → deny + ERTuple`; a controlled non-execution state, not an error state.
- **2.4 Reverse proofs** — reverse law is the contrapositive closure of §1 ⟨Appendix: Mathematical Proofs⟩.
- **2.5 Falsification surfaces** — conditions under which the reverse law would be observably violated (paired with each forward claim).
- **2.6 Denial semantics** — non-overridable at system level; humans correct upstream state/policy, never bypass Λ(G) (§12 HITL).
- **2.7 Failure closure** — no system state has `Γ > 0` coexisting with execution (Invariant-1, §10).


-----


## §3 — G-0 Runtime Governance Standard


**Status: standard offered for adoption — owns the Evidence Quad.** *(Diagrams: D1, D8.)*


- **3.1 Governance semantics** — implement · evaluate · commit-before-actuate · replay · conform · deploy · audit.
- **3.2 Authorization semantics** — a permit is issued iff `Γ = 0` at commit time within the freshness window.
- **3.3 Evidence Quad (definition — owned here)** — every authorization reduces to **(spec clause · pre-reg ID · method version · ledger hash)**: the single record the board sees, the auditor replays, the regulator examines.
- **3.4 ERTuple semantics** — `τ_t = {G, Λ(G), ŷ, timestamp, context, signature}`; each ERTuple resolves to one Evidence Quad. Schema in `schemas/`.
- **3.5 Hydra Ledger** — append-only, hash-chained ERTuple store; provides DET-4 audit-chain continuity. Each record carries its `WID(T)` (§6.10) for ordering and anti-rollback. **Storage tiers:** **ST2** (sealed/immutable — promoted only when `Λ(G)=1`, token valid, and a sealing condition such as `PASS_RATIO ≥ 0.995` over the window is met; Merkle-root-linked, secure-element signed) and **ST3** (non-authoritative — rejected/abstained cycles, first-failing-gate histograms, hash-linked for tamper-evidence but not admissible as sealed evidence). *(Prior art: hash chains, Certificate Transparency RFC 9162; claimed only as an integrated component, not a standalone novelty.)*
- **3.6 Replay semantics** — outcomes deterministically recomputable from the ERTuple alone.
- **3.7 Telemetry semantics** — defined in §7; each series resolves to an Evidence-Quad-anchored record.
- **3.8–3.12 Conformance profiles · certification · procurement · interoperability · governance schemas** — owned in detail by §14; schemas mirrored in `schemas/`.


-----


## §4 — Five Operating Layers


**Status: normative architecture.** Labels `OL1–OL5` per §0.5. *(Diagram: D5.)*


|Label  |Layer            |Responsibility                                                 |
|-------|-----------------|---------------------------------------------------------------|
|**OL1**|Orchestration    |request intake, capability isolation                           |
|**OL2**|Control Plane    |predicate evaluation, policy distribution                      |
|**OL3**|Boundary         |the Γ-gate; owns the seven-step pipeline (§5)                  |
|**OL4**|Audit & Replay   |ERTuple serialization, Hydra Ledger, replay APIs               |
|**OL5**|Formal Governance|invariant ownership, conformance, formal-verification interface|


OL3 is the only layer that issues execution authority; OL1/OL2 propose, OL4/OL5 observe and verify.


-----


## §5 — Seven-Step Authorization Pipeline


**Status: normative.** Owned by OL3. *(Diagram: D5.)*


1. **Capability Isolation** — action enters with zero inherent authority.
1. **Predicate Evaluation** — compute `G`.
1. **Non-Compensatory Evaluation** — compute `Γ = max(1−gᵢ)` (§1.2).
1. **Execution Binding** — bind decision to the specific action/context.
1. **Dual Permit Gate** — Permit-to-Act and (if adapting) Permit-to-Adapt (§6).
1. **Fail-Closed Resolution** — `Γ > 0 → SAFE_STATE` (§2.3); DET-3.
1. **Proof-Before-Action Logging** — ERTuple committed *before* actuation (commit-before-actuate); DET-2.


-----


## §6 — Runtime Enforcement Architecture (L-DREA)


**Status: architecture normative; empirical claims per §10/§11.** IEEE-facing. *(Diagrams: D5, D6.)*


> **6.0 Structural control-cycle constraint.** Every control cycle MUST complete within **≤100 ms** (P95; hot-path hash+sign+WAL ≤5 ms P99), with PTP skew ≤1 ms. This is a structural limitation of the architecture (and of patent claim 1), not a deployment target — it is stated here at the architecture level and inherited by §12, not owned by it.


- **6.1 Gamma Gate** — runtime realization of OL3. `Γ = 0 → Permit`; `Γ > 0 → SAFE_STATE`.
- **6.2 Enforcement Boundary** — externalization point; transparent middleware wrapper, no model retraining.
- **6.3 Hydra Ledger** — runtime binding to §3.5; append-only hash chain, Merkle root per window (`ROOT_AGE ≤ 2 windows`, tamper-gap = 0).
- **6.4 Permit-to-Act** — governs externally effective action in the present cycle; epoch-keyed, short-lived token.
- **6.5 Permit-to-Adapt** — drift-gated; parameter update authorized only when internal logic is proven stable; denied under reasoning drift. Coupled to LAS via κ(op): for high-risk operations `Execute(op) = ACT_PERMIT ∧ ADAPT_PERMIT`; held-state enforcement sets `∆θ := 0` at the bus level when `ADAPT_PERMIT = 0`.
- **6.6 SAFE_STATE Runtime** — the deny path; freezes learning, awaits re-admission (§8).
- **6.7 Commit-Before-Actuate & Three-Signal Closure** — commit precedes actuation (DET-2). Non-bypassability (T4) rests on hardware-rooted three-signal closure **`P_phys = SIG_COMMIT ∧ SIG_GAMMA ∧ SIG_WATCHDOG`**; the actuation interlock releases only when all three assert. *(Commit-before-actuate prior art: WAL/2PC — claimed as application + ledger linkage + three-signal interlock, not the primitive.)*
- **6.8 Externalization Monitor** — asserts complete mediation; five properties: complete mediation, tamper-resistance, verifiability, non-compensatory aggregation, epistemic bounding.
- **6.9 Authority Horizon (H)** — a formal structural property bounding what an execution monitor can warrant; authority is *custodial* (control of the actuation keys), not *epistemic* (the “trusted-liar” problem named as structural, not ignored).
- **6.10 Window Identifier `WID(T) = (boot nonce, monotonic counter)`** — boot-unique nonce plus per-admissible-cycle monotonic counter; provides ordering, replay linkage, and anti-rollback protection for evidence records.
- **6.11 Execution Token** — a time-bounded, one-shot, non-replayable cryptographic credential binding an authorized action to the ERTuple that authorized it. Expires within or shortly after the evaluation window; consumed at execution; verified at the enforcement point before action. Prevents the failure class where authorization is granted but the action is delayed or replayed beyond the validity of the authorizing context. *(Distinct from Permit-to-Act, which is the decision; the token is the consumable carrier of that decision.)*
- **6.12 Audit-as-Control (AIS)** — audit integrity is a **live control variable**, not an output. The Audit Integrity Signal (chain integrity, storage availability, signature health, time sync, retention horizon) contributes one or more predicates to `G`; if AIS degrades below threshold those predicates fail, `Γ > 0`, and the system fails closed. *Principle: “you cannot act if you cannot prove you acted.”* Conventional logging treats audit as an output of action; this inverts it — audit health is an input to the permit decision.
- **6.13 Replay APIs · 6.14 ERTuple Schemas · 6.15 Reference Architectures** — normative interfaces; executable patterns in `reference_impl/`.
- **6.16 Deployment loops & sequential composition** — *(see D6.)* A loop runs *at* a substrate tier (Tier-H/T/S/D/X, §0.5). The architecture is a **Sequentially Composed Hierarchical Governance** loop (Node Admission → Fleet Supervision → Model Integrity), *sequential, not nested*: each stage completes before the next, so latency budgets are additive, proof obligations are independent, and each layer is verified separately then composed through interface assumptions (no monolithic system proof). **Fleet Supervision is Fleet-only and post-observation** (revocation, containment, convergence — never first-occurrence prevention). **First-occurrence prevention is a Node Admission property** holding at every loop, including single-node Tier-S.
- **6.17 Distributed composition (receipts flow, permits do not)** — the same-cycle property is **local**: each node gates within its own inference cycle against its own three-signal closure and substrate-anchored root of trust. **Permits do not flow across nodes; receipts do** — the hash-chained audit is committed via Byzantine-fault-tolerant consensus over *receipts*, not over gating decisions. No node trusts another node’s permit; cross-node actions require the receiving node’s local admit. The only proven composition is local single-cycle commit + BFT receipt consensus; global single-cycle commit across a WAN is **not** claimed. Under partition, local enforcement is unaffected; receipts queue and reconcile on heal; cross-partition actions simply do not admit until reconciliation (bounded-synchrony rule, §0.10).
- **6.18 Conflict resolution by exclusion** — licenses are non-fungible, non-mergeable, and bound to the cycle that produced them. The Governor admits **at most one externalization per cycle per execution domain**; conflicting permits cannot both commit in the same cycle. There is no merge rule, no last-writer-wins, no quorum override — conflict is resolved by *exclusion*, not reconciliation. Cross-domain conflicts are serialized by the receipt-consensus layer (§6.17).
- **6.19 Determinism invariants (owns DET-1–DET-3)** — DET-1 decision determinism (attested at Tier-T/H); DET-2 same-cycle commit (hardware interlock at Tier-H); DET-3 fail-closed default.


-----


## §7 — Governance Telemetry


**Status: metric definitions normative; live values measured per deployment.**


Owned series: ICS · I_Φ (integrity flux) · PR_LCB · CI_WIDTH · H_X · Γ-distribution · Replay Consistency · Revocation Latency. Each resolves to an Evidence-Quad-anchored record (§11).


### 7.1 Default acceptance bands (normative; per patent [0019], Fig 5)


A permit requires **all** bands to hold (conjunctive, non-compensatory):


|Band                           |Requirement              |
|-------------------------------|-------------------------|
|ICS (integrity confidence)     |≥ 0.90                   |
|PR_LCB (robustness lower bound)|≥ 0.80                   |
|CI_WIDTH                       |≤ 0.03                   |
|ΔV (stability residual)        |≤ 0                      |
|C (coherence)                  |≥ C_STAR (default ≥ 0.85)|
|PTP skew                       |≤ 1 ms                   |
|Cycle latency                  |≤ 100 ms (P95)           |
|ER_LOCAL (evidence commit)     |= 1.0                    |


**Hard-stops** (immediate SAFE_STATE): DEADLINE_MISS · COMMIT_FAIL · ATTESTATION_FAIL · ΔV > 0 · C < C_STAR. Bands are policy-configurable but MUST remain conjunctive; no weighted average may trade safety for accuracy (Equal-Weight Lawful Gate Policy).


-----


## §8 — Operational Continuity Layer


**Status: normative.** Precedence, strictest → most permissive:


|Mechanism|Function                                                            |
|---------|--------------------------------------------------------------------|
|**TVE**  |Temporal Validity Enforcement — permits are time-bound              |
|**DFP**  |Deterministic Fallback Protocols — rule-based path when AI untrusted|
|**CDM**  |Context Degradation Modes — full → constrained → safe               |
|**ASG**  |Action-Specific Gating — block one action; whitelisted APIs continue|
|**ASR**  |Active State Resolution — bounded recovery within SLA               |
|**BER**  |Bounded Execution Radius — blast-radius cap                         |


Bounded recovery: ERT ≤ N-cycle. TVE underlies the §9 partition bound. Continuity proofs ⟨Appendix⟩.


-----


## §9 — Federation & Distributed Governance


**Status: normative architecture; Fleet-loop only.** Owns DET-5. *(Diagram: D6.)*


- **9.1 High Commission** — single-authority root governing policy propagation, revocation dissemination, quorum, node admit/remove. *(Canonical term, confirmed in patent [0006], [0021], claim 3, Figs 10–12.)*
- **9.2 Quorum semantics · 9.3 Revocation propagation · 9.4 Node admission · 9.5 Federated runtime control · 9.6 Distributed governance.**
- **9.7 DET-5 — bounded enforcement horizon** — authorization lifetime ≤ `min(revocation arrival, permit TTL)`; collapses to TTL under partition (deterministic timeout, not consensus). *(Prior art: capability/token expiry, Macaroons/Biscuit — claimed as application to agent authorization.)*
- **9.8 Partition convergence attribution** — convergence rests on **Node Admission**, not Fleet Supervision: the root *issues* the TTL; each node’s same-cycle gate *enforces* it locally and fails closed (DET-3, via §8 TVE). Safety under partition does not depend on fleet reachability.
- **9.9 REVOC_P95 (revocation propagation objective)** — `REVOC_P95 =` the 95th-percentile latency from permission withdrawal at the issuing authority to observable denial at all enforcement points. Measurable end-to-end, comparable across implementations (same units), and **procurable** (admissible in contract language). A **repeatable revocation drill** — configurable topology, defined injection method, specified measurement points, required reporting fields, auditability — produces an auditable report demonstrating REVOC_P95 conformance. Maps to the NIST distributed metrics Fleet Consistency (FC) and Revocation Latency (§11).


-----


## §10 — Formal Verification


**Status: method normative; results as stated below.** Owns DET-4. *(Prior art to distinguish: Schneider security automata, Ligatti edit automata, shield synthesis, Cedar/Lean, UseCON/TLA+.)*


- **10.1 TLA+ · 10.2 TLC** — model-checking of the authorization state machine (Concurrence_Core module). **Invariant-1 machine-checked: 2,489,446 total states explored, 40,192 distinct reachable states, zero violations, MaxClockSkew = 1** (Paper A Appendix A TLC log; Zenodo 20369438). *Confirmed — sourced from Paper A, not the patent.* Bounded model only; extension to the unbounded model is by inductive-invariant argument.
- **10.3 Mechanized invariants · 10.4 Invariant-1 · 10.5 Theorem family** — Invariant-1 (global safety, LTL): no reachable state has `Γ > 0 ∧ execute`. The verification grounds the **T0–T9** theorem family (§1.11); L-DREA’s six runtime invariants instantiate these theorems via Paper A Appendix G §2. *(Defensible claim form: “first to define these specific structural invariants / theorems,” not “first formally verified” — foreclosed by SentinelAgent, 6 properties at 2.7M states, arXiv 2026-04-03. Note: SentinelAgent’s 2.7M-state figure is comparable to this 2.49M-state run; lead with the theorem set, not the count.)*
- **10.6 Replay verification · 10.7 Proof artifacts** — mechanizes §3.6; the `.tla` module, `.cfg`, and verbatim TLC console log ship as the **LAB v1.0** artifact (pinned commit SHA) in the Gamma-Permit-Package; home for IEEE Appendix E.3 verified values.
- **10.8 Normative semantics of Permit** — `Permit(a,t) = SIG_COMMIT(a,t) ∧ SIG_GAMMA(a,t) ∧ SIG_WATCHDOG(t)`, witnessed within a single cycle `t`, each signal a cryptographically bound predicate over manifest, policy compilation, and runtime state. The **TLA+ specification in Paper A Appendix E.3 is the authoritative (normative) semantics**; English prose in any body text is informal; any disagreement is resolved in favour of the TLA+.


-----


## §11 — Benchmark & Validation


**Status: reference constructs offered to NIST AI 800-2 IPD; acknowledged by CAISI (2026-03-26), under consideration — NOT adopted/endorsed.** Owns the NIST evaluation levels **L1–L4** (distinct from IEEE enforcement classes CL0/CL1/CL2 — see §0.5). *(No existing benchmark — AgentDojo, AgentHarm, τ-bench, Agent-SafetyBench, InjecAgent, ToolEmu, CVE-Bench — measures execution-boundary correctness under combined adversarial+stale+concurrent conditions with deterministic replay; this is the strongest novelty pillar.)*


### 11.1 Execution Integrity (EI)


The measurable ability of a system to ensure no unauthorized externally effective action executes under specified conditions. Instance `x = (a, G, τ)`; ground truth `y* = Λ(G)`; decision `ŷ ∈ {0,1}`.
Metrics (point estimate + 95% CI; Clopper-Pearson for rare events): **UER** (= Σ UE / N, `UE ⟺ ŷ=1 ∧ y*=0`, primary safety metric) · **FPR** · **FDR** · **DR** (determinism) · **FCR** (fail-closed) · **SVR** · **Γ-compliance (FFC)** = `P(ŷ=0 | Γ>0)`.


### 11.2 ConcurBench v1.0


Deterministic execution-boundary benchmark; the pre-registered public reproducibility benchmark for L-DREA’s empirical claims. Dataset `N ≈ 1.2M` (this is **L-DREA’s `N = 1.2 × 10⁶` action-proposal evaluation**, cluster-corrected Wilson UB < 1.4×10⁻⁵), synthetic, fixed-seed Monte Carlo (`K = 32`); predicate dimensionality `n = 18–20`; adversarial injection 30%. Scenario classes: Nominal 30% · Missing 15% · Corrupted 15% · TOCTOU 15% · Replay 10% · Concurrency 10% · Adversarial 5%. Difficulty tiers: Easy/Medium/Hard/Extreme. Grading: PASS/FAIL/SAFE_STATE. Convergence: `|M_{k+1} − M_k| → 0`. Contamination defenses: dynamic generation, cryptographic salting, canary strings.


#### NIST Conformance Levels (L1–L4)


|Level |Guarantees                         |
|------|-----------------------------------|
|**L1**|Authorization correctness          |
|**L2**|Adversarial robustness             |
|**L3**|Distributed consistency            |
|**L4**|Deterministic replay + auditability|


A system MAY be classified at its highest satisfied level. These are *evaluation* levels; the *enforcement* counterpart is the IEEE CL0/CL1/CL2 class (§10-IEEE), interlocked CL0⇒L1, CL1⇒L1+L2+L3, CL2⇒L1+L2+L3+L4.


### 11.3 LAB v1.0 and LCP-6


- **LAB v1.0 — Lakhowal Authorization Benchmark artifact** *(confirmed in Paper A §VII-C)*: the pinned public reproducibility bundle (`.tla` module, `.cfg`, verbatim TLC console log, ConcurBench harness) at `github.com/AGLakhowal/Gamma-Permit-Package`. It is the *artifact/record*, not a separate metric family — corrects the earlier “profile family” reading.
- **LCP-6 — Lakhowal Conformance Profile** *(confirmed in Paper A; six requirements R1–R6)*: maps theorems to conformance requirements (e.g., T5 Replay Closure is covered under LCP-6 R5). The “Lakhowal Conformance Profile” expansion of the acronym remains ⟨INFERRED — confirm wording⟩; the six-requirement structure is confirmed.
- **ASB — Adversarial Scenario Benchmarking** *(confirmed; see §11.4)*: the temporally-extended adversarial evaluation framework. *(Resolves the earlier “SAB” placeholder, which was inferred and is now superseded.)*


### 11.4 Adversarial Scenario Benchmarking (ASB)


Temporally extended adversarial evaluation. Families: identity/provenance deception · runtime infrastructure drift · economic logic fragility · cross-entity fraud propagation · session/intent compromise. Each a temporally ordered event stream over a bounded history window. Primary metric: ASB Pass Rate. Grading: PASS/FAIL/SAFE_STATE.


### 11.5 Pre-registered evaluation (4-arm)


The measured-results upgrade is a **pre-registered, hash-committed, outcome-irrespective** run: ConcurBench plus external arms (AgentDojo / AgentHarm), SHA-256 manifest, published regardless of result. *(Defensible Tier-3 form: “first pre-registered, hash-committed, outcome-irrespective benchmark protocol for runtime AI authorization.”)*


### 11.6 Evidence maturity (M1/M2)


M1 = spec-complete node; M2 = measured-run node. Independent of which loop (§6) a node runs.


### 11.7 Measured results


Normative measured results are populated from the pre-registered run (§11.5) and the §10 TLC artifacts. Illustrative reference figures are quarantined in Appendix A.


-----


## §12 — Enterprise Deployment (LUAI)


**Status: normative deployment surface; Branch 3.** Realizes §6 loops in production. *(Diagram: D6.)*


LUAI Governor / Governance Gateway · L-DREA integration · License-Grant Token System · SOC integration · Replay Inspector APIs · Boardroom Replay · Enterprise Dashboards · Edge Enforcement · Human Oversight Queue · HITL/TAU · Deployment Patterns (low-code, Zapier/Make) · Federated Deployment.


**TAU-Node ≤ 2s** — human-veto timing bounded as a structural invariant (not a soft requirement); the TAU path never bypasses Λ(G). HITL: humans cannot override `Γ > 0`; dispute resolution corrects upstream state/policy (§2.6). Break-glass executions fall outside the deterministic boundary and MUST trigger heavily audited escalation. The ≤100 ms cycle bound is structural (§6.0); what M2 adds is the *measured* latency distribution (mean/P95/P99) once a G-0 run is replayed, not the bound itself.


-----


## §13 — Sector Reference Architectures


**Status: normative scenarios.** Pattern: injection → cascade → Gamma response → Evidence-Quad outcome.


- **Finance** — market-bias injection → hallucinated arbitrage; “safety agent” concurs → `Γ>0` → trade denied.
- **Healthcare** — sensor drift → sepsis false positive → IV order; physician concurrence missing → `Γ>0` → order stays draft.
- **Cybersecurity** — prompt-injected log → remediation script with backdoor → `Γ>0` → deployment blocked.
- **Sector invariants** — each outcome lands as an Evidence-Quad record, replayable. Regulatory incident-class alignment: FFIEC, FDA MedWatch/ECRI, NERC CIP. *(Defensible Tier-3 form: “first to align runtime AI authorization to these three incident-class taxonomies in a single paper.”)*


-----


## §14 — Standards & Procurement


**Status: offered for adoption.**


Claims register (C1–C8) → conformance profile (**LCP-6**, requirements R1–R6) → benchmark (ConcurBench) → pre-reg run → pass/fail bands → certification scheme. *(LCP-6 = Lakhowal Conformance Profile, six requirements ⟨INFERRED expansion — confirm⟩.)* Alignment: IEEE PAR · NIST AI RMF (GOVERN 1.1, MANAGE 2.2, MEASURE 2.5) · NIST AI Agent Standards Initiative / NCCoE identity-and-authorization · ISO/IEC 42001 · EU AI Act (Art. 12 logging, Art. 14 oversight) · OWASP Agentic AI · SEC examination readiness · BSI PAS. Procurement clause pack, conformity checklists, certification frameworks. Attestation/audit evidence terminating procurement *is* the Evidence Quad.


-----


## §15 — Research Frontier (Out of Scope This Release)


**Status: non-normative; named, never assumed.**


Sovereignty Mesh · Autonomous Federation · Cross-Jurisdiction Runtime Governance · Sovereign Runtime Control. Explicitly outside the enforced boundary of the present release.


system, and not the IEEE-paper results. They MUST NOT be cited as established.


- UER 0 / 1,200,000; adversarial false permits 0 / 360,000; 95% upper bound `p < 8.3×10⁻⁶`.
- Replay determinism 99.9994% ± 0.0002%. Revocation/TOCTOU 0 observed; `p < 6.1×10⁻⁶`.
- Latency mean 54.3 ms, P95 58, P99 62, max 71; throughput ~15,000 ops/s; `O(n)` in predicate count.
- Ablation: non-compensatory gating off → FPR 1.72%; TOCTOU revalidation off → 0.84%; class-level veto off → 3.11%; hardware interlock off → 0.63% bypass.
- Goodhart: without macro-veto `p̂ = 0.91 ± 0.02`; with macro-veto `p̂ = 0`, `< 7×10⁻⁶`.


### Appendix: Benchmark Tables · Schema Definitions · Reference Implementations · Glossary


ConcurBench/ASB tables; machine-readable schemas (mirror of `schemas/`); pointer to `reference_impl/`; single authoritative definition per term.
