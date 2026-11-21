# Three-action theory v1 (Main Task 1, Subtask 1.5)

> **Owner review (2026-11-21, E008).** T1, C1, C2, L1, the wrong-action form,
> T2, D1, and P2 are **proved and owner-reviewed**; their statements are
> unchanged. Rigorous proofs with the implicit assumptions made explicit are in
> [`A4_A6_rigorous.pdf`](A4_A6_rigorous.pdf). **Example E1 has a gap as stated**:
> L1 needs equal stage-1 laws, including `X_T0`. See E008 §2 for the two valid
> repairs. Example E2's first condition is discharged conditionally by Lemma
> S1′; its second condition is open (E008 §3). Where the status lines below
> differ, `docs/errata/E008_owner_review_A4_A6.md` governs. The text below is
> otherwise unchanged.

**Status: draft, written by Claude 2026-11-20 (commit `8dc782c`); revised
2026-11-20 after owner review of Main Task 1 (direction approved; decisions
D1–D3 and the issue-only comparator recorded in the contract). Not frozen. The
individual proofs still await the owner's line-by-line check.** Every result
carries a proof status:

- `proved (draft, owner review pending)`: a complete proof is written below; it
  still needs owner checking before it is cited as proved.
- `corrected`: the statement or proof was changed in the owner-review revision;
  the change is described where it occurs.
- `sketch`: an outline with named gaps.
- `conditional example`: an instance whose premise is itself unproved.
- `numerical check`: exact enumeration of one or a few examples (§9). It checks
  the algebra of an example; it is never a proof.

Evidence type throughout: **analytic**. No simulation result about QAOA, RC
labels, or P-amp is reported here.

The setting is deliberately sensor-independent (program plan §3.7): no QAOA,
E2, or RC notation appears until the examples in §4.2, which are labeled.
Definitions of units, actions, loss, budget, and comparators are in
[`../contracts/decision_problem_v1.md`](../contracts/decision_problem_v1.md).

Literature keys refer to [`../literature/library.csv`](../literature/library.csv).
Their verification states are unchanged by this note: `chow1970`, `herbei2006`,
`howard1966voi`, `tsybakov2009`, `vandervaart1998` are metadata/abstract-level
checks only; `lecam1973` is inherited (bibliographic). No result below depends
on an unread source for its proof: every proof is self-contained (including the
two divergence inequalities used in T2, proved in §5), and a citation only marks
where a standard form comes from. Where the exact attribution or reference
location could not be checked against a full text, the text says
"attribution/reference location unverified". No new literature entry was added
in the revision.

**Model scope.** The theory is sensor- and model-independent. Where an example
refers to the primary E2 model, that model is the **synthetic compiled-angle
model** of contract §6 D1, and nothing here is a conclusion about virtual-Z
hardware.

---

## Summary of status

| # | Result | Status |
|---|---|---|
| T1 | Three-action risk identity | proved (draft); re-checked in revision |
| C1 | Reduction to the predecessor's Eq. (6) (no correction, `lambda_A = 0`) | proved (draft); equation number checked against the predecessor's compiled paper |
| C2 | Reduction to a Chow-type reject rule (no correction, `lambda_A > 0`) | rule proved (draft); attribution of the exact form to Chow (1970) unverified (full text not accessible) |
| P1 | Pairwise switching conditions (when evidence changes the Bayes action) | proved (draft) |
| L1 | Action-selection blindness lemma | proved (draft) |
| E1 | Direct-phase example of L1 (single sensed angle) | proved (draft) within the direct-phase model; relevance to the QAOA likelihood not established |
| E2 | RC-label example of L1 under the synthetic compiled-angle model | conditional example: frame identity proved at M2; the required nuisance-class indistinguishability remains unproved |
| T2 | Finite-pilot lower bound on wrong-action probability and regret | proved (draft); the two divergence inequalities are now proved in the note; their reference location in `tsybakov2009` unverified |
| D1 | Value-of-information decomposition | corrected (comparator set updated; allocation cost now nonnegative at population level) |
| P2 | Honest collapse | corrected and narrowed: proved (draft) for information-free policies at population level under the issue-only comparator; metadata-only policies and finite-sample selection not covered |
| P3 | Uniform dominance implies a fixed Bayes action | proved (draft) |
| D2 | Policy non-degeneracy (definition) | definition; wording of its relation to Gate 3 corrected; thresholds frozen in Part 3 |

---

## 1. Setting

