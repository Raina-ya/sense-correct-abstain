# Gate 1 design lock (M3)

**Lock date:** 2026-11-20

**Status:** frozen before any Gate 1A computation

**Evidence type:** protocol/design record; no experimental or simulation result

## 1. Change-control boundary

This lock freezes Gate 1A and the only permitted Gate 1B fallback. After its
commit, no graph, candidate angle, label rule, parameter grid, estimator,
nuisance class, budget, tolerance, control, P-amp setting, or pass condition may
change in response to Gate 1A results. A defect found later is reported and may
invalidate the affected gate; it is not silently repaired and rerun.

The authoritative mathematical specification is
`../theory/gate1_math_spec_v1.md`. M2 semantics remain authoritative for E2,
RC construction, and the conditional likelihood.

## 2. Owner decisions D4-D6

| ID | Frozen decision | Consequence |
|---|---|---|
| D4 | P-amp uses `atan2` phase estimates and equal-weight least squares. No RPE estimator and no RPE-style consistency check are implemented. | RPE full-text robustness claims are not imported. Phase ambiguity and undefined estimates are explicit failures. |
| D5 | P2 is reported only in its predecessor alarm form. | The unproved first-order `epsilon` estimator is not added after Gate 1A. P2 remains a mandatory same-budget comparator, not another adaptive branch. |
| D6 | M3 uses a Git commit and the SHA-256 manifest as an internal pre-computation lock. Independent registration is deferred to M7 before confirmatory holdout. | This record is not called a preregistration and has no claimed independent timestamp. |

## 3. Fixed budget

```text
N = 24,300 shots per decision unit
f = 0.10
n_S = f*N = 2,430 sensing shots
epsilon_min = 0.02
```

M3 does not allocate the remaining `21,870` shots between initial target and
correction reserve; that split is frozen later before Gate 2/3 evaluation and
cannot exceed `N`. The fixed-reserve semantics from D3 remain unchanged.

For Gate 1A, the sensing experiment uses all `n_S` observations under the
uniform joint label design. Exact-probability enumeration and analytic Fisher
calculations are validation views, not extra shots.

## 4. Gate 1A locked design

- Circuits, graphs, candidates, labels, grids, nuisance class, estimator,
  controls, tolerances, and pass/fail rule: `gate1_math_spec_v1.md`.
- Primary contexts: `G2-primary` and `G3-primary`, `p=1`.
- Secondary only: `G3-p2`.
- Parameter grid: the 9-by-9 Cartesian grid in the math specification.
- Root seed: `20261120`.
- Seed-key tuple:
  `(root, gate_code, context_code, parameter_index, replicate_index, stream)`.
- Gate codes: `1=Gate1A`, `2=Gate1B`; streams:
  `1=labels`, `2=shots`, `3=shuffle`, `4=optimizer_tie_break`.
- Replicate indices for any frozen shot-based convergence diagnostic:
  `0,...,199`. Exact-probability checks use no random seed.

No computation that evaluates Gate 1A rank, recovery, distances, or verdict is
authorized by this lock itself.

## 5. Complete P-amp fallback specification

P-amp is evaluated only if Gate 1A fails by its frozen criterion.

### 5.1 Circuits and settings

The reference block is

```text
B(theta) = CX(c,t) - RZ_tagged(theta)_t - CX(c,t),
```

with control in `|0>` and target in `|+>`. Freeze:

- repetitions `R(m,theta)=B(theta)^m` for
  `m in {1,4,16}`, `theta in {pi/8,pi/4}`: six circuits;
- echoes `E(m)=[B(pi/4)B(-pi/4)]^m` for `m in {1,4,16}`:
  three circuits;
- target measurement in X and Y for all nine circuits: 18 settings;
- 135 shots per setting: `18*135=2,430` shots exactly.

Negative commanded angles obey the same error law. Violation of that premise is
a model failure, not a reason to change the estimator.

### 5.2 Grid and ambiguity

P-amp uses the same 9-by-9 `(epsilon,phi)` grid as Gate 1A. Every point must
satisfy

```text
16*|epsilon*theta + phi| < pi/2
32*|phi| < pi/2
```

for the applicable repetition angle. The grid is not shrunk after evaluation.

### 5.3 Estimator

For each X/Y setting pair,

```text
u_hat = atan2(<Y>_hat,<X>_hat).
```

Subtract the known ideal phase and unwrap sequentially in `m=1,4,16`, choosing
the branch continuous with the preceding rung. The estimator is the
equal-weight least-squares solution of

```text
repetition residual = m*theta*epsilon + m*phi,
echo residual       = 2*m*phi.
```

An undefined `atan2`, ambiguous unwrap, or nonunique least-squares solution is a
failure. No RPE replacement or consistency statistic may be added after this
lock.

### 5.4 Analytic resource calculation

With 135 shots in each X and Y setting, use the conservative first-order bound
`Var(u_hat)<=1/135`. For the nine frozen design rows, equal-weight least squares
gives

```text
SE(epsilon_hat) <= 0.00709020
epsilon_min/2.8  = 0.00714286.
```

Thus the design meets the planning resource condition analytically. This is a
design calculation, not an observed recovery result or a finite-sample
coverage guarantee.

### 5.5 Gate 1B pass conditions

All are required:

1. analytic design rank two and full-rank known-reference Fisher information;
2. noiseless recovery error at most `1e-8` for both parameters at every grid
   point;
3. the analytic resource condition in Section 5.4;
4. no phase ambiguity at any grid point;
5. the same-budget P2 alarm comparator is reported;
6. no ideal target value is read.

Visibility decay, target-context mismatch, drift, asymmetric negative-angle
error, or ladder noise outside the assumed regime is reported as a failure or
limitation. P-amp is RPE-like and carries no sensor novelty claim.

## 6. Frozen outputs and signed predictions

The eventual Gate 1A report must include I1/I2/I3 tables, analytic and numerical
rank, recovery, controls, finite-separation pairs, convergence logs, and a
signed prediction-mismatch table. Before computation, the signed predictions
are:

- semantic equivalence passes for every allowed label;
- I1 for `epsilon` is zero at `phi=0`;
- logical-angle control is label blind;
- score-zero and label-shuffled controls carry no admissible label information;
- I2 may show information unavailable to I1/I3 and cannot pass the gate;
- full Gate 1A failure is a prediction, not a result;
- P-amp is predicted to have analytic rank two and to meet its ambiguity and
  resource criteria, but recovery remains uncomputed.

Every mismatch is retained. Nothing in this section authorizes computation.

## 7. Hash and lock evidence

`gate1_design_lock_manifest.sha256` contains SHA-256 hashes of every frozen
input named there. The manifest is generated and committed before Gate 1A
computation. Its Git commit is the internal lock evidence. The manifest does
not hash itself and is not an independent timestamp.
