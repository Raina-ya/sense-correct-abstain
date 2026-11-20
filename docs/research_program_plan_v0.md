# Sense, Correct, or Abstain: Research Program Plan v0

**Status:** planning draft, 2026-11-19; revised 2026-11-20 (Gate 1A/1B routing, frame bookkeeping, separated information quantities). This document contains no new experimental result. It is not a frozen protocol and has not been independently timestamped. The words *preregistered* and *preregistration* are reserved for a future record with an independent timestamp such as OSF.

**Planning assumption:** 8--10 hours per week, starting 2026-11-23. Dates move later if this assumption is not confirmed; Part contents do not change in response to delays or results.

**Evidence boundary:** the two completed projects supply the reported analytic and noisy-simulation results stated below. The third project has not run an experiment. Hardware work is never implied by this plan and requires separate written authorization for every run.

## 1. One-page research map

### Umbrella question

**Primary wording**

> Under a fixed quantum-execution budget, when is runtime evidence sufficient to decide whether to trust, correct, or withhold a quantum decision?

**Alternative A -- identifiability emphasis**

> Which decision-relevant biases are identifiable from runtime quantum data under a fixed resource budget, and which remain fundamentally indistinguishable?

**Alternative B -- policy emphasis**

> How should a noisy quantum workflow allocate finite execution resources among deciding, sensing, correcting, and abstaining?

The primary wording is preferred because it covers all five chapters without assuming that a probe, correction, or hardware implementation succeeds.

### Inherited fixed findings

These are inputs from the completed projects, not results of this repository.

- **Chapter 1, noisy simulation:** under the stated QAOA selection experiment, raw selection error was `0.271`, linear-ZNE selection error was `0.379`, and the reported comparison was `p = 0.001`. Lower RMSE did not imply a better decision. Under the stated normal approximation, Proposition 1 gives mitigation improvement exactly when `Delta_m > sqrt(gamma) * Delta_r`; for the studied linear ZNE, `gamma = 4.375` and the ratio threshold is approximately `0.48`.
- **Chapter 2, noisy simulation:** assigning 10% of the budget to the structure-matched probe and abstaining on alarm gave registered improvement `Delta_FC = +0.0080` with coverage loss `0.418`. The improvement came from the frozen E2 and E3 coherent-error structures. The structure-agnostic P2 exchange had coverage loss `0.142`. The Proposition-1 prediction test scored `45/100` and never selected ZNE, so it was a degenerate predictor.
- **Chapter 2, analytic:** uniform readout noise does not flip the decision in the frozen symmetric QAOA construction (Eq. 8). Eq. (6), the blindness lemma, and the Le Cam two-point bound are the theoretical starting tools inherited by Chapter 3.
- **Chapter 2, hardware-derived addendum:** on the stated `ibm_marrakesh` readout study, the largest measured pair correlation was approximately `0.011`. This is a narrow hardware-derived finding, not evidence that the simulation results generalize to hardware.

### Chapter map

| Chapter | Working title | Core question | Status | Dependency on the previous chapter | Main evidence type | Prespecified fallback if the main topic fails |
|---|---|---|---|---|---|---|
| Ch. 1 | Estimation Is Not Decision | When does lower estimator error fail to improve top-1 selection under a fixed shot budget? | Completed: `adaptive-qem-benchmark` | Starting point | Analytic and noisy simulation; no hardware evidence | If a general selector fails, retain the counterexamples and Proposition 1 as the chapter's result. This is the observed outcome, not a future pivot. |
| Ch. 2 | Visibility of Decision-Relevant Bias | Which runtime probes can see a differential bias that flips a decision, and what coverage is lost by acting on an alarm? | Completed: `bias-probe-visibility` | Uses Ch. 1's distinction between estimator quality and decision correctness | Analytic and noisy simulation; separately authorized hardware-derived readout addendum | If broad detection fails, draw the visible/blind boundary and quantify the cost of abstention. This is the observed chapter shape. |
| Ch. 3 | Sense, Correct, or Abstain | Can randomized-compiling labels identify angle-dependent coherent bias well enough to choose no action, recalibration, or abstention, and when can no probe choose reliably? | Planning | Starts where Ch. 2 stops: an alarm has value only if it supports a useful action | Analytic, noiseless simulation, noisy simulation; optional device-parameter simulation; hardware only in a separately registered and authorized addendum | If RC labels cannot identify the multiplicative error under the Gate 1A criterion, the RC-label construction becomes a negative identifiability result and the chapter continues only through the single fallback sensor fixed in advance (Gate 1B, P-amp). If P-amp also fails, retain the general three-action theory, the blindness and lower-bound results, and the RC-label negative result; no third probe is added. If identification works but correction has no net value, report the action-value boundary rather than changing methods. |
| Ch. 4 | Decisions Under Drift | When should a workflow sense again, recalibrate, switch action, or stop when calibration becomes stale? | Planned; data collection not authorized | Sequentializes Ch. 3's one-shot action, loss, and sensing cost | Analytic, simulated drift, and only if separately authorized, longitudinal hardware evidence | If a stable hardware time series cannot be collected, establish a time-uniform method under explicitly simulated drift and report hardware generalization as unresolved. |
| Ch. 5 | Limits and Transfer | Which lower bounds and action rules transfer beyond symmetric QAOA-MaxCut, and where do task asymmetry or scale change the boundary? | Planned | Tests whether the concepts from Chs. 1--4 survive a change of task, scale, and error structure | Analytic, noiseless simulation, noisy simulation, and possibly device-parameter simulation; hardware not assumed | If transfer fails, produce a failure taxonomy separating QAOA-specific symmetries from decision-theoretic structure. Candidate backup task: an asymmetric ranking problem where readout error can change the decision. |

