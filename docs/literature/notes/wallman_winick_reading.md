# Wallman--Emerson 2016 and Winick et al. 2022 reading note

**Verification state:** full text read for the randomized-compiling
construction, theorems, assumptions, limitations, simulations/experiments, and
discussion. Proof algebra was inspected but not independently reproduced line
by line.

## Wallman--Emerson

The exact Markovian result organizes a circuit into easy and hard cycles,
samples independent twirls, and compiles each twirl and correction into a
dressed easy gate. Exact stochastic-Pauli tailoring tolerates arbitrary
gate-dependent noise on the hard gates, but assumes gate-independent easy-gate
noise. Easy-gate dependence is handled by a bound comparing the real circuit
with an averaged gate-independent surrogate. The bound is especially favorable
when the twirling group is normalized by the easy-gate group, but it is not an
exact statement that the real channel is Pauli.

The paper repeatedly distinguishes the average over randomized circuits from
an individual randomized circuit. This matters here: retaining labels creates
a conditional experiment, while the original tailoring theorem concerns the
average channel.

## Winick et al.

Winick et al. separate two effects:

1. one randomization can reduce adversarial coherent accumulation between
   cycles, analogously to randomized dynamical decoupling;
2. averaging many randomizations tailors the effective cycle noise toward a
   stochastic Pauli channel and improves nonlinear error metrics.

They extend the cycle-level tailoring statement to time-dependent Markovian
noise and to local stochastic Pauli noise with a persistent environment, while
retaining the gate-independent easy-noise condition. They also give a concrete
gate-dependent non-Markovian failure mechanism: if the environment learns
enough information about twirl parity, coherent accumulation can survive.

## Interpretation for this project

- Neither paper establishes parameter recovery from labels.
- Neither paper says that easy-gate dependence is harmless without magnitude
  conditions; the exact theorem is lost and replaced by a distance bound.
- A label-dependent physical angle is precisely the kind of implementation
  dependence that must be modeled, not waived by citing robustness.
- Improvements in diamond distance or suppression of coherent accumulation do
  not establish improvement in QAOA top-1 decision loss.

The actionable assumptions are summarized in
[`../rc_assumption_table.md`](../rc_assumption_table.md).

