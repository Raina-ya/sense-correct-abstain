# Decision-problem contract v1 (Main Task 1, Subtasks 1.1–1.4)

**Status:** draft contract, 2026-11-20, written by Claude for owner review.
**Not frozen.** It has no independent timestamp and is not a protocol. It
contains no experimental result. Items marked **[OWNER: D1/D2/D3]** cannot be
filled in until the owner records those decisions (see §6 and
[`../schedule/research_schedule_v1.md`](../schedule/research_schedule_v1.md),
"Pending decisions"). Items marked **[PROPOSED]** are defaults proposed by this
draft that the owner can accept or replace; they are not decisions.

**Authority.** This contract implements Subtasks 1.1–1.4 of the research work
plan. Where it and [`../research_program_plan_v0.md`](../research_program_plan_v0.md)
disagree, the program plan governs; disagreements found while writing it are
listed in §7 instead of being resolved here. Part content, Gate order, and the
primary endpoint are unchanged.

**Theory companion.** The risk identity, pairwise switching conditions,
blindness lemma, finite-pilot lower bound, value-of-information condition, and
non-degeneracy definitions that this contract relies on are in
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
| `nu` | Noise condition: the primary E2 model **[OWNER: D1]**, the values `(epsilon, phi)`, and the nuisance noise `eta` (visibility, label-independent offset, any in-scope SPAM or control terms). | Grid frozen before the relevant Gate. |
| `r` | Replicate: seed for label draws and shot sampling. | SeedSequence keys frozen with the protocol. |

**Clustering.** Units sharing a graph `G` are dependent (shared ideal response
and candidate geometry). The primary resampling cluster is the graph **[PROPOSED]**,
in line with program plan §3.5 ("graph-cluster uncertainty method"); the exact
method is fixed in Part 3.

**Ideal ties.** A unit whose ideal gap `g = mu_A - mu_B` satisfies
`|g| <= g_tie` has no well-defined correct candidate. **[PROPOSED]** Such units
are excluded when the population is defined, using the ideal gap in the scoring
layer only, with `g_tie` frozen with the population (for example a small
multiple of numerical precision). The policy never sees `g` (§3). See §7, item 6.

### 1.2 Latent state

```text
vartheta = (r_ideal, epsilon, phi, eta)
```

- `r_ideal`: the ideal (noiseless) response of every circuit in the unit; it
  determines the ideal candidate values `mu_A, mu_B`, the ideal gap `g`, and the
  correct candidate `k*(vartheta) = argmax_k mu_k`.
- `epsilon`: multiplicative angle error (E2); `phi`: additive phase; their exact
  placement in the circuit depends on **[OWNER: D1]**.
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
         C: kappa_hat = kappa(m, X1); recompile; run n_C corrected shots -> X_C; issue delta_C(X_C)
         A: issue nothing