### Chapter-to-chapter transitions

- **Ch. 1 -> Ch. 2:** Knowing that mitigation can worsen a decision raises the runtime question: can the dangerous bias be seen before trusting the result?
- **Ch. 2 -> Ch. 3:** Detecting risk is not enough when alarm-and-abstain discards substantial coverage; the next question is which action the evidence supports.
- **Ch. 3 -> Ch. 4:** A one-shot action rule becomes stale when noise changes, so the decision must include when to measure and act again.
- **Ch. 4 -> Ch. 5:** A sequential rule is useful only to the extent that its guarantees survive new tasks, error structures, and scales.

### Why the five-chapter order is retained

The proposed order is causal rather than chronological: establish a failure of estimator-based reasoning, study observability, study action, add time, then test transfer. Moving the lower-bound chapter earlier would mix general theory with an unvalidated action model; moving drift earlier would require a loss and action space that Ch. 3 has not yet defined.

## 2. Program progress table

Work estimates are focused research time, not calendar duration. They exclude waiting for external review, OSF registration, hardware queues, and large uploads.

| Chapter | Existing output | Main gap | Next deliverable | Estimated focused work | Blocking factors |
|---|---|---|---|---:|---|
| Ch. 1 | Completed repository and paper; Proposition 1; fixed-budget simulation results | Final publication and external review are outside this plan | Stable citation package and a one-page interface note defining what Ch. 2 inherits | 4--8 h | Publication decisions and third-party review |
| Ch. 2 | Completed theory, frozen protocol, one-time holdout, paper, and hardware readout addendum | DOI/release closure and broader external review | Stable citation package plus an explicit Ch. 2 -> Ch. 3 handoff of definitions and evidence limits | 6--10 h | Release/DOI actions under user control |
| Ch. 3 | Research question, four gates, initial literature list, and exact prior E2 implementation identified | No formal likelihood model, no label construction, no primary loss weight, no development or holdout protocol | Part 1 mathematical specification and adversarial review | 35--50 h for Part 1; about 180--240 h for the full chapter project | RC-label construction, identifiability, abstention cost, power, literature novelty, and implementation feasibility |
| Ch. 4 | Umbrella question and sequential extension identified | No registered longitudinal protocol or time series | Hardware-monitoring protocol draft and authorization template; no jobs | 12--20 h to design; then monthly sessions if authorized | Stable backend access, platform rules, drift timescale, repeated authorizations |
| Ch. 5 | Candidate directions: lower-bound transfer, asymmetric tasks, larger scale | Task and estimand not selected | A two-page comparison of at most three transfer tasks after Ch. 3 theory stabilizes | 12--18 h for selection; experiment effort unknown | Ch. 3 definitions, classical ground truth, scale, and compute budget |

## 3. Chapter 3 detailed plan

### 3.1 Scope and fixed four-Part structure

The following Part names, purposes, and order are decided before work begins. A failed gate can stop or delay later Parts, but results do not authorize replacing a Part with a more favorable topic.

| Part | Purpose | Gates | Evidence allowed in this Part | Deliverable |
|---|---|---|---|---|
| Part 1 -- Identifiability and label semantics | Define the physical/statistical model, derive the rank and information conditions, specify the RC-label construction and the fixed P-amp fallback, and test only the smallest analytic/noiseless cases | Gates 1A and 1B | Analytic and noiseless simulation only; no confirmatory noisy data | Mathematical specification, literature map, frozen model candidates, and Gate-1 report |
| Part 2 -- Decision relevance and correction | Determine whether an identifiable parameter predicts gap bias or a top-1 flip; define correction and its failure modes | Gate 2 | Development noisy simulation on development-only seeds and instances | Development report, correction rule, failure taxonomy, and Gate-2 report |
| Part 3 -- Policy value, audit, and freeze | Account for sensing, correction, re-execution, and abstention; test policy non-degeneracy; conduct power analysis and adversarial pre-data audit; freeze and independently timestamp the confirmatory protocol | Gates 3 and 4 | Development and split-99 design simulation only; no holdout | Locked primary rule, thresholds, loss, power report, audit, manifest, and independent registration record |
| Part 4 -- One-time confirmation and synthesis | Run the frozen holdout once, report all positive, negative, and nonevaluable results, then synthesize the paper and conduct a hardware go/no-go review | No new design gate; tests the frozen primary claim | Confirmatory noisy simulation; optional device-parameter simulation clearly separated; hardware only after a new protocol and explicit authorization | One-time holdout report, claim ledger, paper, reproducibility package, and hardware go/no-go decision |

### 3.2 Gate table

Numerical thresholds below are **planning placeholders** unless a source is stated. Part 1 or Part 3 must justify, sensitivity-test, freeze, and independently timestamp every retained threshold before relevant data exist.

