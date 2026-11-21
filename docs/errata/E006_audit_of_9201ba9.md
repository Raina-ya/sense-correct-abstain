# Erratum E006 — Audit of the erratum commit `9201ba9` (2026-11-21)

**Append-only.** E001–E005 and every file hashed in
`results/errata/errata_manifest.sha256` remain byte-identical. Where this
erratum narrows or corrects an earlier erratum, **this erratum governs**. No
frozen verdict changes.

| Section | Subject | Effect on earlier text |
|---|---|---|
| §2 | Lemma S1 (E001 §2) | **Narrowed**: global non-identification holds only for the response-free nuisance classes; for a general class containing a free label-independent distribution, only local non-identification is guaranteed. The FAIL derivation needs only the local statement. |
| §3 | `B_hat` statement (E003 §6) | **Corrected**: `B(epsilon, phi)/2` is an exact, global, instance-uniform bound on the E2-induced shift of the expected gap. E003's "not a bound beyond first order" understated it. `B_hat` (estimates) still has no proven guarantee. |
| §4 | Authoritative Gate 2 wording for MT7 | Replaces the narrowed wording in E003 §8 and `project_status.md`. |
| §5 | Finite-separation pairs at budget (E001 §4) | Confirmed; no change. |
| §6 | Errata-manifest policy | `docs/results/project_status.md` is a living document; its `9201ba9` hash is verified against git history, not the working tree. |
| §7 | Future locks (E005 §5) | Implemented as a new template and checker; old locks unchanged. |

---

## 1. Distinctions used below

For a parameter `epsilon` at a true point `(epsilon_0, eta_0)` in a model
`{P_{epsilon,eta}}`:

- **Zero local efficient information** means the `epsilon` score lies in the
  closed span of the nuisance tangent set. This is a first-order statement.
  It does not by itself imply non-identification: a parameter can be
  identified at higher order with zero Fisher information.
- **Local non-identification** means that every neighborhood of `epsilon_0`
  contains `epsilon' != epsilon_0` with some `eta'` such that
  `P_{epsilon',eta'} = P_{epsilon_0,eta_0}` exactly.
- **Global non-identification** means that for every `epsilon'` in the
  parameter set there is some `eta'` with
  `P_{epsilon',eta'} = P_{epsilon_0,eta_0}`.

Non-identification claims below are established by **explicit constructions
of observationally equivalent parameter points**, not from Fisher information.

## 2. Lemma S1, restated and proved

### Setting and parameterization

- Frozen Gate 1A data: for each candidate circuit `c` (tagged logical angles
  `theta_{c,ell}`, `ell = 1..L_c`) and each label pattern `t` with sign vector
  `s(t)`, i.i.d. draws from an outcome law `P_{c,t}` on `2^n` bitstrings.
  Labels are drawn uniformly and recorded.
- Primary synthetic model: logical tagged angles `u_{c,ell}(t) =
  (1+epsilon) theta_{c,ell} + s_ell(t) phi` (frame covariance, proved at M2).
- **At `phi = 0`, `u_c(t) = (1+epsilon) theta_c` for every `t`, so
  `P_{c,t} = P_c` is label invariant** (M2; verified to `0` in the frozen
  run).

Three nuisance parameterizations are considered, because the frozen
specification (§5.3) is ambiguous (E001 §3):

| Name | Law | Nuisance |
|---|---|---|
| **N-free** (unknown response) | `P_{c,t} = R_c(u_c(t))` | for each `c`, an arbitrary map `R_c` from angle vectors to strictly positive distributions; the exact quantum kernel is one member |
| **N-loc** (literal first-order) | `P_{c,t} = q_c + sum_ell (epsilon theta_{c,ell} + s_ell(t) phi) D_{c,ell}` | `q_c` in the open simplex; `D_{c,ell}` sum-zero vectors, free; positivity of `P_{c,t}` required |
| **N-q** (minimal) | as N-loc, but with `D_{c,ell}` fixed or known | only `q_c` unknown (open simplex) |

