# Gate 1 draft: frame bookkeeping for RC labels

**Status: unreviewed draft (2026-11-20). Not a proof, not a result, not frozen.** Written by Claude as input to the Part 1 mathematical specification. Every statement below must be checked, proved, corrected, or rejected by the project owner before it is used. The only numerical evidence is one single-qubit **numerical check** (noiseless, exact state-vector arithmetic) of one example; it is not a proof of the general statements.

## 1. Setting

A QAOA cost edge compiles to `CX(c,t) - RZ(theta) on t - CX(c,t)`, where `theta` is the frozen logical cost angle. Randomized compiling (RC) inserts a Pauli label `P_t` around hard cycles; labels that pass through the cost rotation are absorbed into it.

For a rotation `R_G(a) = exp(-i a G / 2)` with generator `G` (here `G = Z`), define `s_t = -1` if `P_t G P_t = -G` (labels X or Y on the target qubit) and `s_t = +1` if they commute (I or Z).

## 2. Three candidate error models (one must be frozen in Part 1)

| Model | Implemented operation | Comment |
|---|---|---|
| Logical-angle | Logical `RZ((1+epsilon)*theta + phi)` for every label | Error applied before label absorption. Matches how the predecessor's simulator applied over-rotation to the tagged cost `RZ` while framing only around hard `CX` gates (to be confirmed in Part 1). |
| Compiled-angle, virtual Z | Physical `RZ(a) -> RZ((1+epsilon)*a + phi)` with `a = s_t * theta`; Z labels are error-free frame updates | Error proportional to the commanded physical angle. |
| Compiled-angle, wrapped Z | As above, but Z labels are absorbed as `a = wrap(s_t*theta + z_t*pi)` in `(-pi, pi]` before the error acts | A compiler-representation model; physically meaningful only if the representation is real. |

The physical carrier of the error (pulse amplitude, native fractional two-qubit gate, or something else) is not established; on hardware where `RZ` is virtual there may be no `RZ` error at all. This must be checked against documentation, not assumed.

## 3. Draft lemma (frame covariance)

**Claim.** If `P G P = -G`, then for all `epsilon, phi, theta`:

```text
P R_G((1+epsilon)*(-theta) + phi) P = R_G((1+epsilon)*theta - phi).
```

**Sketch.** `P exp(-i a G/2) P = exp(-i a (P G P)/2) = exp(+i a G/2) = R_G(-a)`, with `a = -(1+epsilon)*theta + phi`.

**Consequence under the compiled-angle, virtual-Z model.** The logical action for label `t` is

```text
R_G((1+epsilon)*theta + s_t*phi),   logical phase error  epsilon*theta + s_t*phi.
```

In the physical frame the multiplicative error flips sign with the label; after the label is undone it flips back. The multiplicative term is therefore label invariant in the logical frame, while the additive term flips sign.

## 4. Draft consequences for the three information quantities

Let `F_r(u)` denote the label-resolved outcome distribution as a function of the logical rotation angle `u`, where `r` is the unknown ideal response (nuisance). Under the compiled-angle, virtual-Z model, label `t` yields `F_r((1+epsilon)*theta + s_t*phi)`.

1. **I1 (label contrast).** At `phi = 0` every label yields the same distribution, so every label-contrast statistic has mean zero for **every** `epsilon`: I1 for `epsilon` is identically zero there. At `phi != 0`, a contrast mean is approximately `2*phi*dF_r/du`, so labels carry first-order information about `phi` and information about `epsilon` only at order `phi`, and only where `dF_r/du != 0`.
2. **I2 (known response).** If `F_r` is known, the label-pooled distribution depends on `(1+epsilon)*theta`, so I2 for `epsilon` can be positive. This uses ideal values and is diagnostic only.
3. **I3 (nuisance `r`).** Suppose the nuisance class is closed under rescaling of the angle argument: for any `epsilon'` there is `r'` with `F_{r'}(x) = F_r(x * (1+epsilon)/(1+epsilon'))`. Then `(epsilon, phi, r)` and `(epsilon', phi*(1+epsilon')/(1+epsilon), r')` give identical label-resolved distributions at every frozen angle simultaneously, so `epsilon` is not identified and its efficient information is zero. Whether the QAOA response class satisfies this closure condition at the frozen angle set is an open question for Part 1; if it does not, I3 may be positive and must be computed.

   **Caution added 2026-11-20 (review).** The closure condition is probably false as a global statement: the expectation of a circuit is a trigonometric polynomial of degree 1 in each single rotation angle (the parameter-shift structure), and rescaling the angle argument changes the frequency, which leaves that class. The non-identifiability argument should therefore not rest on closure. A more plausible route is a local equation count: at the operating point, the label patterns sample the multivariate response at most at `2^m` sign patterns of `phi` around one point `u`, while the unknown response has many more free coefficients, and at `phi = 0` all patterns coincide. Part 1 must replace item 3 with an argument of this kind or show positive I3.