| Gate | Question | Pass criterion | Failure criterion | Prespecified exit after failure |
|---|---|---|---|---|
| Gate 1A: identifiability, primary mechanism (RC labels only) | Can RC-label-conditioned observations identify multiplicative `epsilon` separately from additive `phi` for a frozen angle set, without any ideal target readout? | Using only the information quantities admitted in Section 3.3 (I1, the label-contrast likelihood, and the non-oracle part of I3, the profile/efficient information for `epsilon` with the unknown ideal response as a nuisance parameter): the admitted information matrix for `(epsilon, phi)` is full rank under at least one frozen deployable design, and a noiseless numerical check agrees with the analytic rank and recovers injected parameters within numerical tolerance. I2 (absolute-level information under a known ideal response curve) is reported as a diagnostic only and cannot contribute to a pass. | The admitted information for `epsilon` is zero or rank deficient in every frozen deployable design; or apparent rank comes only from I2, ideal values, or oracle knowledge unavailable at runtime. | Record the RC-label construction as a negative identifiability result. Proceed to Gate 1B if and only if Gate 1A failed by its frozen criterion. Do not modify the RC-label design after inspection. |
| Gate 1B: identifiability, prespecified fallback (P-amp) | Can the fixed amplification-repetition plus echo reference (P-amp, Section 3.4.1) identify `(epsilon, phi)` within the sensing share of the budget? | All P-amp pass conditions in Section 3.4.1, fixed before Gate 1A is run, are met. | Any P-amp pass condition fails. | Stop the empirical policy branch. Retain the action-selection blindness result, the finite-pilot lower bound, the three-action theory, and the RC-label negative result. No third probe is introduced. |
| Gate 2: decision relevance | Does `epsilon_hat` predict gap bias or a flip rather than merely a gate parameter? | On development-only instances, a rule fixed before evaluation predicts the **sign of correction benefit** better than its frozen no-information baseline, with a prespecified uncertainty bound and no ideal target value as an input. Exact metric and margin are frozen in Part 1 after power analysis. | No out-of-sample improvement over the frozen baseline; signal exists only for parameter estimation, not decision loss; or the rule requires knowing the error structure or ideal gap. | End the corrective-policy claim. Retain parameter identifiability plus the theorem showing why it is not decision sufficient. No confirmatory holdout for an adaptive action policy. |
| Gate 3: net value | After charging every shot to one budget, does sensing and correction improve decision value over fixed policies? | Under the development-locked scalar loss and total budget, the lower confidence bound for the label policy's improvement over the development-selected best fixed baseline is positive. Sensitivity to the abstention-cost weight is reported but does not replace the primary value. | Improvement is nonpositive, depends on uncharged re-execution/calibration, or disappears under the primary cost definition. | Report the resource boundary and stop before confirmatory execution. A useful correction with negative net value is a negative result, not a reason to enlarge the budget. |
| Gate 4: non-degeneracy | Does the policy actually use more than one action? | Across development strata fixed in advance, at least two actions have nonzero selection probability and each clears a prespecified minimum frequency supported by power analysis; no action is selected solely because of a coding tie-break. | Always-correct, always-abstain, or effectively no-action under the frozen distribution; one action occurs too rarely to estimate its loss. | Replace no rule after inspection. Report that the optimal deployable policy collapsed to a fixed action; compare that fixed action only as a development result and stop the adaptive confirmatory claim. |

#### Gate 1 routing and claim boundary (decision recorded 2026-11-20)

- The only allowed path is: Gate 1A (RC labels) -> if and only if Gate 1A fails by its frozen criterion -> Gate 1B (P-amp) -> if Gate 1B fails, stop the empirical policy branch.
- The P-amp circuits, repetition counts, statistic, budget share, and pass thresholds in Section 3.4.1 are fixed before Gate 1A is run. They are not designed or tuned after Gate 1A results exist.
- If the chapter proceeds through Gate 1B, the paper may not claim that RC labels sense `epsilon`. The claim becomes: whether a known-phase sensing structure can support a net-beneficial correct-or-abstain decision under a fixed budget. Novelty is placed in decision relevance, fixed-budget accounting, and the three-action policy, not in the P-amp sensor, which is close to known phase-estimation constructions.
- In Gates 2--4 and the endpoints, "the sensor" means the sensor that passed Gate 1 (RC labels if Gate 1A passed, otherwise P-amp). If both could be evaluated, RC labels remain primary.
- An analytic draft (`docs/theory/gate1_frame_covariance_draft.md`, unreviewed) predicts that Gate 1A fails under the compiled-angle model with virtual Z frames. This is a prediction to be reviewed, not a result, and it does not change the routing above.

### 3.3 Part 1 one-page mathematical problem

#### Parameters and angle sets

Let `k` index candidates, `ell` index cost layers or cost rotations, and `t` index randomized-compiling labels. Let

- `theta_{k ell}` be the frozen logical cost angle;
- `g_t(theta_{k ell})` be the compiled signed or shifted angle produced by the frozen label-absorption rule;
- `epsilon` be a multiplicative angle error;
- `phi` be a label-independent additive phase in the primary identifiability model;
- `delta_{k ell t}` be the realized phase error relevant to the measurement likelihood.

The primary linear phase model to test is

```text
delta_{k ell t} = epsilon * g_t(theta_{k ell}) + phi.
```

This is a model, not yet a hardware fact. Part 1 must separately state:

1. **Logical-angle model:** error is applied before label absorption.
2. **Compiled-angle model:** error scales the actual compiled angle `g_t(theta)`.
3. **Control model:** the hardware control parameter, not an abstract `RZ`, carries the error.

The project cannot infer one model from the identity `X RZ(theta) X = RZ(-theta)`. It must establish how the compiler represents the label and whether the operation is a pulse, a virtual frame update, or a composite two-qubit construction. A `theta + pi` representation is not equivalent as an error model unless that representation is frozen explicitly.

#### Frame bookkeeping: physical-frame versus logical-frame phase

`delta_{k ell t}` above is defined in the physical (compiled) frame. The measurement likelihood depends on the phase after the label is undone, that is, in the logical frame. For a label Pauli `P_t` and a rotation generator `G`, write `s_t = -1` if `P_t G P_t = -G` and `s_t = +1` if they commute. Under the compiled-angle model with sign-flip absorption (`g_t(theta) = s_t * theta`) and virtual, error-free Z frames, the unreviewed draft derivation gives

```text
P_t RZ((1+epsilon) * (-theta) + phi) P_t = RZ((1+epsilon) * theta - phi),
logical phase error  delta^L_{k ell t} = epsilon * theta_{k ell} + s_t * phi.
```

