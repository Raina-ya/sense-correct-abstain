# Claim ledger (MT7, Subtask 7.1)

**Status:** MT7 deliverable, 2026-11-21; A3, A7, and B1 updated after the owner review (E007). Every statement the technical report
([`../paper/technical_report_v1.md`](../paper/technical_report_v1.md)) makes
must appear here with its evidence type and scope. Where an erratum governs,
the latest one listed takes precedence (E007 over E006; E006 over E001 and E003).

**Evidence types** (contract §2): analytic; noiseless simulation; noisy
simulation (here: **shot-noise-only** synthetic simulation with coherent E2;
no decoherence or visibility loss); device-parameter simulation (none);
hardware (none).

**Statement kinds:** finding; hypothesis; possible explanation; boundary
(a negative or limiting result).

**Global scope of every row unless stated otherwise:**

- the synthetic compiled-angle E2 model (no physical carrier established);
- the frozen 2–6 qubit, `p = 1` QAOA MaxCut populations and grids; and
- `N = 24,300` shots per unit.

No row is a hardware claim. "Internal recomputation" means recomputation by
the project; nothing here is third-party validated.

## A. Analytic results

| ID | Statement | Kind | Evidence | Scope / limitations | Source |
|---|---|---|---|---|---|
| A1 | RC frame covariance: `P RZ((1+epsilon)s theta + phi) P = RZ((1+epsilon)theta + s phi)` for the frozen Pauli construction. | finding | analytic (proved, M2) | Frozen sign-flip construction with virtual Z; wrapped-Z not adopted. | `docs/theory/gate1_frame_covariance_draft.md` |
| A2 | At `phi = 0`, label-resolved outcome laws are label invariant for every `epsilon`, so the label-contrast information for `epsilon` is exactly zero. | finding | analytic | Primary synthetic model. | same; `conditional_likelihood_v1.md` |
| A3 | Lemma S1′: at `phi = 0`, `epsilon` is locally non-identified under any nuisance class containing a free label-independent per-candidate distribution, and globally non-identified under the response-free classes (N-free, N-loc), each by explicit construction; its efficient information is zero. | finding (**proved, owner-reviewed with corrections**; the per-context/visibility extension S1″ is a draft) | analytic; numerical check of zero efficient information (≤ 6.8e-21/shot) | Says nothing about structured nuisance classes, under which oracle information is 0.24–0.62/shot. Under N-q the identified set is a bounded interval (Prop. 4), so global non-identification fails there. | E006 §2, E007, `docs/theory/S1prime_B_rigorous.pdf` |
| A4 | Three-action risk identity; reductions to the predecessor's Eq. (6) and to a Chow-type rule. | finding (draft proof) | analytic | Attribution of the exact Chow form unverified (full text not read). | `three_action_theory_v1.md` |
| A5 | Action-selection blindness lemma and finite-pilot two-point bound (Le Cam and Bretagnolle–Huber proved in the note). | finding (draft proof) | analytic | Tsybakov lemma locations unverified; the proofs are self-contained. | same |
| A6 | Information-free policies cannot have positive population `Delta_V` under the issue-only comparator (P2). | finding (draft proof) | analytic | Population level only; metadata-only policies are not covered. | same |
| A7 | Lemma B: the E2 shift of the expected candidate gap satisfies `\|Delta g\| <= (\|epsilon\| A + \|phi\| M)/2`, globally and uniformly (constant 1/2, `l_1` perturbation norm, no remainder). | finding (**proved, owner-reviewed**; constant 1/2 sharp) | analytic; numerical check (max ratio 0.431) | Assumes single occurrence of each tagged angle and the noiseless synthetic error model. Expected gap only; says nothing about `B_hat` coverage or the sampled-gap rule. | E006 §3, E007, `docs/theory/S1prime_B_rigorous.pdf` |

## B. Gate results (frozen verdicts and their corrected bases)

