# Gate 3/4 development and power design lock

**Status:** owner-approved and frozen before any split-99 outcome is generated

**Entry condition:** Gate 2 PASS at commit `1e3fa3076c6da62c77fad0016d4150adf03b2653`

**Evidence class:** Part 3 development and split-99 design simulation only; no
confirmatory holdout and no hardware.

This lock implements Main Task 5 and milestone M6. It does not alter the Part
order, Gate order, primary endpoint, loss, total budget, or D1--D3.

## 1. Frozen loss, budget, and actions

The total budget is `N = 24,300` shots per unit. The primary loss remains

```text
L = 1{an issued answer is wrong}
    + 1/4 * 1{abstain}
    + 1/4 * 1{correction attempted but execution fails}.
```

A failed correction issues no answer. The action paths are:

| Action | Sensor | Initial target | Correction reserve | Final answer |
|---|---:|---:|---:|---|
| N | 2,430 | 10,934 | 10,936 charged but unused | initial target only |
| C | 2,430 | 10,934 | 10,936 | corrected rerun only |
| A | 2,430 | 10,934 | 10,936 charged but unused | none |

The target allocations are 5,467 shots per candidate initially and 5,468 per
candidate after correction. P-amp retains 18 settings of 135 shots. Classical
statevector, reference, and policy-computation time is reported separately and
does not replace the shot ledger.

## 2. Frozen deployable three-action policy

All quantities below are runtime observations, P-amp outputs, known metadata,
or constants locked here. Ideal gaps, true errors, graph identity, realized
loss, and scoring-only fields are forbidden policy inputs.

Let `g0_hat` be the initial observed candidate gap and `SE_g0` its independent
two-candidate plug-in standard error. Define the Gate-2 bound

```text
B_hat = (A_A + A_B) * |epsilon_hat|
        + (M_A + M_B) * |phi_hat|,
```

using the metadata angle sums and tagged-rotation counts from the Gate 2 lock.
The frozen Gate-2 correction predicate is true exactly when the P-amp estimate
is defined and unambiguous, either parameter clears its frozen two-sided 1.96
standard-error threshold, `g0_hat != 0`, and `|g0_hat| <= B_hat`.

The action rule is ordered and exhaustive:

1. choose **C** when the Gate-2 correction predicate is true;
2. otherwise choose **A** when P-amp is undefined or ambiguous, or when
   `|g0_hat| <= 1.96 * SE_g0`;
3. otherwise choose **N**.

Equality takes the conservative A branch. An exact observed tie therefore
cannot manufacture N or C. No graph-specific constants, learned model,
threshold search, or post-result adjustment is allowed.

## 3. Split-99 graph generator and contexts

Generate 99 deterministic connected labeled graph clusters. For each
`n in {4,5,6}`, enumerate SHA-256 candidate edge masks from
`"gate34-v1|n|candidate_index"`; accept a mask only if it is connected and has
not previously been accepted for that `n`. Take the first 33 accepted masks per
`n`, then interleave by accepted index and `n`. Cluster IDs `0..32` form the
policy-lock/power partition; IDs `33..98` form the Gate 3/4 evaluation
partition. Outcomes from the latter may not select a comparator or threshold.

Edges `(i,j)` with `i < j` are ordered lexicographically. The first
`n*(n-1)/2` digest bits, read most-significant bit first, are the inclusion
mask. Candidate indices start at zero. Interleaving order is accepted index
first and then `n = 4,5,6`; cluster IDs are assigned consecutively in that
order. The canonical unit key is
`cluster_id|beta_index|gamma_a_index|gamma_b_index|error_index`.

Every graph receives these 60 contexts:

- `beta` at all four Gate-2 values;
- gamma-index pairs `(0,1)`, `(2,4)`, and `(4,6)` from the Gate-2 gamma grid;
- error points `(epsilon,phi)` equal to `(0,0)`, `(-0.02,0)`, `(0.02,0)`,
  `(-0.04,-0.01)`, and `(0.04,0.01)`.

Thus the frozen run contains 5,940 generated units: 1,980 policy-lock/power
units and 3,960 evaluation units before exact ideal-gap exclusions.

