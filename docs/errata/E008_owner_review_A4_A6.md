# Erratum E008 — Owner review of claims A4–A6 (2026-11-21)

**Append-only.** E001–E007 and every file in the v1–v3 errata manifests remain
byte-identical. For the theory-note results listed below, **this erratum
governs** the status lines in `docs/theory/three_action_theory_v1.md`. No frozen
verdict changes.

**Reviewed material:** `docs/theory/three_action_theory_v1.md` and
`docs/contracts/decision_problem_v1.md` at commit `d6814a9`.

**Review supplied by the owner:**
[`../theory/A4_A6_rigorous.tex`](../theory/A4_A6_rigorous.tex) and
[`../theory/A4_A6_rigorous.pdf`](../theory/A4_A6_rigorous.pdf) (5 pages). Both are
byte-identical to the files the owner supplied on 2026-11-21. The `.tex` file
compiles cleanly and its text matches the PDF exactly.

**Owner verdict:** the statements of T1, C1, C2, L1, T2, D1, and P2 stand
unchanged. Implicit assumptions are made explicit. Example E1 has a gap and is
corrected. Example E2's status is updated.

## 1. Status after review

| Result | Ledger row | Status before | Status now |
|---|---|---|---|
| T1 three-action risk identity | A4 | draft | **proved, owner-reviewed**; assumption S3 (stage 2 as a potential outcome, independent of the policy's private randomization given `x`) added. Independence is used only in the C term. |
| C1 reduction to the predecessor's Eq. (6) | A4 | draft | **proved, owner-reviewed** (the Eq. (6) numbering was checked against the predecessor's compiled paper in commit `e8f002c`) |
| C2 Chow-type rule | A4 | draft | **proved, owner-reviewed**; requires a regular conditional probability (exists on standard Borel spaces); both actions are optimal on the tie set `e_N = lambda_A`. Attribution of the exact Chow form still **unverified**. |
| L1 blindness lemma | A5 | draft | **proved, owner-reviewed**; "equal stage-1 law" includes the metadata `m` (the policy is `pi(m, X_1)`), so L1 applies only to states of the **same unit** that differ in latent parameters or responses |
| Wrong-action form | A5 | draft | **proved, owner-reviewed, strengthened**: for equal laws, `P_theta(a != a_0) + P_theta'(a != a_1) >= 1` for **any** `a_0 != a_1`; no optimality hypothesis is needed |
| T2 finite-pilot bound | A5 | draft | **proved, owner-reviewed**; `Gamma_min` needs to hold only a.e. on `{min(p_0, p_1) > 0}`. KL may be taken in either direction (chosen once), giving `n >= log(1/(2 beta)) / min(KL_01, KL_10)` for `beta < 1/2`. |
| D1 allocation decomposition | A6 | corrected (MT1 owner-review revision, `e8f002c`) | **proved, owner-reviewed**; `K >= 0` |
| P2 honest collapse | A6 | corrected and narrowed | **proved, owner-reviewed**; assumption S4(b) added: whenever the policy can take C, the always-correct comparator exists and uses the **same** correction procedure (`kappa`, recalibration rule, `n_C`, `delta_C`) as the policy's path C. Strict version: `Delta_V < 0` unless every action with positive weight attains `R_fix`. |
| Example E1 (uses L1) | — | "proved (draft) within the direct-phase model" | **gap; as stated, L1 does not apply.** Corrected in §2. |
| Example E2 (uses L1) | — | conditional | first condition **discharged conditionally** by Lemma S1′(2)/(3); second condition **open** (§3) |

## 2. Correction of Example E1

**Gap.** E1 shows that `(epsilon, phi)` and
`(epsilon', phi + (epsilon - epsilon') a_S)` give the same **sensor** law. L1
needs equal **stage-1** laws, and stage-1 evidence also contains the initial
target data `X_T0` (contract §1.3). E1 deliberately chooses the pair so that the
candidate-gap biases differ, so the two `X_T0` laws differ in general, and L1
does not apply as stated.

**Valid repairs.**

1. **Sensor-only policies.** Restrict to policies whose action is a function of
   `X_S` (and `m`) only. Then L1 applies with `X := (m, X_S)`.
   - Additional point (Claude, checked): `delta_0` depends on `X_T0`, which is
     not a function of `X_S`. The N-loss must therefore be read as the
     conditional probability `l_N(theta, x_S) = P_theta(delta_0 != k* | X_S = x_S)`.
   - This is admitted by the theory note, which allows `l_N` to be a
     conditional probability in `[0, 1]` (Remark 1, adaptive-reallocation
     variant). The convex-combination argument of L1 is unchanged.
   - Under the frozen design, `X_S` and `X_T0` come from separate circuits
     and are independent given the state, so `l_N` does not depend on `x_S`.
2. **Full stage-1 evidence.** Keep `X_T0` and use T2 with `1 - TV` computed on
   `(X_S, X_T0)`. Only the target shots then separate the two states, and
   (T2d) gives the `n_T0` needed for reliable action selection.

The same caveat applies to any use of L1 in which only the sensor marginal is
shown to agree.

## 3. Example E2 after Lemma S1′

- **First condition** (two states in the frozen nuisance class with identical
  label-resolved laws): discharged by Lemma S1′(2) under N-loc and S1′(3) under
  N-free (E007). This holds **provided** the stage-1 evidence consists only of
  label-resolved draws of those candidate circuits, with target shots counting
  as one label pattern.
  - Under N-free the alternative state is the translate
    `R'_c = R_c(. + (epsilon_0 - epsilon') theta_c)`. Its ideal response at
    `theta_c`, and hence `k*`, may differ from the original.
  - Under the per-context shared reading of §5.3, the rescaling construction
    S1″ (E007 §3.2, still a draft) plays the same role.
- **Second condition** (the two states have different optimal actions):
  **open**.

## 4. Metadata-only gap (owner suggestion recorded; no design change)

If comparators were selected per prespecified metadata stratum, the P2 proof
would apply within each stratum. Averaging over strata, it would give
`Delta_V <= 0` for every policy that depends on metadata only through those
strata.

This changes the comparator definition, which is part of the primary-endpoint
machinery. It is therefore recorded as an option for **future** studies under
lock template v2. It is not applied retroactively to the frozen Gate 3/4 study.

## 5. Remaining reviews

- **S1″** (E007 §3.2): pending. E007 exists only in local commit `630ef91`,
  which was not yet pushed when the owner reviewed `d6814a9`. E007 has been
  sent to the owner directly, with a typeset review sheet for S1″
  ([`../theory/S1doubleprime_review_draft.pdf`](../theory/S1doubleprime_review_draft.pdf),
  source `.tex` alongside). The sheet gives the full proofs of the exceptional
  points (`epsilon' = -1` in the shared nonlinear class, iff `P_1 = P_2`;
  `epsilon' = 0` in the shared first-order class) and of the visibility/offset
  enlargement. Its status is draft, owner review pending.
- Attributions still unverified: the exact Chow (1970) rule form, and the
  Tsybakov lemma locations. Neither affects any proof.
