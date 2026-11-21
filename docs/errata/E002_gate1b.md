# Erratum E002 — Gate 1B / P-amp (2026-11-21)

**Affected frozen artifacts (unchanged):** `tools/run_gate1b.py`,
`results/gate1b/gate1b_results.json`, `docs/results/gate1b_report.md`.

**Frozen verdict:** PASS, P-amp is the sole sensor. **Status:** the verdict
**stands**, within the synthetic, noiseless, known-reference model only.

## 1. Defects and limitations

| # | Issue | Disposition |
|---|---|---|
| 1 | **Inverse-crime recovery check.** Pass condition (b) generated the P-amp phases from the same linear phase model that the estimator inverts (`pamp.exact_residuals`), so it tested only the algebra of the least-squares inversion, not the circuits. | Closed for the synthetic model by a new deterministic circuit check (below). |
| 2 | **Sensor–target transfer holds by construction.** P-amp and the target share one `(epsilon, phi)` acting on every commanded tagged angle, and the P-amp block has its control in `\|0>`, so `CX` acts trivially. The listed failure mode "the repeated block does not reproduce the target-context error" therefore cannot occur in any study run so far. | Limitation; must be stated with every P-amp claim. |
| 3 | **Resource margin is thin.** Condition (c) passes with `SE = 0.0070902` against `0.0071429` (0.7% headroom) under the frozen conservative bound `Var(u_hat) <= 1/135` at visibility 1. Because the standard error scales as `1/v`, the condition fails for visibility `v < 0.99263`. No visibility loss was modeled in Gates 1B–4. | Limitation. (The exact shot-noise variance at visibility 1 is at most `1/270`, which gives more headroom, but that tighter bound was not frozen.) |
| 4 | **No comparator evidence.** The P2 comparator was nonevaluable at Gate 1 (no twin circuit or threshold frozen). Its Gate 2 implementation is structurally blind on half of the units (E003 §5). | No claim that P-amp outperforms P2. |

## 2. Deterministic circuit check

`tools/check_pamp_semantics.py`, also run by `tests/test_errata.py`, simulates
the frozen P-amp circuits at state-vector level with the frozen gate
primitives:

- `B(a) = CX – RZ((1+epsilon)a + phi) – CX`, with control `|0>` and target `|+>`;
- the six repetition circuits and three echo circuits;
- target `<X>` and `<Y>`, on all 81 grid points.

**Result:** 729 circuit–grid cases. The largest deviation from the phase model
used by the estimator is `3.4e-15`, and the control-qubit leakage is 0.

The P-amp phase model is therefore exact for the frozen synthetic circuits.
This is a semantic check; it says nothing about visibility, drift, context
mismatch, or any physical carrier of E2.

## 3. Claim boundary (restated)

> Under the synthetic compiled-angle model with no decoherence, the frozen
> P-amp design identifies `(epsilon, phi)` from its own known reference, and
> its first-order resource condition holds at visibility 1 with a 0.7% margin.

Nothing stronger is supported.
