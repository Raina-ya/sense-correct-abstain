# Sense, Correct, or Abstain: A Fixed-Budget Decision Study of Angle-Proportional Coherent Error in QAOA (Technical Report v1)

**Status:** MT7 technical-report draft, 2026-11-21. Every claim maps to a row of
[`../docs/claim_ledger.md`](../docs/claim_ledger.md) (IDs in brackets). All
evidence is analytic or synthetic simulation. No hardware was used. No
confirmatory study was run, and no protocol was independently registered. The
errata in [`../docs/errata/`](../docs/errata/README.md) are part of this
report.

## 1. Abstract

We asked whether runtime evidence, under one fixed shot budget, can support a
choice among issuing a QAOA top-1 decision, recalibrating and re-executing,
or abstaining, when the decision is exposed to an angle-proportional coherent
over-rotation `epsilon` and an additive phase `phi`. The error model is a
synthetic compiled-angle model; no physical carrier was established.

The study followed a prespecified gate sequence with internal Git and SHA-256
locks.

- **Gate 1A (fail).** Retained randomized-compiling labels failed the frozen
  identifiability rule. At `phi = 0`, `epsilon` is not identified under the
  response-free nuisance classes and has zero efficient information [B1, A3].
- **Gate 1B (pass).** A prespecified amplification-and-echo sensor (P-amp)
  identified both parameters in the noiseless model, with a 0.7% resource
  margin and no test of visibility loss [B3].
- **Gate 2 (formal pass, narrow reading).** The decision-relevance gate passed
  formally, but its diagnostic did not show useful selective prediction of
  which units benefit from correction [B4].
- **Gate 3 (fail).** The deployable three-action policy showed no detectable
  net value over always correcting (`Delta_V = 0.0000804`, one-sided 95%
  lower bound −0.000743). A post-lock corrected-estimand reanalysis gives the
  same conclusion. The estimated power was 0.0004 [B5].

The project therefore stopped at M6 under its frozen stopping rule [B7]. The
contribution is a set of boundary results and sensor-independent theory, not
a working method.

## 2. Introduction

Two completed predecessor projects showed that a lower-error estimator can
worsen a top-1 decision, and that probes can see some decision-relevant biases
at a coverage cost. This study asks the next question: whether runtime
evidence supports a useful **action**, with every sensing, correction, and
rerun shot charged to one budget (contract §1, §4).

The question splits into four parts, each tested by its own gate:

1. **Identifiability.** Can a parameter be identified from runtime evidence
   alone, without target ideal values?
2. **Decision relevance.** Does the estimate predict correction benefit?
3. **Net value.** Does the policy beat the best fixed action after all costs?
4. **Non-degeneracy.** Does the policy actually use more than one action?

We make no novelty or priority claim. The systematic prior-art search and the
full-text citation audit required by MT7.4 are incomplete (§7).

## 3. Methodology

**Decision problem** (`docs/contracts/decision_problem_v1.md`).

- A unit is a graph, a candidate pair, an error point, and a replicate.
- Actions: N (issue the initial decision), C (estimate, recalibrate each
  tagged angle to `(a - phi_hat)/(1 + epsilon_hat)`, and re-execute both
  candidates from a fixed shot reserve, deciding from the corrected data
  only), A (abstain).
- Loss: 1 for a wrong issued answer, `lambda_A = 1/4` for abstaining (an
  owner-chosen normative ratio), and `lambda_F = 1/4` for a failed correction,
  after which no answer is issued.
- Primary endpoint: `Delta_V = mean(L_fixed - L_policy)` against the best
  development-locked fixed comparator.

**Error and compilation semantics** (M2). The tagged cost rotation `RZ(a)`
becomes `RZ((1+epsilon)a + phi)`, with signed compiled angles `a = s(t) theta`
and error-free virtual-Z frames. The frame-covariance identity [A1] makes the
logical error `epsilon theta + s(t) phi`.

**Theory** (`docs/theory/three_action_theory_v1.md`):

- the three-action risk identity [A4];
- the blindness lemma and finite-pilot bound [A5];
- the collapse result under the issue-only comparator [A6];
- Lemma S1′ [A3] and the gap-shift bound [A7] (E006).

**Gates**, each frozen before its run (internal locks, D6):

- Gate 1A: RC labels, with information sources I1/I2/I3 separated.
- Gate 1B: P-amp fallback.
- Gate 2: transfer rule versus a constant majority baseline; balanced
  accuracy; leave-one-graph-out robustness margin 0.05.
- Gate 3: graph-cluster bootstrap lower bound of `Delta_V`.
- Gate 4: at least two actions, each on ≥ 5% of units and in ≥ 10 clusters.

## 4. Experiment setup

- **Gate 1:** exact enumeration of 2- and 3-qubit contexts; 16 Pauli labels
  per tagged block; 9 × 9 grid with `epsilon, phi in [-0.04, 0.04]`;
  `n_S = 2430` sensing shots.
- **Gate 2:** 6600 units (10 graphs with 2–5 qubits, 4 mixer angles, 11
  candidate pairs, 15 error points). Of these, 4905 were evaluable and 3726
  were in the evaluation partition.
- **Gates 3/4:** 99 generated graph clusters with 4–6 qubits (33 policy-lock,
  66 evaluation), giving 5940 units, of which 3545 were evaluable in the
  evaluation partition.
- **Noise:** shot noise with coherent E2 only. There was no decoherence, no
  visibility loss, and no device parameterization.
- **Scoring:** 256-replicate Monte Carlo estimates of selection
  probabilities.

## 5. Results

**Gate 1A: FAIL** [B1, B2].