| ID | Statement | Kind | Evidence | Scope / limitations | Source |
|---|---|---|---|---|---|
| B1 | **Gate 1A FAIL.** Retained RC labels did not satisfy the frozen deployable identifiability rule. The valid basis is A3 together with the frozen recovery rule. The frozen run's I3, recovery, and control entries were hard-coded and are not evidence. | finding / boundary | analytic | Frozen nuisance class ambiguous (readings disclosed in E001 §3 and E007 §3.2); FAIL holds under every reading considered, in all six designs. Under the literal first-order reading, G3 has tiny second-order information (≤ 3.5e-6/shot at `phi != 0`; SE ≈ 11 at budget). The step "nonunique maximizer ⇒ FAIL" is a specification inference checked against §7 and §9. | E001, E006 §2, E007 |
| B2 | At the frozen sensing budget (`n_S = 2430`), the equal-prior two-point error between the frozen hard pairs is at least 0.185–0.232, even with a known response. | finding | analytic + stored exact quantities | Action relevance of the pairs nonevaluable (no action map frozen). | E001 §4, E006 §5 |
| B3 | **Gate 1B PASS.** The frozen P-amp design identifies `(epsilon, phi)` from its own known reference; its circuit semantics match the estimator's phase model (729 cases, max deviation 3.4e-15). | finding | analytic + noiseless simulation | The resource condition passes with a **0.7% margin** at visibility 1 and fails for visibility below 0.9926. **No visibility attenuation, decoherence, drift, or context mismatch was tested.** Sensor–target transfer holds by construction. | E002 |
| B4 | **Gate 2 formal PASS, interpreted narrowly** (wording below). | finding (formal) + boundary (practical) | shot-noise-only synthetic simulation; post-hoc diagnostics exploratory | Plan deviations: no uncertainty bound, no power analysis, resolution-based margin. P2 comparator structurally blind on 3300 of 6600 units. | E003, E006 §4 |
| B5 | **Gate 3 FAIL:** no detectable net value of the deployable three-action policy over the best fixed policy (always correct). Frozen: `Delta_V = 0.0000804`, lower bound −0.000743. Corrected estimand: 0.000237 and −0.000625 (**post-lock reanalysis**; it cannot change or rescue the verdict). | finding / boundary | shot-noise-only synthetic simulation | Estimated power **0.0004**; the design could not have detected a plausible effect. 256-replicate Monte Carlo scoring. | E004 |
| B6 | Gate 4 PASS (N 25.9%, C 72.6%, A 1.5%). | finding | same | Moot after the Gate 3 failure; thresholds not power-derived. | E004 §4 |
| B7 | The project stopped at M6 under the frozen stopping rule and entered MT7. No registration, holdout, or confirmatory claim exists. | finding (procedural) | — | — | E004 §6; work plan stop rule |

**B4 authoritative wording.**

> Gate 2 formally passed its prespecified, internally locked rule, but the
> diagnostic did not demonstrate useful selective prediction of which units
> benefit from correction. Its precision was 0.093 versus a base rate of
> 0.077, and much of the apparent gain came from excluding large-gap units.
> Therefore Gate 2 is retained as a formal PASS but not interpreted as
> evidence of operationally useful benefit selection.

## C. Reproducibility and provenance

| ID | Statement | Kind | Evidence | Limitations | Source |
|---|---|---|---|---|---|
| C1 | All verdict-level quantities of Gates 2–4 reproduce under full internal recomputation (Linux, Python 3.13.18, NumPy 2.3.5) and sampled recomputation (every 50th unit; Python 3.10.12, NumPy 2.2.6). | finding | internal recomputation | **Not third-party validation.** Original Python version and platform unknown. | E005 §4 |
| C2 | Stored per-unit floats are not bit-reproducible across platforms: 416 of 6600 (Gate 2) and 31 of 5940 (Gate 3/4) units differ, from last-bit differences in input probabilities. | boundary | internal recomputation | Verdicts unaffected; cause identified, not removed. | E005 §4 |
| C3 | Analysis code was outside every lock, so code precedence over results cannot be shown for any gate. | boundary | repository history | Remedied for future work only (lock template v2). | E005 §1, E006 §7 |
| C4 | The scoped MT7.4 audit found adjacent prior art for every component (RPE sensing, CDR references, PST/KIK mitigation, reject rules, and decision-aware QEM), but no searched source combining the full frozen pipeline. | boundary, not priority | primary-source records and publisher/full-text pages | Not a systematic review; cannot support “first” or an absence claim. | `docs/literature/novelty_claim_draft.md` |

## D. Statements that must NOT be made

| Not supported | Why |
|---|---|
| "The method works", "the sensor-guided policy improves decisions", or any positive policy value | Gate 3 FAIL under both estimands; power about zero. |
| "Gate 2 successfully predicts correction benefit" or "Gate 2 shows decision relevance" without the B4 qualification | Precision 0.093 vs base rate 0.077 (E003, E006 §4). |
| "RC labels cannot sense `epsilon`" in general, or on hardware | Only the synthetic model, frozen designs, and response-free nuisance classes (A3). |
| "RC labels have zero information about `epsilon`" in a structured nuisance model | Oracle information is positive (A3). |
| Any P-amp robustness, P-amp vs P2 superiority, or hardware transfer | B3 limitations; P2 nonevaluable at Gate 1 and structurally blind at Gate 2. |
| "Validated", "independently reproduced", or "third-party verified" | Only internal recomputation exists (C1). |
| "Preregistered" | No independent timestamp exists (D6). |
| "First", or any priority claim | No systematic prior-art search has been completed (novelty draft, MT7.4 open). |
| That `B_hat` guarantees a decision-flip bound | Only the population bound A7 is proved. |

## E. Hypotheses and possible explanations (not findings)

| ID | Statement | Kind |
|---|---|---|
| E-1 | Labels can support a deployable test of `phi != 0` (licensing abstention) without supporting an estimate (licensing correction). | hypothesis; the testability part is not formally derived |
| E-2 | The Gate 3 null arises because always-correct is already near-optimal in this synthetic model (policy-lock losses: C-always 0.0079 vs issue-only 0.029), leaving almost no room for a policy. | possible explanation |
| E-3 | Under visibility loss, P-amp's 0.7% margin would be lost and Gate 1B would fail. | hypothesis (untested) |
