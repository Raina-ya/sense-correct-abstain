# Gate 2 development design lock

**Status:** frozen before generation or inspection of Gate 2 development outcomes

**Route:** Gate 1B PASS; P-amp is the sole primary sensor
**Evidence class:** development-only synthetic noisy simulation

This lock implements Main Task 4 without changing the Part order, Gate order,
or primary endpoint. Gate 2 asks only whether a deployable P-amp rule predicts
the sign of correction benefit. It does not test net fixed-budget value; that is
reserved for Gates 3 and 4.

## 1. Unit and target

A unit is a graph, QAOA angle pair, coherent-error point, and shot-noise seed.
Each unit contains two candidate `p = 1` QAOA circuits and the observations
available before action selection.

The target circuit starts in `|+>^n`, applies one cost layer containing
`RZZ(2 * gamma)` on every graph edge, then applies `RX(2 * beta)` on every
qubit and measures in the computational basis. The score of a bitstring is its
cut size divided by the number of edges. A candidate gap is expected normalized
cut score of canonical candidate A minus candidate B; the higher score is the
ideal top candidate. The coherent error applies only to the central tagged
`RZ(theta)` in each compiled `RZZ(theta)` block, as fixed by D1.

- Graph strata: edge-2, path-3, triangle-3, path-4, cycle-4, star-4,
  complete-4, path-5, cycle-5, and star-5.
- Mixer angles: `beta in {pi/16, pi/8, 3*pi/16, pi/4}`.
- Candidate cost-angle pairs are adjacent pairs and pairs separated by two
  positions in `gamma in {pi/16, 2*pi/16, ..., 7*pi/16}`. Candidate order is
  canonical and may not be changed using outcomes.
- Error grid: `epsilon in {-0.04, -0.02, 0, 0.02, 0.04}` and
  `phi in {-0.01, 0, 0.01}`.
- The compiled tagged cost rotation obeys the frozen synthetic model
  `theta -> (1 + epsilon) * theta + phi`.
- Every generated unit, including ties, failures, zero-signal cases, and
  undefined estimates, remains in the artifact.

The ideal candidate gap, true parameters, and realized correction benefit are
available only to the scoring layer. Policy features may not contain them.

## 2. Deterministic split and seeds

The canonical unit key is
`graph|beta_index|gamma_a_index|gamma_b_index|epsilon_index|phi_index`.
Its SHA-256 digest determines the split before simulation:

- first digest byte `0..63`: rule-development partition;
- first digest byte `64..255`: out-of-sample development evaluation.

Shot-noise seeds are the first eight bytes of
`SHA256("gate2-v1|" + unit_key + "|" + stream_name)`, interpreted as an
unsigned big-endian integer. Streams for P-amp, initial target, corrected
target, P2, and scoring are separate. There is no confirmatory or holdout data
in M5.

## 3. Fixed budget ledger

The total budget remains `N = 24,300` shots per unit.

| Component | Shots | Rule |
|---|---:|---|
| P-amp or same-budget P2 sensing | 2,430 | frozen Gate 1 share |
| initial target pair | 10,934 | 5,467 per candidate |
| correction reserve | 10,936 | 5,468 per candidate |
| Total | 24,300 | fixed reserve; no adaptive reallocation |

The no-action path does not use the correction reserve, but the reserve remains
charged. The correction path uses only the corrected rerun for its final
answer; it does not pool initial and corrected target counts.

## 4. Primary P-amp transfer rule

P-amp uses the frozen 18-setting estimator. Let `g0_hat` be the initial
observed candidate gap. For candidate `j`, let `A_j` be the sum of absolute
tagged ideal rotation angles and `M_j` the number of tagged rotations, both
computed from circuit metadata. Define the auditable first-order instability
bound

```text
B_hat = (A_A + A_B) * |epsilon_hat|
        + (M_A + M_B) * |phi_hat|.
```

The rule predicts positive correction benefit exactly when all conditions hold:

1. the P-amp estimate is defined and its phase-unwrapping checks pass;
2. `|epsilon_hat| > 1.96 * SE_epsilon` or
   `|phi_hat| > 1.96 * SE_phi`;
3. `|g0_hat| <= B_hat`;
4. the initial candidate gap is not an exact tie.