So in the logical frame the multiplicative term does not depend on the label, while the additive term flips sign with the label. This is the reverse of how the two terms look in the physical frame. If Z labels are instead absorbed as `theta + pi` with wrapping and the error scales the wrapped angle, an extra label-dependent term `epsilon * c_t` with `c_t` in `{+pi, -pi}` appears. Which representation applies must be frozen in Part 1 (see the draft for a numerical check of one single-qubit example; that check is not a proof).

#### Three information quantities (reported separately)

Let `r` denote the unknown ideal response of the target circuits (the response curve as a function of the logical angle). Part 1 computes, for every frozen design:

1. **I1, label-contrast information.** The Fisher information for `(epsilon, phi)` carried by the likelihood of label-contrast statistics, whose distribution does not depend on `r` at `epsilon = phi = 0`.
2. **I2, absolute-level information with a known response.** The Fisher information of the full label-resolved likelihood when `r` is treated as known. This uses ideal values and is a diagnostic only.
3. **I3, profile or efficient information with `r` as nuisance.** The efficient information for `epsilon` after projecting out the nuisance tangent space of `r` (or the profile information under a stated parametric nuisance model). Only the part of I3 that does not rely on oracle knowledge of `r` is admissible.

Gate 1A may pass only on I1 and the admissible part of I3. I2 may never be used as deployable evidence.

**Analytic prediction written before simulation (draft, unreviewed).** Under the compiled-angle model with virtual Z frames, if `phi = 0`, every label-contrast statistic has zero mean for every `epsilon`, and the admissible information for `epsilon` from RC labels is zero (with a nonparametric nuisance `r`). Under the same model with `phi != 0`, labels carry first-order information about `phi` and information about `epsilon` only at order `phi`. Under the logical-angle model, labels carry no information about either parameter.

#### Direct-phase identifiability

If phases `delta_i` were directly observed at design angles `a_i = g_{t_i}(theta_{k_i ell_i})`, the design matrix would be

```text
X = [[a_1, 1], ..., [a_m, 1]].
```

The pair `(epsilon, phi)` is identifiable in this direct linear model if and only if `rank(X) = 2`, equivalently the observed design contains at least two distinct effective angles with positive weight. With one effective angle, every pair satisfying `epsilon * a + phi = constant` is observationally equivalent. This is the first concrete action-selection blindness example.

#### Measurement likelihood and Fisher information

The experiment observes bitstrings, not phases. Let `p_y(delta_i, c_i)` be the probability of outcome `y` for circuit context `c_i`. With `x_i = (a_i, 1)^T`, the Fisher information has the form

```text
I(epsilon, phi) = sum_i n_i * J_i(delta_i) * x_i x_i^T,
J_i(delta_i) = sum_y [ (d log p_y / d delta_i)^2 * p_y ].
```

Full rank requires both variation in effective angle and nonzero measurement sensitivity `J_i`. Therefore two distinct candidate angles are necessary in the direct linear model but are not sufficient in the quantum experiment: symmetry, periodicity, an insensitive measurement basis, or proportional score vectors can preserve blindness. When full rank holds, the local Cramer--Rao direction is

```text
Var(epsilon_hat) >= [I(epsilon, phi)^(-1)]_{epsilon,epsilon}
```

for locally unbiased estimators. Part 1 must not claim a global guarantee from this local bound. A finite-separation two-point bound using total variation, Hellinger distance, or KL divergence will be derived for the budget-limited case.

#### Predictions written before simulation

- One candidate with one effective angle is blind to `(epsilon, phi)` in the direct model.
- Two candidates with identical effective angles remain blind.
- Two distinct angles can remove the algebraic rank defect, but the measurement model can remain blind if its score is zero or symmetric.
- Additional QAOA layers help only if they introduce linearly informative effective angles; repeating the same sensitivity direction does not change rank.
- The two terms need not transform identically for labels to fail. Under the compiled-angle model with virtual Z frames (draft derivation above), the additive term flips with the label and the multiplicative term is label invariant in the logical frame; the label-invariant term is then confounded with the unknown ideal response, so labels identify `phi` but not `epsilon` without ideal values. A direct-phase rank count that treats `g_t(theta) = +/- theta` as two distinct effective angles would wrongly report full rank; rank must be counted in the logical frame and with the nuisance `r` (I1 and I3), not in the physical frame or with I2.

### 3.4 Gate-1 minimum simulation specification

This is a design specification, not authorization to run it. Part 1 freezes the exact grid and seeds before execution.

| Item | Minimum specification |
|---|---|
| Qubits | 2 and 3 qubits |
| QAOA structure | One cost layer (`p = 1`) for the primary minimum test; `p = 2` only as a prespecified secondary rank check |
| Graphs | One 2-qubit edge and a fixed 3-qubit path; noiseless analytic ground truth available |
| Candidates | Single-candidate/single-angle blind control; a same-angle candidate pair blind control; a distinct-`gamma` pair chosen without using simulated outcomes |
| Frozen E2 semantics | Match the predecessor's compiled cost construction as the reference: logical `RZZ(theta)` compiles to `CX-RZ(theta)-CX`, the central cost `RZ` is tagged, and the primary model applies `RZ((1+epsilon)*g_t(theta) + phi)`. The new label-absorption rule must be written separately; it is not inherited from predecessor P3, which framed only hard `CX` gates. |
| Label design | A finite balanced label set with the exact map `g_t(theta)` listed; labels and shot allocation fixed in advance |
| Parameters | A symmetric development-only grid for `epsilon` and `phi`, including zero and local alternatives; values selected by analytic sensitivity and power, not by desired outcomes |
| Statistic | Primary Gate-1 statistic: a label-outcome score or likelihood estimator for `(epsilon, phi)` defined before simulation. Report bias, covariance, Fisher-information condition number/rank, convergence, and failure status. |
| Required negative controls | Label permutation; single angle; identical candidate angles; a measurement basis with analytically zero first-order sensitivity; an error model where `epsilon` and `phi` transform identically |
| Gate-1 outputs | Analytic rank table, noiseless likelihood check, parameter-recovery table, numerical convergence log, and a signed mismatch report between prediction and observation |
| Information reporting | I1, I2, and I3 (Section 3.3) reported separately for every design; the Gate 1A verdict cites only I1 and the admissible part of I3 |
| Additional analytic control | The `phi = 0` label-contrast identity: under the frozen model, the predicted value of every label-contrast mean (identically zero under the compiled-angle model with virtual Z frames, per the draft) is written down before the noiseless check |

