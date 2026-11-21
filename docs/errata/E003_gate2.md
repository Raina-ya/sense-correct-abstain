# Erratum E003 — Gate 2 (2026-11-21)

**Affected frozen artifacts (unchanged):** `docs/freeze/gate2_dev_design.md`,
`tools/run_gate2.py`, `src/sense_correct_abstain/gate2.py`,
`results/dev/gate2_results.json`, `docs/results/gate2_report.md`.

**Frozen verdict:** PASS, route to Gates 3/4. **Status:** the verdict
**stands formally**: the frozen rule met the frozen criterion, and that is not
revisited. The scientific reading of the pass is **narrowed** (§6).

## 1. Deviations from the program plan (not recorded at the time)

The program plan's Gate 2 row requires a rule that predicts the sign of
correction benefit better than its frozen baseline "with a prespecified
uncertainty bound", with the "exact metric and margin ... frozen in Part 1
after power analysis". The Gate 2 lock deviated in three ways.

1. **No uncertainty bound.** The pass statistic is the minimum of eleven
   leave-one-graph-out improvements. The lock itself calls it "not a
   confirmatory confidence interval". It ignores shot-noise and scoring-noise
   uncertainty and treats 3726 units as independent, although each circuit
   appears at up to 15 error points.
2. **No power analysis**, and the metric and margin were frozen in Part 2 (the
   Gate 2 lock), not in Part 1.
3. **The margin rationale is about resolution, not relevance.** "With at least
   20 units in each class, a single-class accuracy change below 0.05 is no
   more than one unit" is a statement about granularity, not practical
   importance.

These deviations could not be recorded in the program plan, because the plan
is hashed by the M3 lock (E005). They are recorded here.

## 2. Baseline

The frozen baseline predicts the constant majority class, so its balanced
accuracy is exactly 0.5 by construction. Any statistic positively associated
with the label beats it. The baseline does not test whether the transfer rule
adds decision information beyond detecting that an error is present.

## 3. Selectivity (EXPLORATORY, post hoc)

`tools/audit_gate2_diagnostics.py` → `results/errata/gate2_diagnostics.json`.
These diagnostics were specified after the verdict was known. They cannot
change or support it.

| Quantity (evaluation partition, 3726 units) | Value |
|---|---|
| Units the frozen rule predicts positive | 2932 (78.7%) |
| Sensitivity / specificity | 0.948 / 0.227 |
| Precision vs base rate | 0.093 vs 0.077 |
| Balanced accuracy: frozen rule | 0.587 |
| Balanced accuracy: significance condition alone | 0.522 |
| Balanced accuracy: `\|g0_hat\| <= B_hat` condition alone | 0.596 |
| Balanced accuracy: oracle indicator `(epsilon, phi) != 0` | 0.512 |
| Balanced accuracy within units of intermediate no-action accuracy (0.02–0.98) | 0.552 (specificity 0.155) |
| Clearly harmed units (benefit < −2 MC s.d.) predicted positive | 85 of 91 |

**Reading.** The gain over 0.5 comes mainly from the gap-bound condition. It
excludes large-gap units, where no-action accuracy is already about 1 and a
positive benefit is nearly impossible. The rule does not selectively identify
the units that benefit from correction.

## 4. Label noise

The binary label is `benefit > 0`, where benefit is the difference between two
**independent** 256-replicate Monte Carlo accuracy estimates. When both
accuracies are intermediate, the sign is close to a coin flip.

| Quantity | Value |
|---|---|
| Positive labels within 2 Monte Carlo s.d. of zero | 126 of 287 |
| Matched-null units with a positive label | 13 of 250 |
| Matched-null units of intermediate accuracy with a positive label | 9 of 18 |

The selection probabilities could have been computed exactly (by discrete
convolution of the score distributions) or with common random numbers across
actions. Neither was done.

**Estimand note.** The label is the *unconditional* unit-level benefit. It is
not conditioned on the realized initial run that the rule sees. That matches
the frozen design, but it is not the decision-time quantity used in Gate 3.

## 5. The P2 comparator is structurally blind on half of the units

The frozen rounding rule maps `2*beta` to the nearest multiple of `pi/2`,
rounding halfway cases toward zero. For `beta in {pi/16, pi/8}` the twin mixer
therefore becomes the identity, so every twin outcome distribution is
independent of the cost phases and of `(epsilon, phi)`.

**Deterministic check:** across 6600 twin distributions, the largest
difference between the noisy and ideal twin is `1.1e-16`. P2 is blind on
**3300 of 6600** generated units by construction, so its balanced accuracy of
0.522 is partly a design artifact. There is no fair same-budget comparator
evidence.

## 6. `B_hat` is a heuristic, not a bound

The lock calls `B_hat = (A_A + A_B)|epsilon_hat| + (M_A + M_B)|phi_hat|` an
"auditable first-order instability bound".

- **Analytic (proved, draft):** each tagged `RZ(theta_i)` enters a candidate's
  expected normalized score `E` as a degree-1 trigonometric polynomial
  `a + b cos theta_i + c sin theta_i`. Hence `|dE/dtheta_i| <= sqrt(b^2+c^2) =
  (range of E in theta_i)/2 <= 1/2`.
- To first order, therefore, `|Delta g| <= (1/2) sum_i (|epsilon||theta_i| +
  |phi|)` over both candidates, which is `B/2` evaluated at the true parameters.
- So `B_hat` is twice a first-order bound evaluated at the estimates. It is
  not a bound beyond first order, and it does not account for estimation
  error. It should be described as a conservative first-order heuristic.

## 7. Minor items

- The ideal-tie tolerance `1e-12` used in code is not stated in the design
  text. It is consistent with the contract's numerical-equality rule.
- 1695 of 6600 units (25.7%) were exact ideal-gap ties. The population was not
  pre-screened for structural degeneracy.
- Bit-level reproduction is platform dependent: 416 of 6600 units differ in at
  least one stored float when recomputed. No verdict-relevant field differs
  (E005).

## 8. Narrowed claim

> In the frozen synthetic development population, the frozen P-amp rule flags
> almost every non-null, not-large-gap unit. Its balanced-accuracy gain over a
> constant baseline met the frozen Gate 2 criterion. It does not selectively
> predict which units benefit from correction (precision 0.093 against a base
> rate of 0.077).

Any statement that Gate 2 established "decision relevance" must carry this
qualification.
