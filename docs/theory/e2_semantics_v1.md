# E2 semantics v1

**Status:** frozen for M2, 2026-11-20. This is a model contract, not a
hardware claim and not an experimental result.

## 1. Primary existence question

The primary E2 model is the **synthetic compiled-angle model**.  For every
tagged cost rotation, the compiler first produces a signed physical angle

```text
a_{k ell t} = s_{ell t} theta_{k ell},  s_{ell t} in {-1, +1},
```

and the model implements

```text
RZ(a_{k ell t}) -> RZ((1 + epsilon) a_{k ell t} + phi).
```

`epsilon` is shared angle-proportional error and `phi` is a shared additive
phase in the minimum Gate-1 model.  Both are simulation parameters.  The
Pauli labels and their signs are recorded exactly.  Virtual Pauli-Z frame
updates are error-free; angles are not shifted by `pi` and are not wrapped
before E2 acts.

This model asks whether retained labels identify a parameter in a fully
specified synthetic experiment.  It does **not** assert that a virtual `RZ` on
superconducting hardware has a pulse, duration, or amplitude error.  No
physical carrier for E2 has been established.  Hardware transfer and
pulse-level interpretation are outside the frozen primary claim.

## 2. Model disposition

| Model | M2 disposition | Implemented tagged rotation | Claim boundary |
|---|---|---|---|
| Compiled angle, sign-flip absorption | **Primary** | `RZ((1+epsilon)s theta + phi)` | Synthetic existence question only. |
| Logical angle | Regression/negative control | Apply `RZ((1+epsilon)theta + phi)` before label absorption. | Matches the predecessor's E2 semantics; labels are blind by construction. Not co-primary. |
| Compiled angle, wrapped-Z absorption | Not adopted | Would scale `wrap(s theta + z pi)`. | Excluded unless a named compiler/backend is first shown to use this physical representation. |
| Physical control | Not modeled | No pulse/control map exists in this repository. | Must not be replaced by a virtual rotation or inferred from the primary synthetic model. |

The predecessor's X-only frames did not cross or alter the tagged cost `RZ`.
They therefore supply a regression control, not the RC construction used here.

## 3. Physical-frame and logical-frame errors

Let `P` be the Pauli correction adjacent to a tagged target rotation and let
`s(P)=+1` when `P` commutes with target `Z`, and `-1` when it anticommutes.
The compiled physical angle is `a=s(P) theta`.  Conjugating the implemented
rotation back into the logical frame gives

```text
P RZ((1+epsilon)s(P)theta + phi) P
    = RZ((1+epsilon)theta + s(P)phi).
```

Thus the logical multiplicative error `epsilon theta` is label invariant,
while the additive phase changes sign.  This identity is proved for the frozen
Pauli construction in `gate1_frame_covariance_draft.md`; it is not evidence of
identifiability by itself.

## 4. Noise placement and RC claim boundary

The tagged `RZ` belongs to an easy round between Clifford `CX` hard rounds.
E2 is therefore an angle- and label-dependent implementation rule for an easy
gate.  It violates the gate-independent easy-noise assumption used by exact
randomized-compiling tailoring theorems.  M2 makes no exact tailoring claim and
no claim that averaging the labels produces a stochastic Pauli channel.

The retained-label experiment and an averaged-channel experiment are distinct:

- Gate 1A conditions on the complete label record and uses the conditional
  likelihood in `conditional_likelihood_v1.md`.
- Marginalizing labels describes a different experiment and cannot establish
  that `epsilon` is identifiable.

Label-dependent SPAM, label-dependent control error, and environmental memory
are not part of the minimum noiseless model.  If introduced later, they must be
explicit nuisance terms; they cannot be silently absorbed into `epsilon` or
`phi`.

## 5. Frozen and still-open quantities

Frozen here are the model placement, sign-flip representation, absence of
wrapped angles, error-free virtual frame labels, and the primary/diagnostic
model roles.  M2 does not freeze the Gate-1 parameter grid, label allocation,
shot count, nuisance dimension, estimator, or pass tolerance.  Those belong to
M3 and must be committed before any Gate-1 computation.