The circuit, score, coherent-error model, P-amp estimator, D3-a correction,
NumPy PCG64 multinomial sampling, numerical ideal-tie tolerance `1e-12`, and
canonical-A sampled tie rule are inherited unchanged from the Gate 2 lock.
Seeds are the first eight bytes of
`SHA256("gate34-v1|" + unit_key + "|" + stream_name)`.

## 4. Fixed comparators and one-time selection

Retain every fixed policy:

1. **N-full:** no sensor; all 24,300 shots go to the target, 12,150 per
   candidate.
2. **N-sensor-allocation:** use 5,467 shots per candidate, ignore P-amp, and
   leave the rest charged but unused.
3. **C-always:** run P-amp and both target stages, decide from corrected data
   only; an undefined/ambiguous estimate is a failed correction with loss 1/4.
4. **A-always:** loss 1/4 on every evaluable unit.

On the 33 policy-lock graph clusters, first choose the lower-loss issue-only
comparator between N-full and N-sensor-allocation. Then choose the lowest-loss
fixed comparator among that issue-only winner, C-always, and A-always. Exact
mean-loss ties within `1e-12` use this fixed priority:
`N-full`, `N-sensor-allocation`, `C-always`, `A-always`.

The selected fixed comparator is then immutable on the 66 evaluation clusters.
All nonselected losses remain in the report.

## 5. Primary endpoint and Gate 3

For every evaluable evaluation unit,

```text
Delta_u = L_fixed,u - L_policy,u,
Delta_V = mean_u Delta_u.
```

Losses are scoring probabilities estimated with 256 scoring-only repetitions;
those repetitions are never policy inputs. Compute one mean `Delta_u` per graph
cluster, then draw 10,000 bootstrap samples of the 66 graph means with
replacement using PCG64 seed derived from `gate34-v1|cluster-bootstrap`.
The one-sided 95% lower bound is the empirical 5th percentile using the
linear-interpolation quantile.

Gate 3 passes only if the full paired `Delta_V > 0` and that lower bound is
strictly positive. It cannot be rescued by secondary endpoints or alternative
loss weights.

## 6. Gate 4 non-degeneracy

On evaluable evaluation units, an action clears the minimum frequency only if:

- it is selected on at least 5% of units; and
- it appears at least once in at least 10 of the 66 graph clusters.

Gate 4 passes only if at least two of N, C, and A clear both requirements. An
action selected only by numerical ties does not count; the report separately
counts exact observed ties.

## 7. Power analysis

After fixed-comparator selection but before inspecting evaluation outcomes,
use the 33 policy-lock cluster means as an empirical design distribution.
Generate 5,000 prospective studies of 66 clusters by resampling those means.
For each study compute

```text
mean - 1.669 * sample_SD / sqrt(66),
```

where `1.669` is the frozen one-sided 95% `t` critical approximation for 65
degrees of freedom. Estimated power is the fraction with a positive bound.
This is a design diagnostic; the actual Gate 3 decision uses the frozen cluster
bootstrap in Section 5. Report the minimum detectable positive mean under the
same approximation and the observed policy-lock standard deviation.

## 8. Missingness, multiplicity, and sensitivities

- Exact ideal-gap ties are outside the unique-top-1 population and retained as
  excluded records.
- Correction failures remain loss events; they are never dropped.
- Infrastructure failures are retained. If more than 1% of generated
  evaluation units are infrastructure-missing, or an entire graph cluster is
  missing, Gate 3 is nonevaluable and fails.
- Primary loss weights are fixed at 1/4. Loss weights 0.10 and 0.50 are reported
  only as secondary sensitivities and cannot rescue either Gate.
- Secondary endpoints are descriptive. No secondary hypothesis test supports
  a pass, so no multiplicity-adjusted confirmatory claim is made.
- No common-random-compilation diagnostic is run: P-amp contains no randomized
  compilations.

## 9. Claim boundary and execution lock

M6 can establish only development evidence for net policy value and
non-degeneracy under this synthetic model. It cannot establish confirmatory
generalization, physical-device realism, or hardware benefit.

Before any split-99 outcome is generated, commit this file with its canonical
SHA-256 manifest and checker. The execution script must require that exact
commit and refuse to overwrite existing M6 results. If either Gate fails, do
not proceed to M7 registration or a confirmatory adaptive-policy run.
