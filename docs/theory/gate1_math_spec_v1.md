# Gate 1 mathematical specification v1

**Status:** frozen at M3, before any Gate 1A computation. This document fixes
the estimands, nuisance boundary, information decomposition, controls, and
decision rule. It contains analytic predictions and design calculations only;
it contains no Gate 1 result.

## 1. Frozen experiment

The primary E2 and RC semantics are those in `e2_semantics_v1.md` and
`rc_construction_v1.md`. For candidate/context `c`, tagged location `ell`,
label vector `t`, sign `s_ell(t)`, and bitstring `b`, the implemented likelihood
kernel is

```text
p_Q(b | c,t,epsilon,phi)
 = Tr[M_b U_{c,t}(epsilon,phi) rho U_{c,t}^dagger(epsilon,phi)],
```

where each tagged physical rotation is

```text
RZ((1+epsilon) s_ell(t) theta_{c ell} + phi).
```

Equivalently, after exact Pauli-frame cancellation, every tagged logical
rotation is

```text
RZ(theta_{c ell} + epsilon theta_{c ell} + s_ell(t) phi).
```

The target parameter is `psi=(epsilon,phi)`. Label draws are parameter
independent and the complete joint label vector is retained.

## 2. Frozen circuit contexts

| ID | Graph and state | Cost structure | Mixer and measurement | Role |
|---|---|---|---|---|
| `G2-primary` | two qubits, edge `(0,1)`, initial `|++>` | `p=1`, one tagged cost block | `beta=pi/8`, computational-basis bitstring | enumerable primary semantic check |
| `G3-primary` | three qubits, path `(0,1),(1,2)`, initial `|+++>` | `p=1`, two tagged cost blocks in listed edge order | `beta=pi/8`, computational-basis bitstring | primary nontrivial context |
| `G2-score-zero` | as `G2-primary` | as `G2-primary` | `beta=0`, computational-basis bitstring | analytically phase-insensitive control |
| `G3-p2` | as `G3-primary` | `p=2`, the same edge order in each layer | `beta=(pi/8,pi/8)`, computational-basis bitstring | prespecified secondary rank check only |

Angles below are the tagged `RZ` angles, so no hidden factor-of-two convention
is allowed:

- single-angle control: `theta=pi/4`;
- same-angle pair: `(pi/4,pi/4)`;
- distinct-angle pair: `(pi/8,pi/4)` in that order.

The `p=2` context cannot rescue a negative `p=1` Gate 1A result. Graphs,
candidate angles, mixers, measurement, and edge order cannot be changed after
this lock in response to results.

## 3. Label design

Every tagged block uses the 16 two-qubit Pauli labels and correction map frozen
in `rc_construction_v1.md`. Labels are uniform and independent across tagged
locations in the primary design. Analytic enumeration weights every joint
label vector equally: 16 patterns for `G2` and 256 for the two-location `G3`
contexts. A budgeted shot realization samples the same joint distribution and
records the complete vector; labels are never reduced to a marginal sign
before likelihood evaluation.

The frozen label-shuffled control applies one deterministic permutation to the
association between complete label vectors and outcome records, separately
within each context and parameter point. It preserves label counts and cannot
use outcomes when selecting the permutation.

## 4. Parameter grid and finite-separation pairs

The primary Cartesian grid is

```text
epsilon, phi in {-0.04,-0.02,-0.01,-0.005,0,0.005,0.01,0.02,0.04}.
```

No point may be removed after inspection. Boundary and zero points are reported
explicitly. `epsilon_min=0.02` is the smallest effect used for the Gate 1B
resource criterion; smaller grid values test local behavior and are not a new
power target.

The frozen hard-pair construction uses `theta_ref in {pi/8,pi/4}`:

```text
z0 = (epsilon=0, phi=0),
z1 = (epsilon=+epsilon_min, phi=-epsilon_min*theta_ref),
z2 = (epsilon=-epsilon_min, phi=+epsilon_min*theta_ref).
```

All constructed pairs are retained. If a pair does not change the optimal
action under the frozen decision contract, it is reported as a failed
action-relevant construction rather than replaced.

## 5. Information sources

### 5.1 I1: retained-label contrast

I1 is computed from conditional label contrasts without an ideal target
response. At `phi=0`, frame covariance proves

```text
p(b | c,t,epsilon,0) = p(b | c,t',epsilon,0)
```