Otherwise it predicts nonpositive correction benefit. Equality in conditions
2 or 3 takes the conservative nonpositive branch. This is a sufficient alarm
for possible decision instability, not a proof that correction helps. Its
failure to predict benefit is a valid Gate 2 failure and may not be repaired by
post hoc thresholds.

## 5. Outcome and scoring

For each unit, the scoring layer computes the probability of selecting the
ideal top candidate under no action and under D3-a recalibration followed by a
full rerun. It uses 256 scoring-only shot-noise repetitions per action, with
seeds derived by appending `|replicate_index` to the scoring stream name. These
repetitions label the unit and are never policy features. D3-a changes every
commanded tagged cost angle `a` to
`a' = (a - phi_hat) / (1 + epsilon_hat)`; mixer angles are unchanged. The
binary label is positive only when

```text
Pr(correct selection after recalibration)
  - Pr(correct selection with no action) > 0.
```

An ideal-gap tie makes the unit nonevaluable for the binary Gate 2 score but it
remains reported. A numerical equality in benefit is nonpositive. The report
also retains candidate-gap bias, flip status, benefit magnitude, estimator
failure, model-transfer failure, and resource failure as separate fields.

## 6. Frozen no-information baseline and Gate 2 metric

The no-information baseline predicts the majority benefit-sign class in the
rule-development partition; a tie predicts nonpositive. The threshold-free
primary metric is balanced accuracy on the out-of-sample development partition.
If either class has fewer than 20 evaluable units, Gate 2 is nonevaluable and
therefore fails.

For graph-level uncertainty, compute balanced-accuracy improvement over the
frozen baseline on the full evaluation set and after leaving out each of the
ten graph strata. Define the robustness lower bound as the minimum of those
eleven improvements.

Gate 2 passes only if:

```text
full improvement > 0
and robustness lower bound >= 0.05.
```

The `0.05` margin was fixed as a minimum practically relevant improvement, not
estimated from outcomes. With at least 20 units in each class, a single-class
accuracy change below `0.05` is no more than one unit and is not treated as
meaningful. This is a development robustness criterion, not a confirmatory
confidence interval and not the Part 3 power analysis.

## 7. Same-budget P2 comparator

P2 is a comparator, not a third sensor branch. For every target candidate,
replace each cost rotation `2 * gamma` and mixer rotation `2 * beta` by the
nearest multiple of `pi/2`; exact halfway cases round toward zero. This makes
the twin Clifford. The twin's ideal normalized-cut gap is computed from the
classically tractable twin only. Split the 2,430 sensing shots equally between
the two twin candidates, assigning the odd remainder to canonical candidate A.

Define

```text
P2_alarm = |observed twin gap - ideal twin gap|.
```

P2 predicts positive correction benefit when the estimate is defined,
`P2_alarm > 1.96 * SE_twin_gap`, and `|g0_hat| <= P2_alarm`; equality takes the
nonpositive branch. Score it with the same outcome, baseline, partitions,
metric, class-count rule, and leave-one-graph-out robustness bound. P2 cannot
change the Gate 1 route and cannot rescue a failed primary P-amp Gate 2 result.

## 8. Controls and claim boundary

- Matched nulls: `epsilon = phi = 0`.
- Decision-insensitive controls: metadata bound `A_A + A_B = 0` if generated,
  ideal-gap ties, and zero realized correction benefit.
- Misspecification control: scoring-only asymmetric negative-angle error. It is
  reported separately and cannot contribute to a pass.
- Graph identity, error labels, ideal gaps, true parameters, and scoring-layer
  fields are forbidden policy features.
- No machine learning, threshold search, graph-specific rule, replacement
  target, or post-inspection change is allowed.
- The optional common-random-compilation diagnostic is not run in M5 because
  the selected P-amp route contains no randomized compilations.

Passing Gate 2 would establish development-only decision relevance in this
synthetic model. It would not establish positive net value, action
non-degeneracy, confirmatory performance, device realism, or hardware benefit.

## 9. Execution lock

Before any Gate 2 outcome is generated, commit this file together with a
canonical SHA-256 manifest and a checker. The execution script must require
that exact lock commit and refuse to overwrite existing development results.