- `Theta`: set of latent states `vartheta`. Each state determines a correct
  answer `k*(vartheta)` in a finite answer set `K` (here `K = {A, B}`).
- Stage-1 evidence `X` in a measurable space `X-space`, with law `P_vartheta`.
  `X` contains everything observed before the action is chosen (sensor data and
  initial target data). Dominating measure `mu`, density `p_vartheta`.
- Actions `{N, C, A}`. A (possibly randomized) policy `pi` gives, for every
  `x`, probabilities `pi_N(x), pi_C(x), pi_A(x) >= 0` summing to 1. The policy's
  private randomization is independent of everything else given `x`.
- `delta_0(x)` in `K`: the answer issued under N (a fixed function of `x`).
- Stage-2 randomness (corrected execution) occurs only on path C. Given
  `X = x` it produces a failure indicator `F` and, if `F = 0`, an answer
  `delta_C`. Its conditional law may depend on `vartheta` and `x`, and is
  conditionally independent of the policy's private randomization given `x`.
- Loss weights: wrong answer 1, abstention `lambda_A >= 0`, failure
  `lambda_F >= 0`. The results are stated for general weights; the contract's
  primary values are `lambda_A = lambda_F = 1/4`. Post-failure semantics: no
  answer (contract §6 D2). Shot path: fixed reserve, so the stage-1 evidence and
  `delta_0` do not depend on the action (contract §6 D3).

**Action-conditional losses.** For state `vartheta` and evidence `x`:

```text
l_N(vartheta, x) = 1{delta_0(x) != k*(vartheta)}
l_A(vartheta, x) = lambda_A
l_C(vartheta, x) = lambda_F * rho(vartheta, x) + c(vartheta, x),
    rho(vartheta, x) = P_vartheta(F = 1 | X = x),
    c(vartheta, x)   = P_vartheta(F = 0, delta_C != k*(vartheta) | X = x).
```

**Risk.** `R(pi; vartheta) = E_vartheta[L]`, where `L` is the realized loss of
the contract (§4.1).

---

## 2. Three-action risk identity

### Theorem T1 — proved (draft, owner review pending)

For every policy `pi` and state `vartheta`,

```text
R(pi; vartheta) = E_vartheta[ pi_N(X) l_N + pi_C(X) l_C + pi_A(X) l_A ]          (T1a)
                = q(vartheta)
                  + E_vartheta[ pi_C(X) (l_C - l_N) ]
                  + E_vartheta[ pi_A(X) (lambda_A - l_N) ],                        (T1b)
```

where `q(vartheta) = E_vartheta[l_N(vartheta, X)]` is the wrong-answer
probability of issuing `delta_0` at the stage-1 allocation. Equivalently,

```text
R(pi; vartheta) = P(issue and wrong) + lambda_A P(abstain) + lambda_F P(C and fail).   (T1c)
```

Against the always-issue comparator with all `N` shots on the target (error
`q_0(vartheta)`),

```text
R(pi; vartheta) - q_0 = (q - q_0)
                        + E[ pi_C (l_C - l_N) ]
                        + E[ pi_A (lambda_A - l_N) ].                             (T1d)
```

**Proof.** Condition on `X = x`. The policy picks `a` with probability
`pi_a(x)`, independently of stage-2 randomness. If `a = N` the loss is
`l_N(vartheta, x)` (deterministic given `x`). If `a = A` it is `lambda_A`. If
`a = C` the conditional expected loss is
`lambda_F P(F = 1 | x) + 1 * P(F = 0, delta_C != k* | x) = l_C(vartheta, x)`,
using the no-answer semantics. The tower property gives (T1a). Substituting
`pi_N = 1 - pi_C - pi_A` gives (T1b). (T1c) is (T1a) with each term read as the
probability of its event. (T1d) subtracts `q_0`. ∎

**Assumptions used:** the policy is a function of `x` and private
randomization; stage-2 randomness is conditionally independent of that
randomization given `x`; the action set and losses are as stated. No Gaussian,
independence-between-sensor-and-target, or stationarity assumption is used.

**Remark 1 (non-adopted variants).** The owner did not adopt a fallback after
failure or an adaptive reallocation of the reserve. For the record only: with a
fallback, T1 holds with `l_C = lambda_F rho + P(F = 1, delta_0 != k* | x) + c`;
with adaptive reallocation, T1 holds if `l_N(vartheta, x)` is redefined as the
conditional wrong-answer probability of the path-N decision given `x`. Neither
variant is used anywhere else in this note.

### Corollary C1 — reduction to the predecessor's Eq. (6). proved (draft)