#### 3.4.1 Gate 1B fallback sensor: P-amp (fixed before Gate 1A is run)

P-amp is a known-reference sensor. Its own ideal outcome is computable classically by construction; that is declared as a runtime-computable quantity, as in Chapter 2's rule, and it never reads the ideal value of a target circuit. P-amp circuits run without RC labels, so the frame bookkeeping of Section 3.3 does not enter.

| Item | Fixed specification |
|---|---|
| Block | The same tagged cost construction as the target: `B(theta) = CX(c,t) - RZ_tagged(theta) on t - CX(c,t)`, with control `c` prepared in `|0>`, so that `B(theta)` acts ideally as `RZ(theta)` on the target qubit `t`, prepared in `|+>` |
| Repetition circuits | `R(m, theta) = B(theta)^m` for `m` in `{1, 4, 16}` and `theta` in `{pi/8, pi/4}` (6 circuits) |
| Echo circuits | `E(m) = [B(pi/4) B(-pi/4)]^m` for `m` in `{1, 4, 16}` (3 circuits) |
| Measurement | Target qubit in the X and in the Y basis for every circuit: 9 circuits x 2 bases = 18 settings |
| Phase model (all three E2 models in Section 3.3 agree here) | Repetition: total phase `m*theta + m*(epsilon*theta + phi)`. Echo: `2*m*phi` (the multiplicative term cancels, the mechanism behind the Chapter 1 folding blindness). Requires that negative commanded angles follow the same error law; otherwise the model is violated and P-amp fails. |
| Statistic | Per setting pair, `u_hat = atan2(<Y>_hat, <X>_hat)`. Residual phases are formed by subtracting the known `m*theta` and unwrapping sequentially in `m`. `(epsilon_hat, phi_hat)` is the equal-weight least-squares solution of: residual `R(m,theta)` = `m*theta*epsilon + m*phi`; residual `E(m)` = `2*m*phi`. |
| Budget | Exactly the sensing share `f*N` of the fixed total budget (`f = 0.10` as a placeholder carried from Chapter 2; `f` and `N` frozen in Part 1 before Gate 1A), split equally over the 18 settings. Recorded in the cost ledger in circuits and shots. |
| Pass condition (a), analytic rank | The linear design matrix with rows `(m*theta, m)` for repetitions and `(0, 2*m)` for echoes has rank 2, and the known-reference Fisher information is full rank, without any ideal target value. |
| Pass condition (b), noiseless recovery | On the frozen `(epsilon, phi)` grid, the noiseless numerical check recovers injected values with absolute error at most `1e-8`. |
| Pass condition (c), budget | At the frozen `N` and `f`, the analytic standard error of `epsilon_hat` (visibility 1, shot noise only) is at most `epsilon_min / 2.8` (two-sided alpha 0.05, power 0.8); `epsilon_min` is frozen in Part 1 (placeholder `0.02`). |
| Pass condition (d), no phase ambiguity | For every grid point, `16 * |epsilon*theta + phi| < pi/2` and `32 * |phi| < pi/2`. If the frozen grid violates this, P-amp fails; the grid is not shrunk afterwards. |
| Prespecified failure modes (Part 2 onward) | Visibility decays with `m` (decoherence); the error in `B(theta)` repeated differs from the error in the target context (crosstalk, schedule dependence); drift between sensing and execution; asymmetric error law for negative angles; noise above the robustness threshold of the repetition ladder (added 2026-11-20, see `docs/literature/notes/phase_estimation_pamp_boundary.md`). |
| Novelty boundary | P-amp is close to robust phase estimation (Kimmel, Low & Yoder 2015; Rudinger et al. 2017; metadata and abstracts checked 2026-11-20, full text not read). No novelty is claimed for the sensor. Whether to adopt the RPE estimator or RPE consistency checks instead of plain least squares is an owner decision that must be made before the week-4 freeze. |

### 3.5 Endpoints and policies

#### Primary endpoint -- one only

**Paired improvement in frozen decision value of the deployable sensor policy over the development-locked best fixed policy, under one fixed total execution budget.** "Sensor" means the sensor that passed Gate 1 (RC labels via Gate 1A, otherwise P-amp via Gate 1B); the endpoint text is otherwise unchanged by the routing.

For a unit `u`, define a loss before holdout data exist:

```text
L_u = 1{an answer is issued and the selected candidate is wrong}
      + lambda_A * 1{abstain}
      + lambda_F * 1{correction attempted but execution fails}.
```

All sensing, calibration, correction, and re-execution shots are charged to the same `N`; classical time and circuit count are reported separately. `lambda_A` and `lambda_F` require justification and user approval before freeze. The primary statistic is the shared-unit paired mean

```text
Delta_V = mean_u[L_fixed,u - L_policy,u].
```

The deployable policy may use only runtime data from the Gate-1 sensor (label-conditioned data, or P-amp data under Gate 1B), known circuit metadata, and quantities declared computable at runtime. It may not read the ideal target value, true `epsilon`, error-structure label, future calibration, or holdout outcomes. The fixed comparator is selected once on development data from no action, always recalibrate, and always abstain, then locked. The confirmatory success rule and graph-cluster uncertainty method are set by Part 3 power analysis and independently timestamped before holdout.