for all labels `t,t'`; hence the I1 score and Fisher information for `epsilon`
are exactly zero. At nonzero `phi`, the label score is evaluated without
promoting response slope information to known input.

### 5.2 I2: oracle diagnostic

I2 evaluates the exact quantum kernel with the ideal state, measurement, and
response treated as known. This is permitted only because the frozen 2–3 qubit
contexts are enumerable. It is labeled oracle/diagnostic everywhere and cannot
contribute to Gate 1A pass, parameter recovery, or an action.

### 5.3 I3: deployable profile information

The primary deployable nuisance class treats each target context's ideal
outcome distribution and its local response directions as unknown, subject
only to normalization, positivity, and the shared frozen circuit/label design.
Visibility and label-independent offset are also nuisance quantities. No
coefficient is supplied by ideal target simulation.

Efficient scores are obtained by projecting the `(epsilon,phi)` scores onto the
orthocomplement of this nuisance tangent space. This saturated local nuisance
model is primary because the runtime policy has no justified transferable
response curve. A structured Fourier/QAOA response computed from the small
circuits is reported only under I2 unless its coefficients are fitted solely
from the same runtime observations under a separately frozen deployable model;
no such additional model is admitted at M3.

## 6. Fisher and rank calculation

For each information source, form the corresponding score matrix `S` and
weighted Fisher matrix

```text
I = sum_i n_i E[S_i S_i^T].
```

Report analytic rank, numerical rank, eigenvalues, and condition number. A rank
claim must name I1, I2, or I3. Numerical rank uses

```text
tau_rank = max(1e-12, 1e-10 * largest_singular_value).
```

Full numerical rank requires every required singular value to exceed
`tau_rank`; the condition number is then reported but is not a separate rescue
criterion. Score-zero points, boundary points, phase aliases, and multiple
optima are failures for that design, not discarded observations.

## 7. Frozen estimator and recovery check

The Gate 1A deployable estimator is the profile maximum-likelihood estimator
under the I3 nuisance class. It conditions on complete labels and may use only
runtime outcomes, frozen circuit metadata, and frozen constants. It may not
read the ideal target response, I2 coefficients, true parameters, or the error
model label.

The exact-probability recovery check uses the full grid and deterministic starts

```text
(epsilon_start,phi_start) in {-0.04,0,0.04}^2.
```

Bounds are `[-0.05,0.05]^2`; maximum iterations are 1,000; gradient tolerance
is `1e-10`; parameter-step tolerance is `1e-12`. All starts must reach the same
identified solution. Absolute recovery tolerance is `1e-8` per parameter. A
flat profile, nonunique solution, boundary solution for an interior truth, or
optimizer disagreement is a failure, not averaged away.

## 8. Controls

The following controls are mandatory and reported separately:

1. `phi=0` balanced-label identity;
2. one effective angle;
3. same-angle candidate pair;
4. distinct-angle candidate pair;
5. `G2-score-zero` measurement control;
6. deterministic label shuffle;
7. matched `epsilon=phi=0` control;
8. logical-angle E2 control, in which labels are blind by construction;
9. I2 oracle diagnostic beside I1 and I3, never merged with them;
10. `p=2` secondary calculation, never used to rescue primary `p=1`.

Matrix equivalence uses absolute tolerance `1e-12`. Analytic zero predictions
use absolute tolerance `1e-12`. Differences below tolerance are reported as
numerically consistent with zero, not proved zero by computation.

## 9. Gate 1A decision rule

Gate 1A passes only if, in at least one frozen primary `p=1` deployable design,
I1 plus admissible I3 has rank two for `(epsilon,phi)`, exact-probability
recovery meets the frozen tolerance at every required grid point, and all
semantic and negative controls agree with their signed predictions. I2 cannot
contribute.

Gate 1A fails under any failure condition in the work plan. A label-based test
of `phi!=0` without an estimate of `epsilon` is recorded as partial information
and remains a Gate 1A failure for correction. No design, nuisance family, grid,
or tolerance is replaced after inspection.

## 10. Finite-separation report

For every frozen hard pair, report total variation, Hellinger distance, KL
divergence, the corresponding two-point action-error lower bound, and whether
the pair implies different Bayes actions. Bounds are evaluated at the frozen
sensing budget. Loose, identical-action, or physically irrelevant pairs remain
in the signed mismatch/failure table.