```

- `X_S` comes from the sensor that passed Gate 1 (RC-label data via Gate 1A,
  otherwise P-amp data via Gate 1B; program plan §3.2, routing note).
- `delta_0(X_T0)` **[PROPOSED]**: the candidate with the larger empirical mean
  score from the initial target shots; an exact tie is broken toward candidate
  `A`, with the tie recorded. (Any tie rule is acceptable if it is frozen and
  does not depend on outcomes.)
- `delta_C(X_C)`: the same rule applied to the corrected-execution data. Whether
  `X_T0` is pooled with `X_C` is part of **[OWNER: D3]**.

### 1.4 Action semantics

| Action | Meaning | Status |
|---|---|---|
| **N, no action (issue)** | Issue `delta_0`, the decision produced by the original execution. | Fixed by the work plan. |
| **C, correct** | Estimate a correction `kappa_hat` from `X1`, recalibrate, and perform the specified corrected execution with `n_C` shots; issue `delta_C`. | The concrete operation, its shot path, and data pooling are **[OWNER: D3]**. |
| **A, abstain** | Withhold the decision; incur `lambda_A`. | `lambda_A` is **[OWNER: D2]**. |

**Correction failure.** A correction "fails" when the corrected execution does
not produce a decision. **[PROPOSED]** failure events, frozen as a closed list:

1. `kappa_hat` is undefined (estimator does not converge, phase-unwrapping or
   no-alias condition violated, division by a zero-information quantity);
2. `kappa_hat` falls outside the frozen admissible correction range;
3. the corrected circuit cannot be compiled under the frozen compilation rule;
4. the corrected execution would exceed the remaining budget.

What happens after a failure is part of **[OWNER: D2]** (option "no answer
after failure" versus "fallback to `delta_0`"; §6).

### 1.5 Budget and resource ledger

One fixed total budget `N` (shots) per unit. Every shot from sensing, reference,
calibration, correction estimation, and corrected re-execution is charged to
`N`. Classical computation time and circuit count are reported separately and
are not part of `N`.

| Path | Shots consumed | Constraint |
|---|---|---|
| N | `n_S + n_T0` | `<= N` |
| C | `n_S + n_T0 + n_C` | `<= N` |
| A | `n_S + n_T0` (already spent before the action is chosen) | `<= N` |

Whether `n_C` is a fixed reserve that stays unused on the N and A paths, or
whether the N path may spend it on more target shots, is part of
**[OWNER: D3]**; it changes `q_f` in the theory and the comparator definitions
below (§7, item 2).

### 1.6 Loss components (kept separate)

| Component | Event | Enters the primary loss as |
|---|---|---|
| Wrong-answer loss | A decision is issued (path N, or path C without failure) and it differs from `k*`. | `1` |
| Abstention loss | The policy chose A. | `lambda_A` **[OWNER: D2]** |
| Correction failure | The policy chose C and a failure event in §1.4 occurred. | `lambda_F` **[OWNER: D2]** (plus `1` if the fallback semantics is chosen and the fallback answer is wrong) |
| Correction harm | C ran without failure but `delta_C` is wrong (including when `delta_0` was right). | Counted as wrong-answer loss; also reported separately as a secondary count. |
| Resource consumption | Shots per path, circuits, depth, classical time. | Not in the loss (budget is fixed); reported in the ledger. |

### 1.7 Fixed comparators

| Comparator | Definition | Notes |
|---|---|---|
| Always issue | All `N` shots on the target; issue `delta_0`. No sensing. | This is the predecessor's all-target baseline (`q_0`). **[PROPOSED]** it uses the full `N`, not the sensing allocation, so that it is the strongest implementable "issue" policy at the same budget. |
| Always correct | Run the Gate-1 sensor, always perform C. | Defined only if a sensor passed Gate 1. Its allocation follows **[OWNER: D3]**. |
| Always abstain | Run nothing; risk is exactly `lambda_A`. | |

The best fixed comparator is selected **once**, on development data, under the
primary loss, and then locked. **[PROPOSED]** tie order if two comparators have
equal development loss: always issue, then always correct, then always abstain.
All three fixed-policy results are retained and reported (work plan, Subtask 5.3).

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

**Proof status for analytic claims.** `proved (draft, owner review pending)`;
`sketch` (argument outline with named gaps); `conjecture`; `inherited` (proved
in a completed project, reused with its stated scope). A **numerical check**
(exact arithmetic or enumeration of one or a few examples) is reported under the
claim it checks, labeled `numerical check`, and never counts as a proof.

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
6. **[PROPOSED clarification, §7 item 1]** Frozen rule constants: thresholds,
   transfer-rule coefficients, and tie rules fixed on development data and
   locked before the data they are applied to.

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
      + lambda_F * 1{correction is attempted but execution fails}.
```

The wrong-answer weight is normalized to 1. The values of `lambda_A`,
`lambda_F`, and the post-failure semantics are **[OWNER: D2]**. If D2 selects a
constrained endpoint instead of a scalar `lambda_A`, this section is rewritten
before any freeze (program plan §8, item 2, allows this option).

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
| Gate 1A fails only for `epsilon` but labels support a deployable test of `phi != 0` | Recorded as a Gate 1A failure for `epsilon`. Abstention can use the test; correction cannot (no estimate). Routing still goes to Gate 1B. |
| Both fail (Branch C) | Action C has no sensor; the empirical policy branch stops. The contract remains the definition used by the theory chapter. |

---

## 6. Owner decisions required (D1–D3)

These are listed as options with consequences. **No option has been chosen in
this document.** D1 is needed before M2 (and therefore before the conditional
likelihood); D2 and D3 are needed before the loss and correction action can be
written as final.

### D1 — Primary E2 placement