Predecessor reference: `bias-probe-visibility` at commit `cd5e576`. In the
compiled paper `paper/main_v4.pdf`, Section 3.3, Eq. (6) is
`d_f > q_f - q_0`, following Eq. (5) `q_f = P(W_f), d_f = P(A_f ∩ W_f),
R_f = q_f - d_f` (checked in the revision by text extraction of the PDF; source
label `eq:worth` in `paper/main_v4.tex`). It is the same condition as display
(4) of `docs/theory/08_prop2.md`; that note's display (6) is the equivalent form
`eta_f > 1 - q_0/q_f`.

Remove C (`pi_C = 0`), set `lambda_A = 0`, and let the policy abstain exactly on
a probe alarm: `pi_A(x) = 1{x in Alarm}`. With the predecessor's notation
`W_f = {delta_0 wrong}` at the reduced target allocation, `A_f = {alarm}`,
`q_f = P(W_f)`, `d_f = P(A_f and W_f)`, (T1b) gives

```text
R = q_f - E[1{Alarm} 1{W_f}] = q_f - d_f,
```

which is the predecessor's `R_f`. Then `R < q_0` iff `d_f > q_f - q_0`, the
predecessor's Eq. (6). ∎ The predecessor's statement that its condition holds
"without independence" is consistent with T1, which also uses no independence
between probe and target data.

### Corollary C2 — Chow-type reject rule. rule proved (draft); attribution unverified

Remove C and let `lambda_A > 0`. Fix a prior `Pi` on `Theta` and write the
posterior wrong-answer probability of the issued decision as

```text
e_N(x) = Pi( delta_0(x) != k* | X = x ).
```

Among all policies with `pi_C = 0`, the Bayes risk `E_Pi[R(pi; vartheta)]` is
minimized by

```text
abstain  iff  e_N(x) > lambda_A        (either action on e_N(x) = lambda_A).
```