N-q is not a reading of the frozen class. It is included to show the weakest
assumption under which the FAIL derivation still goes through.

### Lemma S1′ (status: proved, draft; owner review pending)

At every point with `phi = 0`:

1. **Local non-identification under N-q** (hence also under N-loc).
   *Construction.* Let `v_c = sum_ell theta_{c,ell} D_{c,ell}` (sum-zero) and
   `delta = min_c min_b q_c(b) / max(||v_c||_inf, tiny)`. For any `epsilon'`
   with `|epsilon' - epsilon_0| < delta`, set `q'_c = q_c + (epsilon_0 -
   epsilon') v_c` and keep `D`. Then `q'_c` lies in the open simplex, and for
   every `t`:
   `q'_c + epsilon' v_c = q_c + epsilon_0 v_c`.
   So `P'_{c,t} = P_{c,t}` for all `c, t`. ∎
2. **Global non-identification under N-loc.**
   *Construction.* For `epsilon' != 0`, set `D'_{c,ell} = (epsilon_0 /
   epsilon') D_{c,ell}` and `q'_c = q_c`. Then `epsilon' v'_c = epsilon_0 v_c`,
   so the laws coincide, and positivity is unchanged because the laws are
   identical. For `epsilon' = 0`, set `q'_c = P_c` (strictly positive) and
   `D' = 0`. ∎
3. **Global non-identification under N-free.**
   *Construction.* At `phi = 0` the data reveal `R_c` only at the single point
   `(1+epsilon_0) theta_c`. For any `epsilon'` with `1 + epsilon' != 0`,
   define `R'_c` to equal `R_c((1+epsilon_0) theta_c)` at
   `(1+epsilon') theta_c`, and to be arbitrary (strictly positive) elsewhere.
   Then `P'_{c,t} = P_{c,t}`. ∎ The earlier draft's global rescaling-closure
   premise (rejected at M2) is not used; only one point per candidate is ever
   observed at `phi = 0`.
4. **Zero local efficient information** under N-q, N-loc, and N-free,
   assuming `P` is differentiable in `epsilon` and strictly positive (true for
   the frozen kernel). At `phi = 0` the `epsilon` score of candidate `c` is the
   same for every label and sums to zero over outcomes, so it lies in the
   tangent direction of the free label-independent `q_c` (or `R_c`), and its
   efficient projection vanishes. Numerical check:
   `results/errata/gate1a_efficient_information.json`, at most `6.8e-21`/shot.

**Narrowing of E001 §2.** E001 asserted non-identification "under any
nuisance class that contains ... an unknown label-independent outcome
distribution". That is guaranteed only **locally** (item 1). Global
non-identification needs the response directions or the response itself to
be free (items 2 and 3). Under a class with known response directions (N-q),
positivity can bound the equivalence set.

**What Lemma S1′ does not claim.** Under a **structured** class (for example
the exact quantum kernel with the circuit known and visibility fixed at 1),
`epsilon` can be identified from absolute levels (oracle I2 is
`0.24–0.62`/shot at `phi = 0`). No structured deployable class was frozen,
and none is claimed blind.

### How the frozen rule yields Gate 1A FAIL

1. The frozen estimator is the profile MLE under the I3 class (§7). It is
   applied to **exact probabilities** at every grid point and must reach "the
   same identified solution" from all starts, within `1e-8`.
2. At each of the nine grid points with `phi = 0`, item 1 gives an open
   interval of `epsilon'` values whose laws equal the truth exactly. So the
   profile likelihood attains its maximum on that interval, and the maximizer
   is not unique. (This uses N-q only; N-loc and N-free are larger classes.)
3. Specification §7: "a flat profile, nonunique solution ... is a failure".
   Specification §9: pass requires recovery "at every required grid point".
