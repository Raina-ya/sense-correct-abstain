# Sense, Correct, or Abstain: A Fixed-Budget Decision Study of Angle-Proportional Coherent Error in QAOA

**Author:** Zhen-Jun Liu

**Status:** Final MT7 technical report, 2026-11-23

**Version DOI:** 10.5281/zenodo.24443391
**Evidence boundary:** analytic results and synthetic simulation only; no hardware experiment and no independent validation.

Every scientific claim maps to `docs/claim_ledger.md`. The append-only errata in
`docs/errata/` are part of this report and take precedence over superseded
statements in frozen artifacts.

## Abstract

We studied whether runtime evidence, under one fixed shot budget, can support a
choice among issuing a QAOA top-1 decision, recalibrating and re-executing, or
abstaining when the decision is exposed to angle-proportional coherent
over-rotation `epsilon` and additive phase `phi`. The error model is a synthetic
compiled-angle model; no physical carrier was established. The study followed a
prespecified gate sequence with internal Git and SHA-256 locks. Gate 1A failed:
retained randomized-compiling labels did not satisfy the frozen recovery rule.
Gate 1B passed only in a noiseless known-reference model, with a 0.7% visibility
margin and no visibility-attenuation test. Gate 2 formally passed its internally
locked rule, but precision was 0.093 against a 0.077 base rate and the diagnostic
did not establish useful benefit selection. Gate 3 failed: the deployable policy
had `Delta_V = 0.0000804` with a one-sided 95% lower bound of `-0.000743`.
A corrected post-lock estimand also failed. Estimated power was 0.0004. The
project therefore stopped after M6. These are boundary and negative results, not
evidence that the method works.

## Introduction

The project asks whether runtime evidence supports a useful action after every
sensing, correction, and rerun shot is charged to one budget. The decision has
three actions: issue the initial answer (N), recalibrate and re-execute (C), or
abstain (A). Four gates test identifiability, decision relevance, net value, and
non-degenerate action use. The contribution is a documented combination of a
fixed-budget decision contract, sensor analysis, and negative policy result. We
make no novelty or priority claim.

## Methodology

### Decision problem

A unit consists of a graph, candidate pair, error point, and replicate. A wrong
issued answer has loss 1; abstention and failed correction each have the
owner-chosen normative loss 1/4. After failed correction no answer is issued.
For action C, each tagged angle `a` is recalibrated to
`(a - phi_hat)/(1 + epsilon_hat)` and both candidates are re-executed from a
fixed reserve. Corrected decisions use corrected data only. The primary endpoint
is `Delta_V = mean(L_fixed - L_policy)`, where `L_fixed` is the best
development-locked fixed comparator.

### Error semantics and theory

The tagged cost rotation `RZ(a)` becomes `RZ((1+epsilon)a + phi)`. Signed
compiled angles give logical error `epsilon*theta + s(t)*phi`. The analytic
theory includes the three-action risk identity, pairwise switching rules, a
blindness lemma, finite-pilot lower bounds, and collapse under the issue-only
comparator. Lemma S1-prime proves local non-identification under its stated
nuisance class; it does not infer global non-identifiability from zero efficient
Fisher information. Lemma B gives a local, instance-dependent gap-shift bound;
it is not a global uniform guarantee. Owner-reviewed proofs and corrections are
recorded in E007-E009 and `docs/theory/`.

### Gate sequence

Gate 1A tested retained randomized-compiling labels with information sources
kept separate. Gate 1B was the prespecified amplification-and-echo fallback.
Gate 2 compared a frozen transfer rule with a constant-majority baseline using
balanced accuracy and leave-one-graph-out robustness. Gate 3 used a graph-cluster
bootstrap lower bound for `Delta_V`. Gate 4 required two actions to occur on at
least 5% of units and in at least 10 graph clusters. Each gate design was locked
before its run, but the analysis code and original software environment were not
fully locked.

## Experiment Setup

Gate 1 used exact enumeration of 2- and 3-qubit contexts, 16 Pauli labels per
tagged block, a 9 by 9 grid over `epsilon, phi in [-0.04, 0.04]`, and
`n_S = 2430` sensing shots. Gate 2 generated 6600 units from 10 graphs with 2-4
qubits, four mixer angles, 11 candidate pairs, and 15 error points; 3726
evaluable units were in the evaluation partition. Gates 3 and 4 generated 5940
units from 99 graph clusters with 4-6 qubits; 3545 evaluable units from 66
clusters were in the evaluation partition. The simulation included coherent E2
and shot noise, but no decoherence, visibility loss, drift, context mismatch, or
device parameterization. Selection probabilities used 256 Monte Carlo
replicates.

## Results

### Gate 1A: FAIL

The frozen run contained hard-coded information, recovery, and control entries;
E001 invalidated that original basis. The verdict remains FAIL on the corrected
analytic basis. At `phi = 0`, the response-free nuisance class admits distinct
local parameterizations with the same first-order observable response, making
the frozen profile recovery non-unique. This is a local non-identification
result under the stated nuisance class, not an unrestricted global claim. The
frozen nuisance-class wording is ambiguous; under its literal first-order
reading, the retained second-order signal is at most `3.5e-6` per shot and is
not useful at `n_S = 2430`. Product-distribution distances, rather than
single-shot distances multiplied by sample size, give an oracle two-point error
of at least approximately 0.185 for the frozen hard pair.

