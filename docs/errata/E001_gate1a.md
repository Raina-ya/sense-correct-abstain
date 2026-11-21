# Erratum E001 — Gate 1A (2026-11-21)

**Affected frozen artifacts (unchanged):** `tools/run_gate1a.py`,
`results/gate1a/gate1a_results.json`, `docs/results/gate1a_report.md`.

**Frozen verdict:** FAIL, route to Gate 1B. **Status:** the verdict **stands**.
Its valid basis is Lemma S1 below together with the frozen recovery
requirement, not the entries of the frozen report.

## 1. Defects

| # | Defect | Evidence |
|---|---|---|
| 1 | **I3 was not computed.** The specification (§5.3, §6) requires efficient scores projected onto the orthocomplement of the nuisance tangent space. The runner appends a constant: `ranks["I3"].append(0)`. | `tools/run_gate1a.py`, `summarize_information` |
| 2 | **Profile recovery was not attempted.** The specification (§7) requires a profile MLE from 9 deterministic starts, with bounds and tolerances. The runner writes `"recovered": 0`, `"failed_nonunique"` without running an optimizer. The report sentence "No frozen primary design recovered (epsilon, phi) at any of the 81 required grid points" describes a computation that was never performed. | same |
| 3 | **The verdict is a literal.** The runner writes `"verdict": "fail"`; it is not derived from computed quantities. | `main` |
| 4 | **Control statuses are literals.** These control statuses are fixed strings, not computed results: single-angle ("failed_identification_as_predicted"), same-angle, distinct-angle, matched null ("passed_label_invariance"), and logical-angle ("passed_label_blindness"). The logical-angle property is tested in `tests/test_gate1.py`, but not in the run. Only the `phi = 0` invariance and the score-zero oracle matrix were computed. | `controls` |
| 5 | **"I1" is an oracle quantity.** The reported I1 is the conditional-minus-marginal Fisher information (the Vyas chain-rule term). It uses the exact `P(label \| bitstring)` under the known response, not the specification's I1 (label contrasts with the response unknown). Its ranks (`{1: 9, 2: 72}` in every design) are therefore known-response diagnostics. | `gate1.information_matrices` |
| 6 | **Unrecorded prediction mismatch.** The single-angle control is reported as "failed identification as predicted (epsilon-phi phase confounding)". The computed I1 and I2 for the single-angle design have rank 2 at 72 and 81 of 81 points, respectively: with known response, the label sign `s` separates `phi` from `epsilon*theta`. The direct-phase confounding prediction does not apply to label-resolved data. The signed mismatch table lists this as "Match". | `results/gate1a/gate1a_results.json` |
| 7 | **Finite-separation pairs not at budget.** Specification §10 requires TV, Hellinger, KL, and the two-point bound at the frozen sensing budget. The report gives single-shot TV only (Le Cam lower bound about 0.497–0.498) and omits KL and Hellinger. | report table |
| 8 | The label-shuffle control was nonevaluable (already disclosed in the frozen report). | — |

## 2. Analytic basis for the verdict

**Lemma S1 (zero deployable information for `epsilon` at `phi = 0`).** Status:
proved (draft, owner review pending).

Consider any frozen Gate 1A design and any nuisance class that contains, for
each candidate circuit, an unknown label-independent outcome distribution
constrained only by normalization and positivity (true of the frozen class in
§5.3). Then at every grid point with `phi = 0`:

1. `epsilon` is not identified; and
2. its efficient information is zero.

*Proof.* At `phi = 0`, frame covariance (proved at M2) gives, for every label
pattern `t` of candidate `c`, the same outcome law `F_c((1+epsilon) theta_c)`.
For fixed data the law is therefore one distribution per candidate. The
nuisance class contains every distribution per candidate, so `(epsilon, eta)`
and `(epsilon', eta')`, with `eta'` chosen to reproduce the same per-candidate
distribution, are observationally equivalent. Hence (1).

For (2), the score of `epsilon` at `phi = 0` is `theta_c dF_c/du`, which is
the same for every label of candidate `c` and sums to zero over outcomes. It
therefore lies in the nuisance tangent direction of the unknown
label-independent distribution, and its projection onto the orthocomplement
is zero. ∎