- The frozen run's I3, recovery, and control entries were hard-coded (E001).
  The verdict nonetheless holds on a correct basis. At the nine `phi = 0`
  grid points, `epsilon` is locally non-identified under any class containing
  a free label-independent distribution (explicit construction), so the
  frozen profile MLE is nonunique and the frozen rule fails (E006 §2).
- The frozen nuisance class is ambiguous. Under its literal first-order
  reading, G3 retains second-order information of at most 3.5e-6/shot, which
  is useless at the budget (E001 §3).
- At the sensing budget, even an oracle has two-point error ≥ 0.185 between
  the frozen hard pairs.

**Gate 1B: PASS** [B3]. P-amp identifiability holds in the noiseless model,
and its circuits match the estimator's phase model. The resource condition
has a 0.7% margin and would fail for visibility below 0.9926. Visibility
attenuation was not tested.

**Gate 2: formal PASS** [B4].

> Gate 2 formally passed its prespecified, internally locked rule, but the
> diagnostic did not demonstrate useful selective prediction of which units
> benefit from correction. Its precision was 0.093 versus a base rate of
> 0.077, and much of the apparent gain came from excluding large-gap units.
> Therefore Gate 2 is retained as a formal PASS but not interpreted as
> evidence of operationally useful benefit selection.

Further points, all from E003:

- The rule predicted benefit for 78.7% of units.
- The binary labels are noisy: 126 of 287 positives lie within two Monte Carlo
  s.d. of zero.
- The gate deviated from the program plan: no uncertainty bound and no power
  analysis.
- The same-budget P2 comparator was structurally blind on half of the units.

**Gate 3: FAIL; Gate 4: PASS** [B5, B6].

- The selected fixed comparator was always-correct (policy-lock mean loss
  0.0079, against 0.029 for issue-only).
- Frozen result: `Delta_V = 0.0000804`, lower bound −0.000743.
- The frozen N-path loss ignored selection on the same shots (E004). A
  post-lock reanalysis with the conditional loss gives `Delta_V = 0.000237`
  and lower bound −0.000625. This reanalysis cannot change or rescue the
  verdict.
- Estimated power was 0.0004.
- The policy coincided with always-correct on 72.6% of units.

**Reproducibility** [C1–C3]. Verdict-level quantities reproduce under internal
recomputation. Stored floats differ across platforms in 416 of 6600 (Gate 2)
and 31 of 5940 (Gate 3/4) units. Analysis code was not locked before any run.

## 6. Conclusion

Under the synthetic model and the frozen budget:

1. Retained RC labels did not identify the angle-proportional error at
   `phi = 0` under response-free nuisance classes.
2. A known-reference amplification sensor did, in a noiseless setting with a
   thin margin.
3. The resulting deployable three-action policy showed no detectable value
   over always correcting.

The study stopped as prespecified. **We do not claim that the method works.**

## 7. Discussion

**Why the policy had no room.** In this model, always correcting was already
near-optimal (possible explanation E-2). An adaptive policy can add value only
where correction sometimes hurts and the evidence can tell when; the Gate 2
diagnostics show that the frozen evidence could not.

**Generalization boundaries.** All results are specific to:

- the synthetic compiled-angle model;
- 2–6 qubits and `p = 1`;
- the frozen grids and budget; and
- shot-noise-only simulation.

Visibility loss, decoherence, drift, context mismatch, structured nuisance
models, larger circuits, and hardware are untested.

**Methodological lessons** (E005).

- Lock the analysis code and environment, not only the design.
- Assess power before any evaluation outcome exists.
- Make sampling platform independent.
- Score the policy loss conditional on the evidence the policy saw.
- Specify nuisance classes unambiguously.

**Open items.**

- Owner review of the draft proofs (A3–A7).
- Full-text verification of the Chow and Tsybakov attributions.
- The MT7.4 citation and novelty audit: a systematic search; full-text
  comparison with Vyas (2026), the robust phase-estimation papers, pseudo
  twirling, KIK, and CDR/P2.

## 8. References

Verification states are those recorded in `docs/literature/library.csv`. They
are not upgraded here.

- Wallman, J. J., & Emerson, J. (2016). Noise tailoring for scalable quantum
  computation via randomized compiling. *Phys. Rev. A* 94, 052325. —
  *verified (inherited); full text reread by an AI agent; owner confirmation
  pending.*
- Vyas, K. (2026). Recovering coherent errors from randomized-compiling labels.
  arXiv:2607.26756. — *abstract checked; full-text reading by an AI agent
  unconfirmed by owner.*
- Kimmel, S., Low, G. H., & Yoder, T. J. (2015). *Phys. Rev. A* 92, 062315;
  Rudinger, K., et al. (2017). *Phys. Rev. Lett.* 118, 190502. —
  *metadata and abstract only.* Cited only for the statement that P-amp is
  close to robust phase estimation and carries no novelty.
- McKay, D. C., et al. (2017). Efficient Z gates for quantum computing.
  *Phys. Rev. A* 96, 022330. — *metadata and abstract only.* Cited for
  virtual-Z context.
- Chow, C. K. (1970). On optimum recognition error and reject tradeoff.
  *IEEE Trans. Inf. Theory* 16, 41–46. — *abstract only; attribution of the
  exact rule form unverified.*
- Le Cam, L. (1973). *Ann. Statist.* 1, 38–53. — *verified (inherited,
  bibliographic).*
- Tsybakov, A. B. (2009). *Introduction to Nonparametric Estimation.*
  Springer. — *metadata only; lemma locations unverified; proofs in this
  project are self-contained.*
- Predecessor projects: `Raina-ya/adaptive-qem-benchmark` and
  `Raina-ya/bias-probe-visibility` (commit `cd5e576`).
