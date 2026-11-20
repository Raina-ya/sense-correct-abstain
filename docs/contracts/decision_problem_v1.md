# Decision-problem contract v1 (Main Task 1, Subtasks 1.1–1.4)

**Status:** owner-reviewed draft contract. First drafted 2026-11-20 (commit
`8dc782c`); revised 2026-11-20 after owner review, which recorded decisions
D1–D3, the issue-only comparator, the deployability clarification, and the
ideal-tie rule (§6, §7). **Not frozen**: it has no independent timestamp and is
not a protocol. It contains no experimental result. Items marked **[PROPOSED]**
are defaults that the owner has not yet ruled on; they are not decisions.

**Authority.** This contract implements Subtasks 1.1–1.4 of the research work
plan. Where it and [`../research_program_plan_v0.md`](../research_program_plan_v0.md)
disagree, the program plan governs. The owner-review changes are recorded in
the program plan's dated revision note (§8.1 there). Part content, Gate order,
the Gate 1A → 1B routing, and the primary endpoint `Delta_V` are unchanged.

**Theory companion.** The risk identity, pairwise switching conditions,
blindness lemma, finite-pilot lower bound, value-of-information decomposition,
collapse result, and non-degeneracy definition used here are in
[`../theory/three_action_theory_v1.md`](../theory/three_action_theory_v1.md).

---

## 1. Decision problem (Subtask 1.1)

### 1.1 Unit of analysis

An **evaluation unit** `u` is one complete run of the decision workflow under
the fixed budget `N`:

```text
u = (G, c, nu, r)
```

| Component | Meaning | Fixed by |
|---|---|---|
| `G` | Graph (MaxCut instance). | Population frozen in Part 2 (development) and Part 3 (confirmatory). |
| `c = (A, B)` | Candidate pair: two frozen QAOA parameter vectors for `G`, with their frozen logical cost angles `theta_{k ell}`. | Frozen with the graph; candidates are not chosen from simulated outcomes. |
| circuit instance | The compiled circuits of both candidates, the sensor circuits, and (for RC) the realized label draws `t`, with circuit hashes. | Compilation rule frozen in MT2 (`rc_construction_v1.md`, planned). |
| `nu` | Noise condition: the E2 model (primary: the synthetic compiled-angle model, §6 D1), the values `(epsilon, phi)`, and the nuisance noise `eta` (visibility, label-independent offset, any in-scope SPAM or control terms). | Grid frozen before the relevant Gate. |
| `r` | Replicate: seed for label draws and shot sampling. | SeedSequence keys frozen with the protocol. |