#### Secondary endpoints

- False-certification rate and decision coverage, reported separately so the scalar loss cannot hide the tradeoff.
- Calibration of `epsilon_hat` and `phi_hat` under the frozen model.
- Gap-bias and flip-sign prediction performance.
- Regret relative to an oracle, labelled secondary because the oracle is not deployable.
- Sensitivity of `Delta_V` to prespecified alternative loss weights.

#### Exploratory analyses

- Device-parameter simulation, explicitly not hardware evidence.
- `p = 2` and additional graph families.
- Common random compilations: one-day variance-component check only. Estimate the share of `Var_t(mu_A(t)-mu_B(t))` in total gap variance. If the prespecified share is negligible, stop; never interpret narrower intervals as bias correction.

### 3.6 Prespecified method failure conditions

| Method or claim | It should fail when... |
|---|---|
| Label identification of `epsilon` (Gate 1A) | Only one effective angle is observed; the label map does not vary the relevant control; Z frames are virtual and the multiplicative term is label invariant in the logical frame (draft prediction: zero admissible information for `epsilon` at `phi = 0`); the error is defined on the logical angle; or the measurement score is zero. |
| P-amp identification of `(epsilon, phi)` (Gate 1B) | Visibility decays with repetition; the repeated block does not reproduce the target-context error; negative angles follow a different error law; drift between sensing and execution; or phase ambiguity at the largest repetition count. |
| Parameter-to-decision transfer | The candidate gap is insensitive to the identified parameter, other unmeasured errors dominate, or equal parameter errors induce different biases across circuit contexts. |
| Recalibration | The error drifts before re-execution, the correction model is misspecified, the correction uncertainty exceeds the margin, or re-execution consumes too much budget. |
| Abstention | The score is not calibrated for decision error, coverage loss dominates the fixed loss, or alarms occur under matched nulls. |
| Three-action policy | Treatment benefit has the same sign for every unit, one action dominates after costs, or the policy needs oracle error labels. |
| Local Fisher analysis | The model is globally aliased, far from the local point, on a parameter boundary, or the likelihood is nonregular. |
| Finite-shot lower bound | The chosen two points are physically irrelevant, not inside the frozen model class, or the resulting bound is too loose at the study budget. |
| Common random compilations | Between-compilation variance is negligible relative to conditional shot noise; covariance is nonpositive; or bias remains and narrower intervals increase false certification. |

### 3.7 Theory that survives a failed Gate 1 (1A and 1B)

The following must be formulated without QAOA, E2, or RC-specific notation before the empirical construction is treated as successful:

1. A three-action risk identity for no action, correction, and abstention under a fixed sensing/action budget.
2. An action-selection blindness lemma: two latent states yield indistinguishable runtime evidence but have different optimal actions.
3. A finite-pilot lower bound on the probability of choosing the wrong action.
4. A value-of-information condition comparing the expected reduction in action loss with sensing cost.
5. A policy non-degeneracy definition and an honest fixed-action collapse result.

If Gate 1A and Gate 1B both fail, these results form the general chapter and the failed label construction is its first concrete example. The only replacement probe ever allowed is the P-amp fallback fixed in Section 3.4.1 before Gate 1A; no other probe is introduced after inspection.

## 4. Parallel preparation for Chapter 4

### 4.1 Status and authorization boundary

This section designs a possible monthly longitudinal study. It does not authorize any job, reserve a backend, or claim hardware feasibility. Before the first run, the complete protocol, circuit hashes, backend-selection rule, analysis, stopping rule, and data fields must receive an independent timestamp. Every monthly execution requires separate user authorization and a same-day platform/rule check.

### 4.2 Scientific purpose

Estimate how quickly a frozen runtime signal and correction become stale, without selecting months, qubits, or calibration windows for favorable behavior. This is Chapter 4 data collection, not confirmatory evidence for Chapter 3.

### 4.3 Minimal circuit panel

The exact backend basis must be checked before registration. The draft panel is intentionally small:

1. **Reference preparations:** `|0>`, `|1>`, `|+>`, and `|+i>` followed by X/Y/Z-basis measurements as applicable.
2. **Mixed preparation:** a recorded 50:50 classical random mixture of `|+>` and `|+i>` preparations, with the preparation label retained per circuit rather than pooled away. This tests whether drift conclusions survive a heterogeneous input distribution.
3. **Phase-sensitive sequence:** Ramsey-like `H -- phase operation -- H/S` variants at two frozen angles, only if the backend representation makes the phase operation physically meaningful.
4. **Two-qubit context:** the shortest supported entangling-gate echo or identity-like sequence on one frozen connected pair, with one fixed idle-depth control, to monitor context/crosstalk.
5. **Matched null:** logically equivalent circuits with no injected phase perturbation.

Virtual `RZ` operations may be frame updates rather than noisy physical pulses. If the backend cannot expose or implement a relevant physical control, the angle-over-rotation panel is `not feasible`; it is not silently replaced.

### 4.4 Backend and qubit selection rule

- Before registration, choose one backend that is available under the user's plan and supports the frozen circuits. Keep it for the series. Backend loss triggers a documented pause and protocol amendment, not opportunistic switching.
- Primary single qubit: the smallest-index operational qubit satisfying only prespecified functional requirements, not the best reported fidelity.
- Primary pair: the lexicographically first operational directed edge supporting the required entangling instruction.
- Fallbacks are ordered lexicographically and used only for a recorded unavailability reason. No same-month search across qubits is allowed.
- Calibration metrics are recorded after selection and are never used to choose the best-looking qubit unless that quality-based rule was independently timestamped before the series.

