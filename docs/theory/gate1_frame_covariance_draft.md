# Gate 1 draft: frame bookkeeping for RC labels

**Status: reviewed and corrected for M2 (2026-11-20), on the project owner's instruction.** Section 3 is a proved algebraic identity for the frozen Pauli construction. Section 4 separates proved consequences from open Gate-1 questions. This is not an independent review and contains no Gate-1 result. The numerical example remains a **numerical check**, not a proof.

## 1. Setting

A QAOA cost edge compiles to `CX(c,t) - RZ(theta) on t - CX(c,t)`, where `theta` is the frozen logical cost angle. Randomized compiling (RC) inserts a Pauli label `P_t` around hard cycles; labels that pass through the cost rotation are absorbed into it.

For a rotation `R_G(a) = exp(-i a G / 2)` with generator `G` (here `G = Z`), define `s_t = -1` if `P_t G P_t = -G` (labels X or Y on the target qubit) and `s_t = +1` if they commute (I or Z).

## 2. Three candidate error models

| Model | Implemented operation | Comment |
|---|---|---|
| Logical-angle | Logical `RZ((1+epsilon)*theta + phi)` for every label | Error applied before label absorption. Matches how the predecessor's simulator applied over-rotation to the tagged cost `RZ` while framing only around hard `CX` gates (to be confirmed in Part 1). |
| Compiled-angle, virtual Z | Physical `RZ(a) -> RZ((1+epsilon)*a + phi)` with `a = s_t * theta`; Z labels are error-free frame updates | Error proportional to the commanded physical angle. |
| Compiled-angle, wrapped Z | As above, but Z labels are absorbed as `a = wrap(s_t*theta + z_t*pi)` in `(-pi, pi]` before the error acts | A compiler-representation model; physically meaningful only if the representation is real. |

The compiled-angle, virtual-Z row is frozen as the primary **synthetic** model in `e2_semantics_v1.md`. The logical-angle row is a regression/negative control; wrapped-Z is not adopted; physical control is not modeled. The physical carrier of the error is not established, and no hardware interpretation is claimed.

## 3. Frame-covariance lemma

**Lemma (proved).** If `P` is a Hermitian Pauli and `P G P = sG` for
`s in {-1,+1}`, then for every real `a`,

```text
P R_G(a) P = R_G(s a).
```

In particular, if `s=-1`, then for all `epsilon, phi, theta`:

```text
P R_G((1+epsilon)*(-theta) + phi) P = R_G((1+epsilon)*theta - phi).
```

**Proof.** Since `P=P^dagger=P^{-1}`, conjugation commutes with the matrix exponential:
`P exp(-iaG/2)P = exp[-ia(PGP)/2] = exp(-iasG/2)`. Substituting
`a=-(1+epsilon)theta+phi` proves the displayed special case. QED.

**Consequence under the compiled-angle, virtual-Z model.** The logical action for label `t` is

```text
R_G((1+epsilon)*theta + s_t*phi),   logical phase error  epsilon*theta + s_t*phi.
```

In the physical frame the multiplicative error flips sign with the label; after the label is undone it flips back. The multiplicative term is therefore label invariant in the logical frame, while the additive term flips sign.

## 4. Consequences and open information questions

Let `F_r(u)` denote the label-resolved outcome distribution as a function of the logical rotation angle `u`, where `r` is the unknown ideal response (nuisance). Under the compiled-angle, virtual-Z model, label `t` yields `F_r((1+epsilon)*theta + s_t*phi)`.

1. **I1 (proved for the frozen model).** At `phi = 0` every label yields the same implemented logical circuit for every `epsilon`. The complete conditional outcome distribution is therefore label invariant, so every label-contrast statistic has zero mean and I1 for `epsilon` is exactly zero. At `phi != 0`, a differentiable scalar response has contrast `2*phi*dF_r/du + O(phi^3)`; whether that slope is nonzero is circuit and measurement dependent.
2. **I2 (known response).** If `F_r` is known, the label-pooled distribution depends on `(1+epsilon)*theta`, so I2 for `epsilon` can be positive. This uses ideal values and is diagnostic only.
3. **I3 (open).** The earlier draft's global rescaling-closure premise is rejected: QAOA response functions need not be closed under rescaling their angle arguments. No global non-identifiability conclusion follows from that premise. Admissible profile/efficient information must instead be computed from the frozen multi-context likelihood and nuisance family at M3. At `phi=0`, label contrasts still add no information about `epsilon`; absolute variation across known circuit contexts may or may not leave admissible profile information.

Under the logical-angle model all labels yield `F_r((1+epsilon)*theta + phi)`: labels carry no information about either parameter.

Under the compiled-angle, wrapped-Z model, labels with `z_t = 1` acquire an extra logical term `epsilon * c_t`, `c_t = wrap(theta + pi) - theta` in `{+pi, -pi}`. This term is present at `phi = 0`, is linear in `epsilon`, and does not scale with `|theta|`; I1 for `epsilon` is then positive, but the signal comes from the compiler representation.

**Frozen pre-computation prediction for Gate 1A.** I1 for `epsilon` is zero at `phi=0`. A full Gate-1A failure remains a prediction, not a theorem, until the admissible I3 calculation is frozen and performed. If Gate 1A fails by its frozen criterion, routing proceeds to Gate 1B.

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

## 6. Boundary after M2

- The full Pauli RC construction, correction closure, label table, and noiseless equivalence proof are in `rc_construction_v1.md`.
- The exact conditional statistical model is in `conditional_likelihood_v1.md`.
- I3, the parameter grid, estimator, tolerances, and finite-design rank remain M3/Gate-1 work. No computation has been run here.
- The prior-art boundary remains that RC tailoring does not imply label-based identification; no novelty claim is established by this lemma alone.

## 7. M2 review disposition

- [x] Section 3 sketch replaced by a proof.
- [x] I1 corrected to an exact distributional statement at `phi=0`.
- [x] The unsupported global closure argument rejected; I3 left open for a frozen nuisance model.
- [x] Primary error model and claim boundary frozen.
- [x] RC/Vyas reading notes checked for the limited claim used here; no stronger novelty or tailoring claim added.