**Consequence.** No deployable estimator can recover `epsilon` at the nine
`phi = 0` points of the frozen grid. The frozen pass rule requires recovery
"at every required grid point" (specification §9), so Gate 1A fails under
every admissible reading of the nuisance class. Routing to Gate 1B is valid.

**Deterministic check** (`tools/audit_gate1a_efficient_information.py`,
`results/errata/gate1a_efficient_information.json`). At `phi = 0`, the largest
efficient `epsilon` information over all contexts and designs is
`6.8e-21`/shot (numerically zero). The oracle full information at the same
points is `0.24–0.62`/shot.

## 3. The frozen nuisance class is ambiguous

Specification §5.3 calls the class "saturated" but defines it through "local
response directions". The two readings differ.

| Reading | `epsilon` efficient info | `phi` efficient info | Rank counts over 81 points |
|---|---|---|---|
| **Fully saturated:** every label-sign-class distribution free whenever `phi != 0` | 0 everywhere | 0 at `phi != 0` (the model is saturated there); positive but non-regular at `phi = 0` (local information without global identification) | 72 × rank 0, 9 × rank 1 (all designs; analytic) |
| **Literal first-order:** unknown distribution plus first-order directions; second-order response terms not nuisance | 0 at `phi = 0`; in G3 up to `3.5e-6`/shot at `phi != 0` | positive at `phi = 0`; in G3 up to `2.3e-2`/shot at `phi != 0` | G2: 72 × 0, 9 × 1. G3 single/same: 45 × 1, 36 × 2. G3 distinct: 27 × 1, 54 × 2 (computed) |

- Under the literal reading, the residual G3 information comes from
  second-order (interaction) response terms, which are not deployably known.
  Even taken at face value, `3.5e-6`/shot gives `SE(epsilon_hat) >= 1/sqrt(2430
  × 3.5e-6) ≈ 11` at the frozen budget.
- The frozen report's "I3 rank 0 at all 81 points" is wrong under **both**
  readings at the nine `phi = 0` points, where the `phi` information is
  positive. It is also wrong under the literal reading at the G3 `phi != 0`
  points.
- None of this changes the verdict (Lemma S1). Any future identifiability
  study must specify its nuisance class unambiguously and must include the
  runner code in the lock (E005).

## 4. Finite-separation pairs at the frozen budget

`tools/audit_gate1a_pairs_budget.py` → `results/errata/gate1a_pairs_at_budget.json`.
It applies exact product identities (`BC_n = BC_1^n`, `KL_n = n KL_1`) to the
stored single-shot quantities with `n = 2430`.

| Context | `theta_ref` | `KL_n` | `TV_n` upper bound | Equal-prior two-point error lower bound |
|---|---:|---:|---:|---:|
| G2 | π/8 | 0.150 | 0.269 | 0.232 |
| G2 | π/4 | 0.594–0.606 | 0.509 | 0.185 |
| G3 | π/8 | 0.279–0.280 | 0.361–0.362 | 0.217 |
| G3 | π/4 | 0.514–0.575 | 0.475–0.502 | 0.187–0.194 |

These distances use the **oracle** law (known response), so the bounds hold
for any deployable procedure as well. At the frozen budget, no procedure can
distinguish these pairs with equal-prior error below about 0.19.

Action relevance remains nonevaluable (no action map was frozen), so these are
statistical, not action-level, lower bounds.

## 5. Corrected reading of the frozen report

| Frozen entry | Correct reading |
|---|---|
| "I1 rank counts" | Known-response label-information diagnostic (oracle), not the specification's I1. |
| "I3 rank counts {0: 81}" | Not computed. See §3 for the correct values under each reading. |
| "Profile recovery 0/81" | Not attempted. Recovery is impossible at the nine `phi = 0` points by Lemma S1. |
| Single-angle control "Match" | Mismatch: label-resolved data are not single-angle confounded when the response is known. |
| Finite-pair Le Cam bound ≈ 0.498 | Single-shot only. At budget, the lower bound is 0.185–0.232. |
| Verdict FAIL | Stands, on the basis of Lemma S1 and the frozen recovery rule. |