Under the logical-angle model all labels yield `F_r((1+epsilon)*theta + phi)`: labels carry no information about either parameter.

Under the compiled-angle, wrapped-Z model, labels with `z_t = 1` acquire an extra logical term `epsilon * c_t`, `c_t = wrap(theta + pi) - theta` in `{+pi, -pi}`. This term is present at `phi = 0`, is linear in `epsilon`, and does not scale with `|theta|`; I1 for `epsilon` is then positive, but the signal comes from the compiler representation.

**Draft prediction for Gate 1A.** If the compiled-angle, virtual-Z model is frozen as primary, Gate 1A fails (zero admissible information for `epsilon` at `phi = 0`), and the plan proceeds to the frozen Gate 1B.

**Remark on direct-phase rank counting.** Treating the physical angles `+theta` and `-theta` as two distinct effective angles in a design matrix `[a_i, 1]` gives full rank, but that count is made in the wrong frame. In the logical frame the design matrix has rows `(theta, s_t)`; the `epsilon` column is constant across labels and is absorbed by the nuisance `r`.

## 5. Numerical check (single qubit, one example; not a proof)

Initial state `|+>`, `theta = 0.7`, `epsilon = 0.05`, `phi = 0.03`; error law `RZ(a) -> RZ((1+epsilon)*a + phi)`; reported `<X>`:

| Case | `<X>` |
|---|---|
| Ideal `RZ(theta)` | 0.76484 |
| No label, compiled-angle model | 0.72138 |
| X label (physical angle `-theta`), compiled-angle model | 0.76161 |
| Logical `RZ((1+epsilon)*theta + phi)` | 0.72138 (equals "no label") |
| Logical `RZ((1+epsilon)*theta - phi)` | 0.76161 (equals "X label") |
| Z absorbed as `theta + pi` | 0.60416 |
| Z absorbed as `theta - pi` (wrapped) | 0.82084 |

The matching pairs agree with the claim of Section 3 for this example; the last two rows show the extra `+/- epsilon*pi` term of the wrapped-Z model. Script used:

```python
import numpy as np
def rz(a): return np.diag([np.exp(-1j*a/2), np.exp(1j*a/2)])
X = np.array([[0, 1], [1, 0]]); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1, -1])
plus = np.array([1, 1]) / np.sqrt(2)
def ex(U):
    v = U @ plus
    return np.real(v.conj() @ X @ v), np.real(v.conj() @ Y @ v)
th, eps, phi = 0.7, 0.05, 0.03
err = lambda a: rz((1 + eps) * a + phi)
print(ex(rz(th)), ex(err(th)), ex(X @ err(-th) @ X),
      ex(rz((1 + eps) * th + phi)), ex(rz((1 + eps) * th - phi)),
      ex(Z @ err(th + np.pi)), ex(Z @ err(th - np.pi)))
```

## 6. Not shown here (Part 1 work)

- A general proof for the full two- and three-qubit RC construction, including labels that do not commute or anticommute with the cost rotation in a single step.
- The exact label-absorption rule of the chosen compiler and whether Z labels are virtual.
- Whether the QAOA response class satisfies the closure condition in Section 4, item 3.
- Whether this observation is already published (Vyas 2026 and the RC literature must be read in full first).

## 7. Review checklist for the project owner

- [ ] Section 3 sketch checked or replaced by a proof.
- [ ] Section 4 items 1--3 checked; closure condition settled for the frozen design.
- [ ] Primary error model chosen and frozen.
- [ ] Prior-art check completed.