### 4.5 Monthly cadence and fields

Nominal cadence: one authorized session every 28--35 days for at least six months. A missed month stays missing; it is not backfilled with two runs.

Record at minimum:

- protocol version, repository commit, circuit manifest hash, and analysis version;
- authorization record and independent-registration identifier;
- backend name, service/channel, region if exposed, and backend status;
- UTC submission/start/completion timestamps and the calibration timestamp used by the provider;
- job ID, session ID if any, execution mode, shots, circuit count, and transpiler settings/seeds;
- physical qubit indices, directed coupling, native/basis instructions, layout and schedule metadata available to the user;
- public calibration fields available at run time: readout assignment metrics, T1, T2, gate error/duration, and their provider timestamps;
- randomized label, preparation label, angle, repetition/depth, and circuit hash for every aggregate count record;
- raw counts, failures, partial jobs, cancellation reason, queue/runtime metadata, and provider messages without credentials;
- environment, Qiskit/runtime versions, operating system, and analysis log;
- explicit evidence label `hardware-derived` and a note that one backend/time series does not establish generality.

### 4.6 Monthly analysis boundary

Monthly descriptive summaries may be generated, but the longitudinal hypothesis is scored only at frozen milestones. Repeated monthly viewing does not authorize changing circuits, qubits, thresholds, or the final test. Confidence sequences may be used only if derived and frozen before the first run.

## 5. Schedule

The detailed and editable schedule is maintained in
[`docs/schedule/research_schedule_v1.md`](schedule/research_schedule_v1.md).
It supersedes the earlier 24-week calendar in this section and expands the plan
to 26 weeks so that Gate 1 model review, independent verification, negative
branches, Chapter 4 preparation, and paper/reproducibility work are explicitly
budgeted. The scientific Part order, Gate criteria, and primary endpoint are
unchanged. Dates may move later; Part contents may not change in response to
delay or observed results.

## 6. Risks and kill conditions

| Risk | Early sign | Fastest check (no more than 2 days) | Triggered action |
|---|---|---|---|
| Labels do not act on the noisy physical quantity | Compiler absorbs labels as virtual frames while the injected error is unchanged | Print and algebraically audit the compiled operation/label map for 2--3 qubits; compare unitary and tagged-control parameters | Gate 1A fails; retain the RC-label blindness result; proceed only to the frozen Gate 1B |
| Frame covariance hides `epsilon` from labels | Draft derivation: in the logical frame the multiplicative term is label invariant; label contrast is identically zero at `phi = 0` | Review the draft proof in `docs/theory/gate1_frame_covariance_draft.md`; exact 2-qubit noiseless check of the `phi = 0` identity | Gate 1A fails as predicted; record as negative result; proceed only to the frozen Gate 1B |
| `epsilon` and `phi` are confounded | Admissible information (I1 plus admissible I3) rank 1 or extreme condition number in every allowed design | Symbolic/numerical rank calculation over the minimal angle set and negative controls, reporting I1, I2, I3 separately | Gate 1A fail -> frozen Gate 1B; if Gate 1B also fails, no adaptive empirical branch |
| P-amp fails | Rank, recovery, budget, or phase-ambiguity condition in Section 3.4.1 not met | Analytic standard error at the frozen `N` and `f`; noiseless recovery on the frozen grid | Stop the empirical policy branch; no third probe |
| Two candidate angles are algebraically different but measurement-blind | Distinct angles produce proportional or zero score vectors | Exact noiseless likelihood derivatives for the two circuits | Change no outcome-driven measurement; fail Gate 1A and follow the frozen Gate 1B |
| Vyas-style label statistic does not extend to angle-dependent QAOA | Parameter recovery works for a fixed phase but not for multiplicative errors across angles | Minimal 2-qubit noiseless/local-alternative test | Report limited transport; Gate 1A fails if the primary model fails, then frozen Gate 1B |
| Parameter estimate is not decision-relevant | Good `epsilon` recovery but no gap-bias/flip prediction | Exact derivative of the candidate gap with respect to `epsilon` on fixed development instances | Gate 2 fail; theory/negative result only |
| Correction creates an inverse crime | Recovery succeeds only when analysis and generator use the identical model | One misspecified-generator check fixed before evaluation | Classify model failure; do not claim deployability |
| Always-correct dominates | Correction benefit has one sign and sensing never changes the action | Development-only per-unit treatment-effect sign table | Gate 4 fail; report fixed-action collapse |
| Always-abstain wins because abstention is too cheap | Policy loss is minimized by zero coverage | Sensitivity calculation over justified `lambda_A` range before holdout | User must choose/justify loss; do not freeze an arbitrary favorable value |
| False-certification events are too rare | Power analysis cannot estimate policy value or an action stratum | Split-99 generator power analysis using the same unit hierarchy as holdout | Stop or enlarge the prespecified unit count before registration; never after holdout |
| Re-execution exceeds the budget | Correct action leaves too few target shots | Static budget ledger for all action paths | Gate 3 fail or simplify only according to a prewritten development option |
| Common random compilations add negligible information | Between-compilation component is tiny relative to conditional shot noise | One-day variance decomposition | Drop to a textual limitation or appendix; no further grid |
| Hardware `RZ` is virtual and does not instantiate the target error | Backend circuit/schedule shows only frame changes | Same-day dry compile and documentation check without submitting a job | Hardware angle panel `not feasible`; do not substitute a new experiment without amendment |
| Longitudinal backend disappears | Backend retirement or instruction-set change | Pre-session availability check | Record missing month; pause and amend before any backend change |
| Literature already covers the action rule | A source proves the same fixed-budget label-to-action claim | Full-text prior-art comparison of the eight priority sources | Narrow or stop novelty claim before implementation |