**Clustering.** Units sharing a graph `G` are dependent (shared ideal response
and candidate geometry). The primary resampling cluster is the graph
**[PROPOSED]**, in line with program plan §3.5 ("graph-cluster uncertainty
method"); the exact method is fixed in Part 3.

**Ideal ties (owner decision 2026-11-20).** A unit whose ideal gap
`g = mu_A - mu_B` is exactly zero has no unique correct top-1 decision and is
**excluded from the target population**. The ideal gap is used for this only in
the population-definition and scoring layer; the policy never sees `g` (§3).

- No near-zero scientific exclusion threshold is defined. Units with small but
  nonzero `|g|` stay in the population, however hard they are to decide.
- If floating-point evaluation makes an exact-zero test impossible, a
  **numerical equality tolerance** `tau_num` may be frozen with the population
  for the sole purpose of deciding whether a computed `g` equals zero. It is set
  from the arithmetic precision of the ideal-value computation, not from any
  decision consideration, and it is not a **scientific indifference region**:
  it may not be widened to exclude units that are merely difficult.

### 1.2 Latent state

```text
vartheta = (r_ideal, epsilon, phi, eta)
```

- `r_ideal`: the ideal (noiseless) response of every circuit in the unit; it
  determines the ideal candidate values `mu_A, mu_B`, the ideal gap `g`, and the
  correct candidate `k*(vartheta) = argmax_k mu_k` (unique, since `g != 0`).
- `epsilon`: multiplicative angle error (E2); `phi`: additive phase. Under the
  primary model (§6 D1) a physical tagged `RZ(a)` is implemented as
  `RZ((1+epsilon) a + phi)`, with `a = s_t theta` after sign-flip label
  absorption and Z labels as error-free virtual frame updates.
- `eta`: nuisance noise in scope (visibility, offsets, label-dependent terms
  when included).

The latent state is never available to the deployable policy. It is available
to the scoring layer, which computes losses after the run.

### 1.3 Runtime observations and timeline

```text
Stage 0  metadata m          circuits, logical angles, label design, budget split   (known before execution)
Stage 1  X1 = (X_S, X_T0)    sensor data (n_S shots) + initial target data (n_T0)  (runtime)
Stage 2  a = pi(m, X1)       action in {N, C, A}
Stage 3  N: issue delta_0(X_T0)
         C: kappa_hat = kappa(m, X1); recalibrate; run n_C corrected shots -> X_C; issue delta_C(X_C)
         A: issue nothing
```

- `X_S` comes from the sensor that passed Gate 1 (RC-label data via Gate 1A,
  otherwise P-amp data via Gate 1B; program plan §3.2, routing note).
- `delta_0(X_T0)` **[PROPOSED]**: the candidate with the larger empirical mean
  score from the initial target shots; an exact tie is broken toward candidate
  `A`, with the tie recorded. (Any tie rule is acceptable if it is frozen and
  does not depend on outcomes.)
- `delta_C(X_C)`: the same rule applied to the corrected-execution data **only**.
  `X_T0` is never pooled with `X_C` (§6 D3).

### 1.4 Action semantics

| Action | Meaning |
|---|---|
| **N, no action (issue)** | Issue `delta_0`, the decision produced by the original execution. |
| **C, correct** | Estimate `(epsilon_hat, phi_hat)` from `X1`, recalibrate every tagged cost rotation (§6 D3), re-execute **both** candidate circuits with the reserved `n_C` shots under the same frozen compilation rule as the initial execution, and issue `delta_C(X_C)`. |
| **A, abstain** | Withhold the decision; incur `lambda_A = 1/4`. |

**Correction failure.** A correction "fails" when the corrected execution does
not produce a decision. **[PROPOSED]** failure events, frozen as a closed list:

1. `kappa_hat` is undefined (estimator does not converge, phase-unwrapping or
   no-alias condition violated, division by a zero-information quantity,
   `1 + epsilon_hat <= 0`);
2. `kappa_hat` falls outside the frozen admissible correction range;
3. the corrected circuit cannot be compiled under the frozen compilation rule;
4. the corrected execution would exceed the reserved `n_C`.

After a failure **no answer is issued** and the loss is `lambda_F` only; there
is no fallback to `delta_0` (§6 D2).

### 1.5 Budget and resource ledger

One fixed total budget `N` (shots) per unit. Every shot from sensing, reference,
calibration, correction estimation, and corrected re-execution is charged to
`N`. Classical computation time and circuit count are reported separately and
are not part of `N`.

**Fixed reserve (owner decision D3).** The split `N = n_S + n_T0 + n_C` is fixed
in advance for the sensor policy. `n_C` is a reserve for the corrected
re-execution.

| Path | Shots executed | Shots charged to the policy's design |
|---|---|---|
| N | `n_S + n_T0` | `N` (the unused reserve `n_C` is part of the design and is **not** reallocated) |
| C | `n_S + n_T0 + n_C` | `N` |
| A | `n_S + n_T0` | `N` (reserve unused, not reallocated) |

The ledger records executed shots per path and the unused reserve separately,
but the policy's budget is `N` on every path. The split and the fixed-reserve
rule cannot be changed to an adaptive reallocation after any result is seen.

### 1.6 Loss components (kept separate)

| Component | Event | Enters the primary loss as |
|---|---|---|
| Wrong-answer loss | A decision is issued (path N, or path C without failure) and it differs from `k*`. | `1` |
| Abstention loss | The policy chose A. | `lambda_A = 1/4` |
| Correction failure | The policy chose C and a failure event in §1.4 occurred (no answer is issued). | `lambda_F = 1/4` |
| Correction harm | C ran without failure but `delta_C` is wrong (including when `delta_0` was right). | Counted as wrong-answer loss; also reported separately as a secondary count. |
| Resource consumption | Shots executed per path, unused reserve, circuits, depth, classical time. | Not in the loss (budget is fixed); reported in the ledger. |

### 1.7 Fixed comparators

The action classes remain N, C, and A; no fourth primary action is added.

| Comparator | Definition |
|---|---|
| **Issue-only comparator** (fixed no-action / always-issue) | Development-locked choice between two prespecified allocations, both of which always take N: **(i) full-target**: all `N` shots on the target, no sensing, issue `delta_0`; **(ii) sensor allocation**: the sensor policy's split `(n_S, n_T0, n_C)` is executed exactly as the policy would, but the sensor observation is ignored and N is always taken (`delta_0` from the `n_T0` shots). The allocation with the lower development loss is selected once and locked before the holdout. The comparator never reads unit-level sensor observations to choose an action. |
| **Always correct** | The sensor policy's allocation `(n_S, n_T0, n_C)`; C is always taken. Defined only if a sensor passed Gate 1. |
| **Always abstain** | Always A; loss exactly `lambda_A = 1/4`. |

`L_fixed` is the loss of the best of these three, selected **once** on
development data under the primary loss and locked before the holdout.
**[PROPOSED]** tie order: issue-only, then always correct, then always abstain;
within the issue-only comparator, a development tie goes to the full-target
allocation. All fixed-policy results, including both issue-only allocations,
are retained and reported (work plan, Subtask 5.3).

**Why allocation (ii) is included.** Under coherent bias that flips the
decision, moving shots away from the target can *lower* the issue error (it
tends toward 1/2 instead of 1). Without (ii), a policy that always issues at the
sensor allocation could beat a full-target comparator through the allocation
alone, with no use of sensor information. Theory note, Proposition P2, shows
that with (ii) included, no information-free policy has positive population
`Delta_V`.

---

## 2. Evidence hierarchy (Subtask 1.2)

Every claim in this project carries exactly one evidence type. Types are never
merged, and a weaker type is never relabeled as a stronger one.

| Type | What it can establish | What it cannot establish | Label used in documents |
|---|---|---|---|
| Analytic | Identities, rank conditions, risk decompositions, blindness results, finite-sample lower bounds — within the stated model. | That the model describes a device. | `analytic` + proof status (below) |
| Noiseless simulation | Exact semantic checks, likelihood checks, parameter recovery, implementation verification. | Robustness to noise; decision value. | `noiseless simulation` |
| Noisy simulation | Decision relevance, policy value, action frequency, robustness under frozen noise models. | Hardware behavior. | `noisy simulation` |
| Device-parameter simulation | Behavior of a simulation parameterized by published device numbers. | **Never** hardware evidence. | `device-parameter simulation (not hardware evidence)` |
| Hardware-derived | Observations from an authorized run under a separately registered addendum. | Generality beyond the backend and interval observed. | `hardware-derived` |

**Model scope.** Every analytic or simulated result under the primary E2 model
is a result about the **synthetic compiled-angle model** (§6 D1). It is not an
experimental conclusion about virtual-Z hardware.

**Proof status for analytic claims.** `proved (draft, owner review pending)`;
`corrected` (a previously stated result whose statement or proof was changed);
`downgraded`; `sketch`; `conjecture`; `conditional example`; `inherited`
(proved in a completed project, reused with its stated scope). A **numerical
check** (exact arithmetic or enumeration of one or a few examples) is reported
under the claim it checks, labeled `numerical check`, and never counts as a
proof.

**Literature status** is reported separately from evidence type, as in
[`../literature/source_ledger.md`](../literature/source_ledger.md): metadata
verified / abstract checked / full text read (and by whom). A literature
statement does not become project evidence.

**Hardware.** No hardware-derived evidence is produced under this plan without
an independently timestamped addendum and explicit authorization of every run.

---

## 3. Deployability boundary (Subtask 1.3)

### 3.1 Allowed inputs to the deployable sensor and policy

1. Measured runtime outcomes of the unit (`X_S`, `X_T0`, and on path C, `X_C`
   for `delta_C` only).
2. Recorded randomized-compiling labels of the unit.
3. Circuit metadata available before execution (graph, candidate angles,
   compiled circuits, label design, budget split).
4. Analytically known reference quantities declared runtime-computable before
   any data exist (for example the ideal outcome of a P-amp reference circuit,
   or the ideal value of a Clifford twin; never of a target circuit).
5. Calibration quantities whose acquisition shots are charged to `N`.
6. **Development-locked rule constants** (owner decision 2026-11-20):
   thresholds, transfer-rule coefficients, tie rules, and other rule constants
   fixed on development data only and locked before the data they are applied
   to. They may not be refit on confirmatory data.

### 3.2 Forbidden inputs

1. The ideal target expectation or the ideal target gap `g`.
2. The true injected `epsilon`, `phi`, or `eta`.
3. The error-structure label (which E2 model or noise condition is active).
4. Simulator-only likelihood derivatives (for example the derivative of the
   ideal target response, `dF_r/du`), unless charged as calibration under 3.1.5.
5. Future calibration information.
6. Confirmatory outcomes during rule construction.

### 3.3 Enforcement (to be implemented in MT3 and later)

- Every policy-input field is tagged with its class (3.1.x) in the data schema.
- Following the predecessor's pattern (audit §4), tests reject sensor and
  policy functions whose signatures accept forbidden fields, and raw run records
  must not contain target ideal values. Fields such as the true `epsilon` and
  the structure label live only in the scoring layer.
- Gate 1A reports I2 (known-response information) as a diagnostic only; it can
  never support a deployability claim (program plan §3.3).

---

## 4. Primary endpoint (Subtask 1.4)

### 4.1 Loss

For evaluation unit `u`:

```text
L_u = 1{an answer is issued and the selected candidate is wrong}
      + lambda_A * 1{the policy abstains}
      + lambda_F * 1{correction is attempted but execution fails},

lambda_A = 1/4,   lambda_F = lambda_A = 1/4,   no answer is issued after a failed correction.
```

**Meaning of `lambda_A = 1/4`.** It is an **owner-chosen normative loss
ratio**: one wrong answer costs as much as four abstentions. It is not an
objective constant estimated from Chapter 2 data, and it is not claimed to be a
universally applicable utility weight. `lambda_F = lambda_A` treats a failed
correction as an involuntary abstention, so that attempting a correction can
never be a cheaper substitute for abstaining.

**Alternative-loss sensitivity.** Prespecified alternative loss weights may be
analyzed, but only as a **secondary endpoint**. They are never used to rescue,
replace, or reinterpret the primary `Delta_V`.

### 4.2 Sole primary statistic

```text
Delta_V = mean_u [ L_fixed,u - L_policy,u ]
```

- `L_policy,u`: loss of the deployable sensor policy on unit `u`.
- `L_fixed,u`: loss of the development-locked best fixed comparator (§1.7) on
  the same unit (paired, shared units).
- Both under the same total budget `N`, with every sensing, reference,
  calibration, correction, and re-execution shot charged.
- "Sensor" means the sensor that passed Gate 1.
- Uncertainty: graph-clustered; method and success rule fixed by the Part 3
  power analysis and independently timestamped before the holdout.

### 4.3 Nonevaluable and failed units

**[PROPOSED]** Every unit enters `Delta_V`. A correction failure is a loss event
(§1.6), not a missing value. A unit is nonevaluable only for an infrastructure
reason recorded in a closed list (for example a crashed run); nonevaluable units
are reported with counts and are not silently dropped. The exact handling is
frozen in Part 3 (work plan, Subtask 6.2).

### 4.4 Secondary endpoints (from program plan §3.5; not used to rescue the primary)

False-certification rate and coverage, reported separately; calibration of
`epsilon_hat` and `phi_hat`; gap-bias and flip-sign prediction; regret to the
non-deployable oracle; sensitivity of `Delta_V` to prespecified alternative
loss weights; correction-harm count (§1.6).

---

## 5. Gate 1 dependence of this contract

| Gate 1 outcome | Consequence for this contract |
|---|---|
| Gate 1A passes | Sensor = RC labels; all actions defined. |
| Gate 1A fails, 1B passes | Sensor = P-amp; all actions defined; no RC-label sensing claim. |
| Gate 1A fails only for `epsilon` but labels support a deployable test of `phi != 0` | Recorded as a Gate 1A failure for `epsilon`. Abstention can use the test; correction cannot (D3 needs `epsilon_hat`). Routing still goes to Gate 1B. |
| Both fail (Branch C) | Action C has no sensor; the empirical policy branch stops. The contract remains the definition used by the theory chapter. |

The draft frame-covariance derivation predicts a Gate 1A failure under the
primary model. That prediction is not a result: Gate 1A is still tested formally
against its frozen criterion (program plan §3.2).

---

## 6. Owner decisions (recorded 2026-11-20)

The option tables presented for these decisions are in commit `8dc782c`
(this file, §6). Only the decisions and their boundaries are kept here.

### D1 — Primary E2 placement: D1-b, as a synthetic compiled-angle model

**Primary model.** Compiled-angle model with virtual-Z frames and sign-flip
absorption: each physical tagged rotation with commanded angle `a = s_t theta`
is implemented as `RZ((1+epsilon) a + phi)`; Z labels are error-free virtual
frame updates.

**Boundaries.**

1. Until there is evidence of a physical pulse or control carrier for an
   angle-proportional `RZ` error, this model is called the **synthetic
   compiled-angle model** in every document.
2. Conclusions under this model may not be extrapolated to experimental
   conclusions about real virtual-Z hardware.
3. **D1-a (logical-angle model)** is kept as a regression and negative control
   (labels blind by construction). It is not a co-primary model.
4. **D1-c (wrapped-Z absorption)** is neither a primary nor an alternative
   success model. It is listed only as a non-adopted model variant, unless it is
   first shown that the actual representation of a named compiler or backend
   matches it.
5. **D1-d (physical-control model)** is recorded as **not modeled**. No
   pulse-level simulator is added.
6. Gate 1A is tested formally under its frozen criterion even though the draft
   predicts failure; the prediction is never written as a result.

### D2 — Losses and failure semantics

- Primary `lambda_A = 1/4`: owner-chosen normative loss ratio (one wrong answer
  = four abstentions); not estimated from Chapter 2 data and not a universal
  utility weight.
- `lambda_F = lambda_A = 1/4`.
- After a correction failure, no answer is issued; there is no fallback to
  `delta_0`.
- Prespecified alternative-loss sensitivity analyses are secondary only and
  cannot rescue the primary `Delta_V`.

### D3 — Correction action

- **D3-a.** Estimate the angle error, recalibrate, and fully re-execute both
  candidate circuits. Under the primary linear model, each tagged rotation whose
  intended physical angle is `a` is commanded at
  `a' = (a - phi_hat) / (1 + epsilon_hat)`, so that the implemented angle is
  `(1+epsilon) a' + phi`, which equals `a` when the estimates are exact. The
  correction therefore needs both `epsilon_hat` and `phi_hat`.
- **Shot path: fixed reserve.** `n_C` is reserved in advance. Paths N and A do
  not reallocate the reserve; the unused reserve is still part of that policy's
  fixed budget design (§1.5). The rule cannot be changed to adaptive
  reallocation after results are seen.
- **Decision data.** The corrected decision uses `X_C` only; uncorrected `X_T0`
  is not pooled with `X_C`.

---

## 7. Plan issues found while drafting and their resolution

| # | Issue | Resolution (2026-11-20) |
|---|---|---|
| 1 | Development-locked rule constants were not on the deployability list. | Added (§3.1 item 6); program plan revision note §8.1. |
| 2 | Budget path of C was unspecified. | Fixed reserve (D3; §1.5). |
| 3 | Post-failure semantics was unspecified. | No answer after failure (D2; §1.4). |
| 4 | Fewer target shots do not always mean higher error under coherent bias. | Kept as a stated fact; handled by the issue-only comparator (§1.7). |
| 5 | Decision-ID numbering differed between the work plan and the program plan. | Index added to program plan §8.1; work plan cross-reference corrected. Numbering only. |
| 6 | Ideal ties were unspecified. | Exact `g = 0` excluded; only a numerical equality tolerance allowed (§1.1). |
| 7 | M1 versus MT1 "done". | M1 achieved at `8dc782c`; MT1 status updated in the work plan after this revision. |
| 8 | Comparator loophole (allocation-only gains). | Issue-only comparator with two prespecified allocations (§1.7); theory note P2 corrected. |

**Still open (raised by the P2 correction; owner ruling needed before the
comparator set is frozen).**

- **Metadata-only policies.** P2 covers policies whose action does not depend on
  the unit at all. A policy that chooses its action from circuit metadata alone
  (an allowed input, §3.1 item 3), without any sensor observation, could beat
  the single best fixed comparator by taking different fixed actions in
  different metadata strata, and would then show `Delta_V > 0` without using
  runtime evidence. This draft does not change the comparator set; options
  include reporting a development-locked metadata-only comparator as a
  secondary diagnostic, or forbidding metadata-only action variation in the
  policy class.
- **Finite-sample comparator selection.** P2 is a population statement. With
  estimated development losses, the locked comparator (or the issue-only
  allocation) can be mis-selected. An information-free policy can then show a
  positive holdout `Delta_V` only through that development mis-selection; this
  is to be covered by the Part 3 uncertainty method, not by P2.
