# Conditional likelihood v1

**Status:** analytic M2 specification, 2026-11-20. This derives the likelihood
from the frozen dressed circuit. It contains no fitted parameter, simulated
result, or Gate-1 verdict.

## 1. Observed unit and conditioning record

For candidate `k`, randomized circuit `r`, cost locations `ell=1,...,m_k`, and
measured bitstring `b`, let

```text
t_r = (T_{r1}, ..., T_{rm_k}),
s_r = (s(T_{r1}), ..., s(T_{rm_k})).
```

The full `t_r`, not only a parity or averaged label, is observed. Its design
probability `pi(t_r | m)` is fixed by M3 and parameter independent. Conditional
inference uses

```text
P(b | t_r, epsilon, phi, eta, m).
```

The joint experiment factors as

```text
P(t_r, b | epsilon, phi, eta, m)
  = pi(t_r | m) P(b | t_r, epsilon, phi, eta, m).
```

Consequently `pi` adds no score for `(epsilon,phi)`, while discarding `t_r`
changes the statistical experiment.

## 2. Implemented dressed circuit

Start from the exact dressed circuit in `rc_construction_v1.md`. At every tagged
location replace only

```text
RZ(s_{r ell} theta_{k ell})
```

by the primary synthetic operation

```text
RZ((1+epsilon)s_{r ell} theta_{k ell} + phi).
```

All Pauli labels, corrections, mixers, state preparation, and measurements stay
in their recorded order. Denote the resulting unitary by
`U_{k,t_r}(epsilon,phi)`. The quantum probability before nuisance observation
terms is

```text
p_Q(b | k,t_r,epsilon,phi,rho,M)
  = Tr[M_b U_{k,t_r}(epsilon,phi) rho U_{k,t_r}^dagger(epsilon,phi)].
```

This expression is the primary likelihood kernel. It does not assume that the
different locations commute and does not collapse a multi-location circuit to
one scalar phase response.

Using the proven Pauli cancellation at each location, the same probability may
be evaluated in the logical frame by replacing the tagged logical rotations
with

```text
RZ(theta_{k ell} + epsilon theta_{k ell} + s_{r ell} phi).
```

The two forms are algebraically equivalent. The logical-frame form shows that
`epsilon theta` is label invariant and `phi` is label signed; it is not an
independent sign-model assumption.

## 3. Nuisance observation model

The minimum noiseless Gate-1 model sets visibility `v=1`, uses the specified
state and measurement, and sets all offsets to zero. For an explicitly broader
model, define

```text
p(b | t,epsilon,phi,eta)
  = v p_Q(b | t,epsilon,phi,rho,M)
    + (1-v) q_b + h_b(t),
```

where `eta=(rho,M,v,q,h)` and the constraints are

```text
0 <= v <= 1,  sum_b q_b = 1,
sum_b h_b(t) = 0,  and 0 <= p(b | ...) <= 1.
```

`q` is a label-independent baseline incorporating visibility loss and a fixed
offset. `h(t)` is reserved for prespecified label-dependent SPAM/control terms.
It is zero in the primary minimum model. An unrestricted `h(t)` can absorb all
label signal, so any later nonzero nuisance family and its dimension must be
frozen before evaluation; it cannot be added after seeing Gate-1 results.

Environmental memory or drift requires a joint conditional model across
randomized circuits and is out of scope for the first noiseless check. Such
data must not be analyzed with the independent product likelihood below.

## 4. Counts and joint label designs

For `n_{krt}` repeated shots of a fixed dressed circuit, with count vector
`N_{krtb}`, the conditional log likelihood is

```text
log L(epsilon,phi,eta)
  = constant
    + sum_{k,r,t,b} N_{krtb} log p(b | t,epsilon,phi,eta,m_k).
```

Independent labels across locations give
`pi(t)=product_ell pi_ell(T_ell)`. A correlated balanced design uses its frozen
joint `pi(t)` instead. In both cases the outcome likelihood conditions on the
entire vector, so correlations are neither discarded nor treated as extra
independent samples.

## 5. Information boundaries

- **I1:** information in label contrasts is computed from the conditional
  likelihood with the target response treated as unknown. At `phi=0`, the
  logical circuit is identical for all labels for every `epsilon`; therefore
  I1 for `epsilon` is exactly zero in the frozen primary model.
- **I2:** treating `rho`, `M`, or the ideal target response as known can produce
  absolute-level information about `epsilon`. It is diagnostic and cannot pass
  Gate 1A.
- **I3:** admissible profile/efficient information depends on a nuisance family
  frozen at M3. M2 does not claim that a global rescaling closure holds. Whether
  multiple known circuit contexts leave positive deployable profile information
  is an open Gate-1 calculation.

The likelihood alone therefore proves neither parameter identifiability nor
Gate-1 failure. It fixes the statistical object against which those later
claims must be tested.

## 6. Explicit exclusions

The deployable likelihood may not read the ideal target response, true
`epsilon`, true `phi`, error-structure label, future calibration, or holdout
outcomes. Wrapped-angle terms, pulse-level controls, label-dependent offsets,
and memory effects are absent unless separately prespecified. No result from an
averaged RC channel may replace the retained-label likelihood.
