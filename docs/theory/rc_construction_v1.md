# Randomized-compiling construction v1

**Status:** frozen semantic construction for M2, 2026-11-20. Logical
equivalence is analytic and has a deterministic matrix check. No noise
tailoring or parameter-identification result is claimed.

## 1. Cycle convention

Circuit products are written in matrix order: the rightmost operation acts
first.  A bare circuit is decomposed into easy rounds `C_j` followed by hard
rounds `G_j`,

```text
U = G_K C_K ... G_2 C_2 G_1 C_1.
```

The frozen sets are:

- easy gates `C`: tensor products and products of single-qubit Clifford gates,
  virtual Pauli frames, the tagged target `RZ`, and the other single-qubit QAOA
  gates;
- hard gates `G`: `CX` gates in the frozen `RZZ` decomposition;
- twirling set `T`: the full two-qubit Pauli set
  `{P_c tensor P_t : P_c,P_t in {I,X,Y,Z}}`, sampled modulo phase;
- correction for label `T_j` around hard gate `G_j`:
  `T_j^c = G_j T_j^dagger G_j^dagger`.

Because `CX` is Clifford, `T_j^c` is again a two-qubit Pauli.  Correction
closure therefore holds in the easy-gate group.  This closure is an algebraic
statement; it does not repair the gate-dependent easy-noise mismatch described
in `e2_semantics_v1.md`.

For the general cycle sequence, set the incoming boundary correction to the
identity and the final twirl to the identity.  The dressed easy round is

```text
C_tilde_j = T_j C_j T_{j-1}^c.
```

Adjacent factors cancel because `T_{j-1}^c G_{j-1} T_{j-1}=G_{j-1}`.  This
proves noiseless logical equivalence for every Cartesian product of allowed
labels, not only for one sampled pattern.

## 2. Tagged cost-block specialization

One logical cost edge is

```text
B(theta) = CX(c,t) RZ_t(theta) CX(c,t).
```

Treat the two `CX` gates as consecutive hard rounds, draw one label
`T=P_c tensor P_t` between them, and set the exterior boundary twirls to the
identity.  Let

```text
T^c = CX T CX,
s(T) = +1 if [T^c, I tensor Z] = 0, otherwise -1.
```

The second dressed easy round can be compiled as

```text
RZ_t(theta) T^c = T^c RZ_t(s(T) theta).
```

The complete dressed block is therefore

```text
B_T(theta) = CX T^c RZ_t(s(T) theta) CX T.
```

In the noiseless case, `B_T(theta)=B(theta)` up to global phase for every
allowed `T`.  Under primary E2, only the signed tagged rotation is replaced by
`RZ_t((1+epsilon)s(T)theta + phi)`.

## 3. Label-to-dressed-gate table

Phases on Pauli products are discarded because they are global.  The control
label changes `T^c` but the signed tagged angle depends only on whether the
target factor of `T^c` commutes with `Z`.

| Input label `T` | Correction `T^c=CX T CX` | `s(T)` | Tagged angle |
|---|---|---:|---:|
| `II` | `II` | +1 | `+theta` |
| `IX` | `IX` | -1 | `-theta` |
| `IY` | `ZY` | -1 | `-theta` |
| `IZ` | `ZZ` | +1 | `+theta` |
| `XI` | `XX` | -1 | `-theta` |
| `XX` | `XI` | +1 | `+theta` |
| `XY` | `YZ` | +1 | `+theta` |
| `XZ` | `YY` | -1 | `-theta` |
| `YI` | `YX` | -1 | `-theta` |
| `YX` | `YI` | +1 | `+theta` |
| `YY` | `XZ` | +1 | `+theta` |
| `YZ` | `XY` | -1 | `-theta` |
| `ZI` | `ZI` | +1 | `+theta` |
| `ZX` | `ZX` | -1 | `-theta` |
| `ZY` | `IY` | -1 | `-theta` |
| `ZZ` | `IZ` | +1 | `+theta` |

The table is balanced: eight labels produce each sign.  M3 may freeze a
balanced subset or joint design, but it may not change this absorption map
after Gate-1 outcomes are inspected.

## 4. Boundaries, measurement, and records

- Initial boundary: the incoming correction is `I`; the first sampled Pauli is
  an explicit dressed easy gate.
- Final boundary: the final twirl is `I`. If a later implementation instead
  leaves a Pauli at measurement, it must relabel each bit by the Pauli's `X`
  component before likelihood evaluation; `Z` components do not change
  computational-basis bits.
- Labels are sampled independently across tagged blocks in the primary design
  unless M3 freezes a correlated balanced design. Correlation is permitted only
  when the full joint label vector is recorded and used by the likelihood.
- Each execution record stores circuit and compiler hashes, candidate and
  location indices, input `T`, correction `T^c`, sign, commanded signed angle,
  randomization ID, shot count, measurement-relabel mask, and outcome counts.
- Labels are retained per randomized circuit. An average over randomized
  circuits is reported separately and is never substituted for conditional
  label data.

## 5. Verification

The cancellation proof in Section 1 covers every multi-location label pattern.
`python tools/check_rc_semantics.py` independently enumerates all 16 local
labels at four angles and checks the dressed and bare matrices up to global
phase (64 label-angle cases). This is a deterministic semantic check, not a
research simulation and not evidence that E2 is identifiable.