## 7. Priority reading list

Statuses below are copied exactly from the task specification and are not upgraded by inclusion in this plan.

**Update note (2026-11-20).** Later reading notes in `docs/literature/` record full-text reading of Wallman & Emerson 2016, Winick et al. 2022, and Vyas 2026 by an AI agent; the project owner has not yet confirmed them. The arXiv abstract page gives Vyas's title as *Recovering Coherent Errors from Randomized-Compiling Labels*, matching this table. The canonical states in this table stay unchanged until the owner confirms; see `docs/literature/source_ledger.md` for the current working state.

| Priority | Source and required status | Why it must be read | Relationship to Chapter 3 |
|---:|---|---|---|
| 1 | Wallman & Emerson 2016, *Physical Review A* 94, 052325 -- **verified (cited by the second project)** | Establish the actual randomized-compiling assumptions, easy/hard cycles, and gate-dependence bounds | Determines whether the proposed cost-rotation construction lies inside or outside the theorem and prevents an invalid claim that RC must fix or must fail on E2 |
| 2 | Vyas 2026, "Recovering Coherent Errors from Randomized-Compiling Labels," arXiv 2607.26756 -- **abstract checked only** | Identify the exact label statistic, Fisher-information statement, circuit assumptions, and reported limitations | Closest direct predecessor to label-based sensing; Chapter 3 must add decision relevance rather than repeat coherent-parameter estimation |
| 3 | Santos, Bar & Uzdin 2024, *npj Quantum Information* 10, 100 (Pseudo twirling) -- **abstract checked only** | Separate controllable rotation errors from other coherent errors and understand the control-sign requirements | Supports calibration as a possible action while delimiting what pseudo twirling itself changes |
| 4 | Bar, Santos & Uzdin, Layered KIK, *npj Quantum Information*, DOI 10.1038/s41534-026-01207-0 -- **abstract checked only** | Clarify what is new about layered amplification, dynamic circuits, and non-Clifford applicability | Prevents misusing Layered KIK as evidence that the E2 sensing/correction construction works |
| 5 | Henao, Santos & Uzdin 2023, *npj Quantum Information* 9, 120 (Adaptive KIK) -- **abstract checked only** | Understand its meaning of "adaptive," noise-strength signal, and integration with RC | Establishes the novelty boundary: adaptive mitigation coefficients are not the same as instance-wise action selection |
| 6 | Winick et al. 2022, arXiv 2212.07500 -- **abstract checked only** | Review RC's roles, variability reduction, coherent accumulation, crosstalk, and limitations | Supplies mechanisms and failure conditions for the RC action without assuming universal benefit |
| 7 | Kurita et al. 2023, *Quantum* 7, 1184 (RC + ZNE) -- **abstract checked only** | Understand the existing estimator-level RC+ZNE combination and its simulated setting | Prevents claiming that combining RC with mitigation is novel; Chapter 3 contribution must remain at decision/action level |
| 8 | Zhang, Seshadri & Knill 2026, arXiv 2602.08114 (sequential spot-checking) -- **abstract fragment only** | Determine whether its non-i.i.d. spot-checking allocation or certificates apply to runtime sensing | Primary bridge to Chapter 4 and a possible finite-budget tool; not assumed to solve action selection |

### Additional literature to verify before citation

The following are research needs, not verified bibliography entries. No volume, pages, or DOI are asserted here.

- **Unverified:** original predictive-biomarker and treatment-by-marker interaction methods, for separating error detection from correction-benefit prediction.
- **Unverified:** biased best-arm identification and best-arm identification with misspecified rewards, for the decision-level lower bound.
- **Unverified:** value-of-information and reject-option decision theory with explicit abstention cost.
- **Unverified:** common-random-number designs for paired quantum circuit comparisons, only to position the one-day CRN check.
- **Unverified:** time-uniform confidence sequences and change-detection methods appropriate to irregular monthly hardware observations.

Every source entering the bibliography must be opened at an original publisher, DOI, or arXiv page and checked for authors, title, venue, bibliographic fields, and the precise claim used.

## 8. Decisions required from the user

At most five decisions block a future freeze; none blocks storing this planning draft.

1. **Work capacity:** confirm or replace the planning assumption of 8--10 hours per week starting 2026-11-23.
2. **Abstention loss:** what practical harm ratio should `lambda_A` represent relative to issuing a wrong answer? If there is no defensible single value, approve a constrained primary endpoint instead of a scalar loss before Part 3.
3. **Correction action:** should "correct" mean a second execution with an estimated angle recalibration, or may it include a separately defined compiled correction? The primary action must be one concrete operation.
4. **Longitudinal hardware:** should Chapter 4 protocol design begin in parallel, knowing that registration and every monthly job still require separate authorization and may be declared infeasible?
5. **Writing target:** should Chapter 3 be planned as a standalone two-column article first, with the dissertation chapter adapted later, or as a dissertation chapter with a later article extraction?

## Planning acceptance checklist

- [ ] User decisions in Section 8 recorded.
- [ ] Full-text prior-art review completed without upgrading unverified entries prematurely.
- [ ] Part 1 mathematical specification approved.
- [ ] Frame-covariance draft (`docs/theory/gate1_frame_covariance_draft.md`) reviewed by the user: proved, corrected, or rejected.
- [ ] P-amp specification (Section 3.4.1), `N`, `f`, and `epsilon_min` frozen and committed before any Gate 1A check is run.
- [ ] Primary loss or constrained endpoint justified.
- [ ] No noisy development data generated before the Part 1 prediction/model record is frozen and committed.
- [ ] No confirmatory data generated before adversarial audit, clean lock, and independent registration.
- [ ] No hardware job submitted without a separately registered protocol and explicit authorization.