If in addition `delta_0(x)` is the posterior-most-likely answer, then
`e_N(x) = 1 - max_k Pi(k* = k | x)`, and the rule becomes "abstain iff the
largest posterior answer probability is below `1 - lambda_A`", which is the
threshold rule commonly attributed to Chow (1970) in secondary literature.
**Attribution unverified:** only the abstract of `chow1970` (which describes "an
optimum rejection rule") has been checked; the full text was not accessible in
the revision (publisher paywall), so it is not confirmed that the paper states
this exact form with these costs. The proof below does not depend on it.

**Proof.** By (T1b) averaged over `Pi` and conditioned on `X`, the Bayes risk is
`E[e_N(X)] + E[pi_A(X)(lambda_A - e_N(X))]`, minimized pointwise by setting
`pi_A(x) = 1` when `lambda_A - e_N(x) < 0` and 0 when it is positive. If
`delta_0` is the posterior mode, `e_N = 1 - max_k Pi(k | x)`. ∎

**Consequence for the loss (two answers).** If `delta_0` is the posterior
mode, `e_N(x) <= 1/2`, so abstention is never Bayes-optimal when
`lambda_A >= 1/2`. In this project action N issues the *fixed empirical*
decision `delta_0`, not the posterior mode, and N cannot issue the other answer;
under coherent bias `e_N(x)` can exceed 1/2, so abstention can still be optimal
for `lambda_A >= 1/2`. Only correction can reverse the issued answer.

---

## 3. Pairwise switching conditions

### Proposition P1 — proved (draft)

Fix a prior `Pi`. Define the posterior action risks

```text
rho_N(x) = e_N(x),   rho_A(x) = lambda_A,
rho_C(x) = lambda_F * phi_F(x) + c_bar(x),
phi_F(x) = E_Pi[rho(vartheta, x) | X = x],   c_bar(x) = E_Pi[c(vartheta, x) | X = x].
```

The Bayes policy chooses an action in `argmin_a rho_a(x)`. Pairwise:

```text
A over N   iff  e_N(x) > lambda_A
C over A   iff  lambda_F phi_F(x) + c_bar(x) < lambda_A
C over N   iff  e_N(x) - c_bar(x) > lambda_F phi_F(x)
```

Necessary conditions that follow directly: C can beat A only if
`lambda_F phi_F(x) < lambda_A`; C can beat N only if `e_N(x) > c_bar(x)`
(correction must lower the posterior wrong-answer probability by more than the
expected failure cost).

**Sensing changes the action.** Let `a_0 in argmin_a E_Pi[rho_a(X)]` be the
best action chosen without looking at `X` (at the same allocation). The
expected value of looking at `X` at a fixed allocation is

```text
VOI_alloc = E_Pi[ rho_{a_0}(X) - min_a rho_a(X) ] >= 0,
```

with equality iff `a_0` is a Bayes action for `Pi`-almost every `x`. So
evidence has positive decision value at a fixed allocation iff, with positive
probability, it moves the posterior across one of the three pairwise
boundaries above away from `a_0`.

**Proof.** The Bayes risk of `pi` is `E[sum_a pi_a(X) rho_a(X)]` by T1 and the
tower property; it is minimized pointwise. The pairwise conditions are
`rho_a < rho_b` written out. `VOI_alloc` is the difference between the Bayes
risk of `a_0` and of the Bayes policy; it is nonnegative and zero iff the
integrand is zero almost surely. ∎

**Deployability note.** `rho_a(x)` uses a prior and the true conditional laws;
the Bayes policy is an oracle reference for theory, not a deployable rule. A
deployable policy (MT5) must replace `rho_a` by frozen, development-fitted
estimates built only from allowed inputs.

---

## 4. Action-selection blindness

### Definitions

Oracle risk and regret, for a state known to the oracle together with `x`:

```text
R*(vartheta)      = E_vartheta[ min_a l_a(vartheta, X) ],
Reg(pi; vartheta) = R(pi; vartheta) - R*(vartheta)
                  = E_vartheta[ sum_a pi_a(X) D_a(vartheta, X) ] >= 0,
D_a(vartheta, x)  = l_a(vartheta, x) - min_b l_b(vartheta, x) >= 0.
```

`A*(vartheta, x) = argmin_a l_a(vartheta, x)` is the set of optimal actions.

### Lemma L1 — proved (draft)

Let `vartheta, vartheta'` satisfy `P_vartheta = P_vartheta'` (identical stage-1
evidence laws; stage-2 laws may differ). Let

```text
Gamma(x) = min_a [ D_a(vartheta, x) + D_a(vartheta', x) ].
```

Then for every policy `pi`,

```text
Reg(pi; vartheta) + Reg(pi; vartheta') >= E_P[ Gamma(X) ],
max{ Reg(pi; vartheta), Reg(pi; vartheta') } >= E_P[ Gamma(X) ] / 2.
```

`Gamma(x) > 0` iff `A*(vartheta, x)` and `A*(vartheta', x)` are disjoint. If the
optimal-action sets are disjoint on a set of positive `P`-probability, no
policy has zero regret at both states.

**Wrong-action form.** If each state has a unique, `x`-independent optimal
action, `a_0 != a_1`, then for every policy
`P_vartheta(pi != a_0) + P_vartheta'(pi != a_1) >= 1`.

**Proof.** Because the two laws are equal and `pi` sees only `x`,
`Reg + Reg' = E_P[ sum_a pi_a(X) (D_a(vartheta, X) + D_a(vartheta', X)) ]`.
For each `x` the weights `pi_a(x)` are a probability vector, so the sum is at
least `Gamma(x)`. `Gamma(x) = 0` iff some action is optimal for both states.
For the wrong-action form, `P_vartheta'(pi != a_1) >= P_vartheta'(pi = a_0) =
P_vartheta(pi = a_0) = 1 - P_vartheta(pi != a_0)`. ∎

This generalizes the predecessor's Lemma 1 (`docs/theory/02_lemma1.md`), which
is the special case of two outputs (certify / not certify) with 0–1 losses.

### 4.2 Examples

**Example E1 — single sensed angle (direct-phase model). proved (draft) within
that model.** Suppose the sensor observes phases only at one effective angle
`a_S`, so its law depends on `(epsilon, phi)` only through
`delta_S = epsilon a_S + phi` (program plan §3.3, direct-phase model). Take two
candidates whose decision depends on the phase difference
`delta_A - delta_B = epsilon (a_A - a_B)` with `a_A != a_B`. The states
`(epsilon, phi)` and `(epsilon', phi + (epsilon - epsilon') a_S)` give the same
sensor law, but different candidate-gap biases `epsilon (a_A - a_B)` and
`epsilon' (a_A - a_B)`. If the margin is such that one bias flips the decision
and the other does not (then C, or A, is optimal at one state and N at the
other), L1 applies. Note that correcting only the sensed phase `delta_S` does
not help: what the decision needs is `epsilon`, which this sensor cannot
separate from `phi`. Whether the QAOA measurement likelihood inherits this
direct-phase structure is a Gate 1A question, not established here.

**Example E2 — RC labels under the synthetic compiled-angle model (primary
model, contract §6 D1). conditional example (nuisance premise unproved).** The
reviewed and corrected
[`gate1_frame_covariance_draft.md`](gate1_frame_covariance_draft.md) proves
that at `phi = 0` every label yields the same outcome law for a fixed circuit,
depending on `(1+epsilon) theta` and the unknown ideal response. *If* Gate 1
also proves that the
admissible information for `epsilon` is zero in the strong sense that there
exist `(epsilon, r)` and `(epsilon', r')` in the frozen nuisance class with
identical label-resolved laws (the draft's closure argument is flagged there as
probably false and is to be replaced), and *if* those two states imply different
optimal actions, then L1 makes RC labels action-blind at `phi = 0`. Both "if"s
are open; this example only shows where L1 would enter. It is not a Gate 1A
result: Gate 1A is decided only by its frozen criterion.

---

## 5. Finite-pilot lower bound

### Theorem T2 — proved (draft); reference location unverified

Let `vartheta_0, vartheta_1` have stage-1 laws `P_0, P_1` (now possibly
different). With `Gamma(x)` as in L1 but computed for this pair:

```text
Reg(pi; vartheta_0) + Reg(pi; vartheta_1) >= integral Gamma(x) min(p_0(x), p_1(x)) mu(dx).   (T2a)
```

If `Gamma(x) >= Gamma_min > 0` for every `x`, then

```text
max_j Reg(pi; vartheta_j) >= (Gamma_min / 2) (1 - TV(P_0, P_1)).                            (T2b)
```

With unique, `x`-independent optimal actions `a_0 != a_1`:

```text
P_0(pi != a_0) + P_1(pi != a_1) >= 1 - TV(P_0, P_1).                                       (T2c)
```

If the pilot consists of `n` independent observations with per-observation laws
`P_{0,i}, P_{1,i}`, then for the product laws

```text
1 - TV >= (1/2) exp( - sum_i KL(P_{0,i} || P_{1,i}) ),                                      (T2d)
1 - TV >= (1/2) prod_i BC(P_{0,i}, P_{1,i})^2,  BC = integral sqrt(p_0 p_1) = 1 - H^2/2.      (T2e)
```

So to make the sum of wrong-action probabilities in (T2c) at most `beta`, the
pilot must satisfy `sum_i KL_i >= log(1 / (2 beta))`; for i.i.d. observations,
`n >= log(1 / (2 beta)) / KL(P_0 || P_1)`.

**Proof.** (T2a): `Reg_0 + Reg_1 = integral sum_a pi_a(x) [D_a^0(x) p_0(x) +
D_a^1(x) p_1(x)] mu(dx) >= integral sum_a pi_a(x) (D_a^0 + D_a^1)(x)
min(p_0, p_1)(x) mu(dx) >= integral Gamma(x) min(p_0, p_1) mu(dx)`.
(T2b): `integral min(p_0, p_1) = 1 - TV`. (T2c): `P_0(pi != a_0) + P_1(pi = a_0)
= integral [(1 - pi_{a_0}) p_0 + pi_{a_0} p_1] >= integral min(p_0, p_1)`, and
`P_1(pi != a_1) >= P_1(pi = a_0)`. For (T2d)–(T2e) two inequalities are
needed; both are proved here so that T2 does not rest on an unread reference.

*Conventions (checked in the revision).* `TV(P, Q) = sup_A |P(A) - Q(A)|
= (1/2) integral |p - q|`, so `integral min(p, q) = 1 - TV` and
`integral max(p, q) = 1 + TV <= 2`. `BC(P, Q) = integral sqrt(p q)`;
with `H^2 = integral (sqrt p - sqrt q)^2` (range `[0, 2]`), `BC = 1 - H^2/2`.
`KL(P || Q) = integral p log(p/q)`, taken as `+infinity` if `P` is not
absolutely continuous with respect to `Q`.

*(i) Le Cam's inequality, `integral min(p, q) >= (1/2) BC^2`.* By
Cauchy–Schwarz,
`BC^2 = (integral sqrt(min) sqrt(max))^2 <= integral min * integral max
<= 2 integral min`.

*(ii) Bretagnolle–Huber, `integral min(p, q) >= (1/2) exp(-KL(P || Q))`.* If
`KL = infinity` there is nothing to prove. Otherwise, by (i) it suffices that
`BC^2 >= exp(-KL)`. On `{p > 0}`, `BC >= integral p sqrt(q/p)`, and by Jensen
(log concave), `log integral p sqrt(q/p) >= integral p log sqrt(q/p) =
-(1/2) KL`, so `BC^2 >= exp(-KL)`.

*Products.* `KL` adds over independent coordinates and `BC` multiplies, which
gives (T2d) from (ii) and (T2e) from (i). Direction: both bound the overlap
`1 - TV` from **below**, which is the direction a lower bound on errors needs;
the constant is `1/2` in both.

*Reference location (unverified).* These are standard (`lecam1973`;
`tsybakov2009`, Chapter 2). Secondary sources cite them as Lemma 2.3 (Le Cam's
inequalities) and Lemma 2.6 (Bretagnolle–Huber) of Tsybakov's book; the book
itself was not consulted (only its metadata is verified), so these locations are
recorded as unverified. ∎

**Scope.** T2 is only as meaningful as the pair. MT3 Subtask 3.3 must construct
pairs that lie inside the frozen model class, imply different optimal actions,
and are physically relevant, and must report loose or irrelevant pairs as failed
constructions. A pilot with label-dependent settings is a product of
non-identical laws, which (T2d)–(T2e) already allow. T2 bounds the probability
of choosing the wrong *action*; it is a different quantity from the QEM
sample-complexity bounds on estimator error (`takagi2022`, `quek2024`, see
`identification_and_information.md`).

---

## 6. Value of information under a fixed budget

### Decomposition D1 — corrected (identity; comparator set updated)

Let `Pi` be the distribution of units (states), bars denote averages over `Pi`,
and write the population risks of the fixed comparators of contract §1.7 as

```text
q_bar_0    issue-only, full-target allocation
q_bar_f    issue-only, sensor allocation (sensor observation ignored)
r_bar_C    always correct, sensor allocation
lambda_A   always abstain
R_fix = min{ min(q_bar_0, q_bar_f), r_bar_C, lambda_A }.
```

For a sensor policy `pi` (whose stage-1 issue error at the sensor allocation is
also `q_bar_f`), T1b gives

```text
Delta_V(pi) = R_fix - R_bar(pi) = G(pi) - K,
G(pi) = E_Pi[ pi_C (l_N - l_C) + pi_A (l_N - lambda_A) ]      (expected action-loss reduction)
K     = q_bar_f - R_fix                                        (allocation cost relative to the best fixed policy)
```

Gate 3 asks whether the lower uncertainty bound of `Delta_V` is positive, i.e.
whether `G(pi) > K` with the required confidence. This is the value-of-
information principle (`howard1966voi`: information is worth acquiring only if
the expected improvement in the decision exceeds its cost) written with the cost
measured in shots.

**Sign of `K` (corrected).** No monotonicity of issue error in shots is
assumed: under coherent bias that flips the decision, removing target shots can
lower the issue error (it moves toward 1/2 instead of toward 1), so
`q_bar_f < q_bar_0` is possible. In the first draft, whose comparator was
full-target always-issue only, `K` could therefore be negative, and part of
`Delta_V` could come from the allocation alone. With the issue-only comparator,
`R_fix <= min(q_bar_0, q_bar_f) <= q_bar_f`, hence

```text
K = q_bar_f - R_fix >= 0       (population level),
```

so at population level `Delta_V(pi) > 0` requires `G(pi) > K >= 0`: a positive
expected action-loss reduction from deviating from N.

### Proposition P2 — honest collapse. corrected and narrowed; proved (draft)

**What changed.** The first draft claimed that every policy taking a single
action has `Delta_V <= 0`, under a comparator condition that fails exactly when
`q_bar_f < q_bar_0`. That condition is now met by construction, and the
statement is strengthened from single-action policies to all information-free
policies, but narrowed to the population level.

**Assumptions.**

- (A1) Comparators as in contract §1.7: issue-only (best of full-target and
  sensor allocation), always correct at the sensor allocation, always abstain.
- (A2) Population level: the comparator is selected by exact risks under the
  same distribution `Pi` on which `Delta_V` is evaluated.
- (A3) Information-free policy: the action probabilities `w_a = P(pi = a)` are
  the same for every unit; they depend neither on the stage-1 evidence `X` nor
  on the unit's metadata (a fixed, possibly randomized, mixture of N, C, A).
  Single-action policies are the special case `w_a = 1`.

**Statement.** Under (A1)–(A3), `Delta_V(pi) <= 0`. Equivalently, under (A1)–(A2),
`Delta_V(pi) > 0` implies that the action of `pi` depends on the unit.

**Proof.** Under (A3) the action is independent of the unit, so by T1a
`R_bar(pi) = w_N q_bar_f + w_C r_bar_C + w_A lambda_A`, where every term is the
risk of always taking that action at the sensor allocation (fixed reserve, so
the allocation does not depend on the action). Each of these is a comparator
risk or, for N, at least `min(q_bar_0, q_bar_f)`; hence each is at least
`R_fix`, and so is their weighted average. Therefore
`Delta_V = R_fix - R_bar(pi) <= 0`. ∎

**What P2 does not cover (open, contract §7).**

1. **Metadata-only policies.** A policy whose action depends on circuit metadata
   but not on any sensor observation violates (A3). It can take different fixed
   actions in different metadata strata and beat the single best fixed
   comparator, giving `Delta_V > 0` without runtime evidence. P2 cannot exclude
   this; the comparator set or the policy class would have to be changed, which
   is an owner decision.
2. **Finite samples.** (A2) fails when comparators are selected from estimated
   development losses. An information-free policy can then show a positive
   holdout `Delta_V` only through development mis-selection; controlling that is
   the job of the Part 3 uncertainty method, not of P2.

**Consequence.** By P2, a policy that uses only one action, or mixes actions
without regard to the unit, cannot pass Gate 3 at population level; in
particular a gain from "issue with fewer target shots" alone is absorbed by the
issue-only comparator and cannot produce a spurious positive `Delta_V`.

### Proposition P3 — uniform dominance gives a fixed Bayes action. proved (draft)

If some action `a` satisfies `rho_a(x) <= rho_b(x)` for every `b` and
`Pi`-almost every `x`, then always taking `a` is a Bayes policy, and
`VOI_alloc = 0`. In particular, if correction benefit `e_N(x) - rho_C(x)` has the
same sign for almost every `x` and abstention is never preferred, the Bayes
policy is fixed. **Proof.** Immediate from P1. ∎ This is the analytic form of the
program plan's failure condition "treatment benefit has the same sign for every
unit" (§3.6).

---

## 7. Policy non-degeneracy

### Definition D2

Let `S` be the frozen set of development strata, `nu_min > 0` a minimum action
frequency, and `tau_tie >= 0` a tie tolerance, all fixed in Part 3 by power
analysis. A deployable policy `pi` is **non-degenerate** if

1. at least two actions `a != b` satisfy `P(pi = a) >= nu_min` and
   `P(pi = b) >= nu_min` over the frozen development distribution, and the same
   holds within every stratum in a prespecified subset of `S` (or overall, if
   Part 3 so freezes); and
2. the action variation is not produced by ties: the probability that the
   policy's decision statistic falls within `tau_tie` of an action boundary is
   below a frozen level, and re-running the policy with the opposite tie rule
   changes the action frequencies by less than a frozen amount.

**Honest collapse** is the outcome in which condition 1 fails; the work plan
requires reporting it as a result rather than tuning thresholds.

**Relation to Gate 3 (wording corrected).** P2 shows that a positive population
`Delta_V` requires the action to depend on the unit, hence at least two actions
with positive probability. It does not show that each must reach `nu_min`: a
policy that uses a second action very rarely could have a small positive
`Delta_V` while failing condition 1. Gate 4's frequency requirement is
therefore an additional requirement, not a consequence of Gate 3, and
non-degeneracy in the sense of D2 is neither necessary nor sufficient for a
positive `Delta_V`. (The first draft said "necessary"; that was too strong.)

---

## 8. Open items for owner review

1. Check every proof marked `proved (draft)` or `corrected`.
2. Attribution/reference location unverified: the exact C2 form in the full
   text of `chow1970`; the lemma numbers of Le Cam's inequality and
   Bretagnolle–Huber in `tsybakov2009`. Neither affects a proof here.
3. Rule on the metadata-only policy gap left by P2 (§6; contract §7).
4. Example E2 remains conditional on Gate 1 establishing nuisance-class
   indistinguishability or an equivalent zero-admissible-I3 result; M2 proves
   only the frame identity and zero I1 at `phi = 0`.

Resolved in the owner-review revision: the comparator loophole (P2, D1); the
choice of `lambda_A`, `lambda_F`, post-failure semantics and shot path
(contract §6).

---

## 9. Numerical check (exact enumeration of toy examples; not a proof)

Python 3.13 in Claude's workspace, exact rational arithmetic for checks 1–2.

1. **T1 on a toy model.** Three evidence values with probabilities
   `(1/2, 3/10, 1/5)`, true answer A, `delta_0 = (A, B, B)`, stage-2
   `(P(fail), P(correct answer | no fail)) = ((1/10, 9/10), (1/5, 7/10),
   (1/2, 1/2))`, policy rows `(1,0,0), (1/3,1/3,1/3), (0,1/2,1/2)` over
   `(N, C, A)`, `lambda_A = 1/4`, `lambda_F = 1/2`. Direct enumeration of the
   loss: `117/500`; identity (T1b): `117/500`.
2. **C1 on the same model.** No C, `lambda_A = 0`, alarm on the second evidence
   value only: `R_f = 1/5 = q_f - d_f`.
3. **T2c–T2e.** `P_0 = Bernoulli(0.50)`, `P_1 = Bernoulli(0.55)`, `n` i.i.d.
   shots. The minimum over policies of `P_0(wrong) + P_1(wrong)` equals
   `1 - TV`:

| `n` | `1 - TV` | `(1/2) exp(-n KL)` | `(1/2) BC^(2n)` |
|---:|---:|---:|---:|
| 10 | 0.872549 | 0.475495 | 0.487609 |
| 100 | 0.615528 | 0.302503 | 0.389033 |
| 1000 | 0.113228 | 0.003285 | 0.040657 |

Both lower bounds hold in all three cases.

4. **P2 loophole and its repair (arithmetic on invented risks, added in the
   revision).** Take `q_bar_0 = 0.30`, `q_bar_f = 0.22` (fewer target shots give
   a lower issue error), `r_bar_C = 0.27`, `lambda_A = 1/4`. With the
   first-draft comparator set `{q_bar_0, r_bar_C, lambda_A}`, `R_fix = 1/4`, and
   the information-free policy "always N at the sensor allocation" has
   `Delta_V = 3/100 > 0` (spurious). With the issue-only comparator,
   `R_fix = 11/50` and the same policy has `Delta_V = 0`; the information-free
   mixture `(w_N, w_C, w_A) = (1/2, 3/10, 1/5)` has `R_bar = 241/1000` and
   `Delta_V = -21/1000`. (Exact rational arithmetic.)

Script for checks 1–3:

```python
import math
from fractions import Fraction as F
lamA, lamF = F(1,4), F(1,2)
P_X = {0:F(1,2), 1:F(3,10), 2:F(1,5)}; d0 = {0:'A', 1:'B', 2:'B'}; truth = 'A'
st2 = {0:(F(1,10),F(9,10)), 1:(F(1,5),F(7,10)), 2:(F(1,2),F(1,2))}
pi = {0:{'N':F(1),'C':F(0),'A':F(0)}, 1:{'N':F(1,3),'C':F(1,3),'A':F(1,3)},
      2:{'N':F(0),'C':F(1,2),'A':F(1,2)}}
R_direct = F(0)
for x, px in P_X.items():
    for a, pa in pi[x].items():
        if a == 'N': R_direct += px*pa*(1 if d0[x] != truth else 0)
        if a == 'A': R_direct += px*pa*lamA
        if a == 'C':
            pf, pok = st2[x]; R_direct += px*pa*(pf*lamF + (1-pf)*(1-pok))
lN = {x: F(1 if d0[x] != truth else 0) for x in P_X}
lC = {x: st2[x][0]*lamF + (1-st2[x][0])*(1-st2[x][1]) for x in P_X}
qf = sum(P_X[x]*lN[x] for x in P_X)
R_id = qf + sum(P_X[x]*pi[x]['C']*(lC[x]-lN[x]) for x in P_X) \
          + sum(P_X[x]*pi[x]['A']*(lamA-lN[x]) for x in P_X)
print(R_direct, R_id)                                   # 117/500 117/500
alarm = {0:0, 1:1, 2:0}
print(sum(P_X[x]*(1-alarm[x])*lN[x] for x in P_X),
      qf - sum(P_X[x]*alarm[x]*lN[x] for x in P_X))     # 1/5 1/5
def binom(n, p): return [math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]
p0, p1 = 0.50, 0.55
kl = p0*math.log(p0/p1) + (1-p0)*math.log((1-p0)/(1-p1))
bc = math.sqrt(p0*p1) + math.sqrt((1-p0)*(1-p1))
for n in [10, 100, 1000]:
    a, b = binom(n, p0), binom(n, p1)
    print(n, sum(min(x, y) for x, y in zip(a, b)), 0.5*math.exp(-n*kl), 0.5*bc**(2*n))
```