| Option | What is frozen | Consequences |
|---|---|---|
| D1-a Logical-angle model | E2 multiplies the logical angle before label absorption (what the predecessor implemented; audit §1). | Labels are blind to both `epsilon` and `phi` by construction, so Gate 1A fails analytically and almost trivially; the chapter runs through Gate 1B (P-amp). Existing predecessor tests serve as regression tests. The RC-label negative result is weak as a contribution because it follows from the definition. |
| D1-b Compiled-angle model, virtual Z frames, sign-flip absorption | Physical `RZ(a) -> RZ((1+epsilon)a + phi)` with `a = s_t theta`; Z labels are error-free frame updates. | Draft prediction (unreviewed): zero admissible information for `epsilon` at `phi = 0`, a deployable test for `phi != 0`, no estimate of `phi` without the response slope. If proved, this is a non-trivial negative identifiability result. Requires stating the physical carrier of an angle-proportional `RZ` error; on hardware where `RZ` is virtual (`mckay2017vz`) the model may have to be recorded as synthetic. |
| D1-c Compiled-angle model, wrapped Z absorption (`theta + pi`) | As D1-b, but Z labels are absorbed as wrapped angles before the error acts. | Labels then carry first-order information about `epsilon` even at `phi = 0`, but the signal comes from the compiler's representation (`epsilon * (+/- pi)` terms). Gate 1A could pass for a reason a reviewer may call an artifact; the representation must be shown to be real in a named compiler. |
| D1-d Physical-control model | The error acts on a pulse amplitude/duration or composite control parameter. | Most physically motivated, but the current simulator has no pulse or control model (audit §1); substantial new modeling. If it cannot be represented faithfully, the work plan requires recording it as "not modeled" rather than substituting a virtual rotation. |

Secondary/diagnostic status of the non-chosen models is fixed at the same time
(work plan, Subtask 2.1).

### D2 — Abstention loss `lambda_A`, failure loss `lambda_F`, post-failure semantics

**D2.1 `lambda_A` (or a constrained endpoint)**

| Option | Consequences |
|---|---|
| D2.1-a A single scalar `lambda_A` in `(0, 1/2)` (for example `1/4`: one wrong answer is as bad as four abstentions) | Keeps the single scalar endpoint unchanged. Abstention can be optimal. Theory note (Corollary 2): if the issued decision were the posterior-most-likely candidate, abstention could be optimal only for `lambda_A < 1/2`; because action N issues the fixed empirical decision `delta_0`, abstention can still be optimal above `1/2` when bias makes `delta_0` confidently wrong. |
| D2.1-b A scalar `lambda_A >= 1/2` | Abstention is chosen only where the conditional error of `delta_0` exceeds 1/2, i.e., where the bias is believed to flip the decision. Policies will abstain rarely; Gate 4 (non-degeneracy) becomes harder to pass via abstention. |
| D2.1-c A very small `lambda_A` (for example `<= 0.05`) | Risk listed in program plan §6: always-abstain may become the best fixed comparator, and `Delta_V` then measures how often the policy beats a zero-coverage rule. |
| D2.1-d Constrained endpoint: minimize the wrong-issue rate subject to coverage `>= c_min` (or the reverse) | Avoids choosing a harm ratio, but changes the form of §4 and requires a constrained comparator and a different uncertainty method; must be written and frozen before Part 3. |

For orientation only (arithmetic on inherited Chapter 2 results, not evidence
for any value): for the E2 structure, the predecessor's alarm rule lowered
false certification from `0.0609` to `0.0159` while coverage fell from `0.6025`
to `0.300` (audit §6). Under a scalar loss that rule beats certify-only exactly
when `lambda_A < 0.045 / 0.3025 ≈ 0.149`. The chapters are not directly
comparable: in Chapter 2 an uncertified decision already counted as "not
covered", while here action N issues regardless of the interval.

**D2.2 `lambda_F`**

| Option | Consequences |
|---|---|
| D2.2-a `lambda_F = lambda_A` | A failed correction is an involuntary abstention. Simple; no incentive to "use C as a cheap abstention". |
| D2.2-b `lambda_A < lambda_F < 1` | Penalizes the wasted resources and the late failure; correction becomes less attractive where the failure probability is high. |
| D2.2-c `lambda_F = 1` (or more) | Failure as bad as a wrong answer; strongly discourages C in uncertain regions; may push the policy toward collapse to N or A. |
| Constraint for every option | `lambda_F < lambda_A` is not recommended by this draft: a policy could then choose C where failure is likely as a cheaper substitute for A, which rewards failures. |

**D2.3 Post-failure semantics**