### Gate 1B: PASS in the synthetic known-reference model

The P-amp sensor identified both parameters in the noiseless analytic model and
its circuit semantics matched the estimator. The resource condition had only a
0.7% margin and fails below visibility 0.9926. Visibility attenuation was not
tested, so the result does not establish robustness or hardware transfer.

### Gate 2: formal PASS, practical conclusion narrowed

Gate 2 formally passed its prespecified, internally locked rule, but the
diagnostic did not demonstrate useful selective prediction of which units
benefit from correction. Its precision was 0.093 versus a base rate of 0.077,
and much of the apparent gain came from excluding large-gap units. Therefore
Gate 2 is retained as a formal PASS but not interpreted as evidence of
operationally useful benefit selection.

The rule predicted benefit for 78.7% of evaluation units. Of 287 positive
labels, 126 were within two Monte Carlo standard deviations of zero. The
same-budget P2 comparator was structurally blind on 3300 of 6600 generated
units. The gate also lacked the uncertainty bound and power analysis requested
by the program plan.

### Gate 3: FAIL; Gate 4: PASS but moot

The selected fixed comparator was always-correct, with policy-lock mean loss
0.00791 versus about 0.029 for issue-only comparators. The frozen result was
`Delta_V = 0.0000804` with lower bound `-0.000743`. The frozen N-path loss had
ignored selection on the same shots. An append-only, post-lock reanalysis using
the corrected conditional loss gave `Delta_V = 0.000237` and lower bound
`-0.000625`; it cannot change or rescue the verdict. Estimated power was
0.0004. The policy chose C on 72.6% of evaluation units. Gate 4 passed its
action-frequency rule, but it is moot after Gate 3 failed.

### Reproducibility status

Verdict-level quantities reproduce under internal deterministic recomputation.
Stored floats differ across platforms in 416 of 6600 Gate 2 units and 31 of
5940 Gate 3/4 units. This is internal recomputation, not independent validation.
The original Python version and some package versions remain unknown, and the
analysis code was outside the original locks. Future studies use the v2 lock
template to lock code, environment, seed, command, and artifact hashes together.

## Conclusion

Under the synthetic model and frozen budget, retained RC labels failed the
frozen recovery rule, a noiseless known-reference sensor passed with a thin
resource margin, and the resulting three-action policy showed no detectable
value over always correcting. The frozen stopping rule ended the primary route
after M6 and moved the project to MT7 synthesis. We do not claim that the method
works.

## Discussion

Always correcting was already near-optimal in this model, leaving little room
for an adaptive policy. A policy can add value only where correction sometimes
hurts and runtime evidence can identify those cases; the Gate 2 diagnostics do
not establish that capability.

The conclusions are limited to the synthetic compiled-angle model, 2-6 qubits,
QAOA depth `p = 1`, the frozen grids and budget, and shot-noise-only simulation.
No claim extends to visibility loss, decoherence, drift, context mismatch,
structured nuisance models, larger circuits, or hardware. Low power and
cross-platform floating-point differences remain part of the result.

The scoped literature audit places P-amp near robust phase estimation and P2
near known-reference data-driven error mitigation. Chow's exact reject rule and
Tsybakov's cited lower-bound lemmas were checked against full-text scans on
2026-11-23; the project proofs remain self-contained. The study does not claim a
new sensor, a new rejection rule, or priority.

## References

The LaTeX source uses an `abbrv`-style numeric bibliography. Verification and
access levels for every entry are recorded in `docs/literature/library.csv` and
`docs/literature/library_notes.md`.

1. C. K. Chow, "On Optimum Recognition Error and Reject Tradeoff," IEEE Transactions on Information Theory 16, 41-46 (1970).
2. A. B. Tsybakov, *Introduction to Nonparametric Estimation*, Springer (2009).
3. J. J. Wallman and J. Emerson, "Noise Tailoring for Scalable Quantum Computation via Randomized Compiling," Physical Review A 94, 052325 (2016).
4. K. Vyas, "Recovering Coherent Errors from Randomized-Compiling Labels," arXiv:2607.26756 (2026).
5. S. Kimmel, G. H. Low, and T. J. Yoder, "Robust Calibration of a Universal Single-Qubit Gate Set via Robust Phase Estimation," Physical Review A 92, 062315 (2015).
6. K. Rudinger et al., "Experimental Demonstration of a Cheap and Accurate Phase Estimation," Physical Review Letters 118, 190502 (2017).
7. D. C. McKay et al., "Efficient Z Gates for Quantum Computing," Physical Review A 96, 022330 (2017).
8. P. Czarnik et al., "Error Mitigation with Clifford Quantum-Circuit Data," Quantum 5, 592 (2021).
9. A. Lowe et al., "Unified Approach to Data-Driven Quantum Error Mitigation," Physical Review Research 3, 033098 (2021).
10. V. Scavino, "Decision Kernels for Quantum Error Mitigation: Why Accuracy Gains Need Not Improve Downstream Decisions," arXiv:2607.02888 (2026).