4. Hence Gate 1A fails under every reading of the frozen class. This derivation
   uses no Fisher-information or regularity argument. It needs only that the
   frozen class contains a free label-independent per-candidate distribution
   in the open simplex, which is how §5.3 describes it ("each target context's
   ideal outcome distribution ... unknown, subject only to normalization,
   positivity").

## 3. The gap-shift bound (corrects E003 §6)

### Lemma B (status: proved, draft; owner review pending)

**Setting.** Candidate `j in {A, B}` is the frozen `p = 1` circuit with
tagged angles `x_{j,1..m_j}`, each entering through its own `RZ(x_{j,i})`.
The normalized cut score is `s(b) in [0, 1]`. The expected score is
`E_j(x_j) = sum_b s(b) |<b|U_j(x_j)|+^n>|^2`, and the expected gap is
`g(x) = E_A(x_A) - E_B(x_B)`.

Under the primary model (target circuits carry no labels), each tagged angle
`theta_{j,i} > 0` becomes `theta_{j,i} + delta_{j,i}` with
`delta_{j,i} = epsilon theta_{j,i} + phi` **exactly**.

**Claim.** For all real `epsilon`, `phi`:

```text
|g(theta + delta) - g(theta)|  <=  (1/2) * ||delta||_1
                               <=  (1/2) * ( |epsilon| * A + |phi| * M )  =  B(epsilon, phi) / 2,
```

with `A = sum_{j,i} |theta_{j,i}|` and `M = m_A + m_B`.

*Proof.*

1. **Trigonometric degree.** Fix all arguments but `x = x_{j,i}`. Then
   `U_j = V_2 RZ(x) V_1` with `RZ(x) = cos(x/2) I - i sin(x/2) Z`, so each
   amplitude is `cos(x/2) alpha_b - i sin(x/2) beta_b`. Its squared modulus is
   a combination of `cos^2(x/2)`, `sin^2(x/2)`, and `sin(x/2)cos(x/2)`, hence
   `E_j = a + b cos x + c sin x`.
2. **Uniform derivative bound.** Because `0 <= E_j <= 1` for all `x`, the
   oscillation `2 sqrt(b^2 + c^2)` is at most 1. So
   `|dE_j/dx| <= sqrt(b^2 + c^2) <= 1/2` at **every** point, not only at
   `theta`.
3. **Exact integral identity.** The two candidates have disjoint arguments,
   so `||grad g(y)||_inf <= 1/2` for all `y`. By the fundamental theorem of
   calculus along `y(t) = theta + t delta`:
   `|g(theta + delta) - g(theta)| = |int_0^1 grad g(y(t)) . delta dt| <=
   (1/2) ||delta||_1`.
4. Finally, `|delta_{j,i}| <= |epsilon| theta_{j,i} + |phi|`. ∎

**Properties.**

- Norm pairing: `l_inf` on the gradient, `l_1` on the perturbation.
- The constant `1/2` is uniform: independent of the instance, the angles,
  `epsilon`, `phi`, and the perturbation size. It depends only on the score
  range `[0, 1]`.
- There is no remainder term; the bound is exact and **global**. It is not a
  first-order approximation.

**Numerical check** (`tools/audit_gap_shift_bound.py` →
`results/errata/gap_shift_bound_check.json`). This deterministically evaluates
the frozen exact-probability functions; it is not a proof. Over every nonzero
error unit, the largest ratio of the shift to `B/2` is 0.431 (Gate 2, 6160
units) and 0.213 (Gate 3/4, 4752 units). The bound holds everywhere, with at
least about 2.3× slack in these populations.

**Correction to E003 §6.** E003 called `B_hat` "twice a first-order bound" and
"not a bound beyond first order". The second phrase is wrong: `B(epsilon,
phi)/2` bounds the expected-gap shift globally, so `B` is twice a global bound
at the true parameters.

**Still unproved about the frozen rule:**

1. `B_hat = B(epsilon_hat, phi_hat)` uses estimates. No coverage statement
   `P(B(epsilon, phi) <= B_hat) >= 1 - alpha` has been proved for the frozen
   P-amp estimator.
2. The rule compares the **sampled** initial gap `|g0_hat|` with `B_hat`.
   Lemma B concerns the **expected** gap. No result links the comparison to
   the probability of a decision flip, or to correction benefit, under shot
   noise.
3. Lemma B says nothing about the residual error after recalibration with
   estimated parameters, or about tightness (the observed slack is at least
   about 2.3×).
4. It covers only the noiseless synthetic E2 model, with errors on tagged
   rotations only.

Therefore `B_hat` must be described as a **heuristic alarm threshold built
from a provable population bound**, not as a guarantee about the rule.

## 4. Authoritative Gate 2 wording for MT7

Owner-fixed wording, with one edit: "preregistered" is replaced by
"prespecified, internally locked". The project reserves "preregistered" for
records with an independent timestamp (program plan status line), and the
Gate 2 lock is an internal Git and SHA-256 lock (D6, E005).

> Gate 2 formally passed its prespecified, internally locked rule, but the
> diagnostic did not demonstrate useful selective prediction of which units
> benefit from correction. Its precision was 0.093 versus a base rate of
> 0.077, and much of the apparent gain came from excluding large-gap units.
> Therefore Gate 2 is retained as a formal PASS but not interpreted as
> evidence of operationally useful benefit selection.

Chinese summary at the same claim level:

> Gate 2 形式上通過了事先指定、內部鎖定的判準；但診斷結果顯示，它沒有展現出「選擇性地預測哪些單位會從校正中獲益」的實用能力：precision 為 0.093，base rate 為 0.077，表面上的增益有相當部分來自排除大 gap 單位。因此 Gate 2 保留為形式上的 PASS，但不解讀為具有實用價值的獲益篩選證據。

The diagnostics behind this wording are exploratory and post hoc (E003 §3).
The wording neither revises nor supports the frozen verdict.

## 5. Finite-separation pairs at budget (E001 §4): confirmed

- **Data model.** The sensing experiment uses `n_S = 2430` i.i.d. draws of
  the joint (label, bitstring) variable under uniform labels (M3 lock §3), so
  the law of the sample is the `n`-fold product.
- **Tensorization used.**
  - The Bhattacharyya coefficient multiplies: `BC_n = BC_1^n`. The stored
    `hellinger_squared = 0.5 * sum (sqrt a - sqrt b)^2` equals `1 - BC_1`.
  - KL adds: `KL_n = n KL_1`.
  - TV is **not** multiplied.
- **Bounds.**
  - Upper: `TV_n <= sqrt(1 - BC_n^2)`.
  - Lower: `1 - TV_n >= max(BC_n^2 / 2, exp(-KL_n) / 2)` (Le Cam;
    Bretagnolle–Huber, both proved in the theory note §5).
  - Equal-prior two-point error: `(1 - TV_n)/2`.
- **Reported values** (0.185–0.232) follow, and are lower bounds valid for any
  procedure, because they use the oracle law.

## 6. Errata-manifest policy correction

`9201ba9` hashed `docs/results/project_status.md` in
`results/errata/errata_manifest.sha256`. That contradicts E005 §5 item 5
("status must not live in hashed files").

**Correction.** `project_status.md` is designated a **living document**.
`tools/check_errata_artifacts.py` verifies its v1 hash against the blob
committed in `9201ba9` (`git show 9201ba9:docs/results/project_status.md`)
instead of the working tree. All other v1 entries are still verified against
the working tree. The v1 manifest itself is unchanged.

New errata files are hashed in `results/errata/errata_manifest_v2.sha256`.
`requirements.txt` stays unchanged (it is v1-hashed). Its comment already
records that the Python version and platform are unknown; the full
environment record is in `docs/reproducibility.md`.

## 7. Future locks (E005 §5 implemented)

`docs/protocols/lock_template_v2.md` and `tools/check_protocol_lock.py`
define and enforce a lock record. A lock must cover:

- design files;
- every execution-code file, with local imports checked by static scan;
- the environment (Python version, platform, package versions), checked
  against the running interpreter;
- seeds;
- the exact command;
- outputs that must not pre-exist; and
- post-run artifact hashes.

The M3, Gate 2, and Gate 3/4 locks are not modified and are not retroactively
upgraded.