| Option | Consequences |
|---|---|
| D2.3-a No answer after failure; loss `lambda_F` | Matches the loss formula in the work plan as written; action set stays {N, C, A}. |
| D2.3-b Fallback: issue `delta_0` after failure; loss `lambda_F` + wrong-answer term | Recovers coverage, but effectively adds a fourth path ("C, else N") that the loss formula and comparators must then name explicitly. |

### D3 — The single concrete correction action

| Option | What C does | Consequences |
|---|---|---|
| D3-a Angle recalibration + full re-execution | Recompile each tagged cost rotation with the commanded angle that cancels the estimated error (for the linear model, `(theta - phi_hat) / (1 + epsilon_hat)`), run both candidates again with `n_C` shots, decide from `X_C`. | Matches the program plan's wording ("second execution with an estimated angle recalibration"). Needs both `epsilon_hat` and `phi_hat` (or a stated rule if only one is identified). Costs a full re-execution, so `n_C` competes directly with `n_T0` and `n_S`; under the compiled-angle model the recalibrated angle is itself subject to the same error law, which the correction must account for. |
| D3-b Compiled compensating rotation | Insert a compensating rotation after each tagged gate (for example `RZ(-epsilon_hat theta - phi_hat)`), then re-execute. | Under virtual-Z frames the compensator may be error-free, which makes correction look easier than any physical realization; under the compiled-angle model the compensator is itself mis-rotated. The result depends strongly on D1. |
| Not eligible under the current plan: classical post-hoc correction of the observed gap (no re-execution) | — | Conflicts with Subtask 1.1 ("perform the specified corrected execution"); allowed only through a dated program-plan revision. |

**D3 sub-choices (needed with either option):**

1. **Shot path.** (i) Fixed reserve: `n_S`, `n_T0`, `n_C` fixed in advance; the
   reserve is unused on paths N and A. Simple and auditable, but N and A waste
   `n_C`, which lowers policy value. (ii) Adaptive: on path N the reserve is
   spent on more target shots before issuing. Higher value, but `delta_0` then
   depends on the action, which the theory handles (`q_f` becomes
   path-dependent) but the ledger and comparators must spell out.
2. **Pooling.** Decide from `X_C` only (clean; discards `n_T0` shots) or pool
   `X_T0` with `X_C` (uses all shots, but mixes uncorrected and corrected data
   and so reintroduces part of the bias).

---

## 7. Issues found in the plan while writing this contract (not resolved here)

1. **Frozen rule constants are not on the deployability list.** Subtask 1.3 does
   not list development-locked thresholds and transfer-rule coefficients, yet
   Gates 2–4 require them. §3.1 item 6 proposes adding them explicitly. Owner
   confirmation needed.
2. **Budget path of C is unspecified.** "All shots are charged to one fixed
   budget" does not say whether the re-execution reserve is spent on other
   paths. This changes `q_f`, the always-issue comparator, and Gate 3. Folded
   into D3.
3. **Post-failure semantics is unspecified.** The loss formula does not say
   whether a wrong-answer term can follow a failure. Folded into D2.
4. **Fewer target shots do not always mean higher error.** Under coherent bias
   that flips the decision, the wrong-decision probability of the empirical
   sign can *decrease* when target shots are removed (it tends toward 1/2 rather
   than 1). The value-of-information condition in the theory note therefore
   keeps the allocation cost `q_f - q_0` signed and does not assume it is
   nonnegative.
5. **Decision-ID numbering.** The work plan says D1–D7 are "recorded in program
   plan §8", but §8 lists five different items (work capacity, abstention loss,
   correction action, longitudinal hardware, writing target). D1 (E2 placement)
   is stated in §3.3, and D4–D6 in §3.4.1 and the checklist. The two documents
   should be reconciled by a dated revision note.
6. **Ideal ties.** Neither plan says how units with ideal gap `g = 0` (or
   numerically near 0) are handled. §1.1 proposes exclusion at population
   definition.
7. **M1 versus MT1 "done".** M1's exit evidence is "contracts drafted and
   committed", while MT1's "done when" also requires owner approval of D1–D3.
   This draft reaches M1 but not MT1 completion; the status table should say so.
8. **Comparator loophole (from item 4).** If removing target shots lowers the
   issue error, a policy that always issues at the sensing allocation would beat
   the full-budget always-issue comparator without using any sensor
   information, giving `Delta_V > 0` from the allocation alone (theory note,
   Proposition P2). Options: add "always issue at the sensor allocation" to the
   comparator set, or define always-issue as the best issue-only allocation on
   development data. Owner decision needed before the comparator set is frozen.
