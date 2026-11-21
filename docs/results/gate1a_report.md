# Gate 1A report

**Run time (UTC):** 2026-11-20T08:04:15.687938+00:00

**Frozen lock commit:** `14432b26f00309fee7529c61b7ec884a491b9fc9`
**Evidence:** analytic and exact noiseless simulation under the synthetic compiled-angle model; no hardware and no noisy-development evidence.

## Verdict

**Gate 1A fails.** The M3-frozen deployable profile estimator is nonunique under the saturated unknown-response nuisance class. No frozen primary design recovered `(epsilon,phi)` at any of the 81 required grid points. Oracle I2 can have rank that is unavailable to the deployable experiment and is not used to pass the gate.

This verdict routes the project to the already frozen Gate 1B P-amp fallback. Gate 1B was not executed in this run.

## Information-source table

Rank counts are shown as dictionaries over all 81 grid points. I3 is the deployable profile information under the frozen saturated nuisance class.

| Context | Candidate design | I1 rank counts | I2 rank counts | I3 rank counts | Profile recovery |
|---|---|---|---|---|---|
| G2-primary | single | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |
| G2-primary | same | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |
| G2-primary | distinct | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |
| G3-primary | single | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |
| G3-primary | same | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |
| G3-primary | distinct | {'0': 0, '1': 9, '2': 72} | {'0': 0, '1': 0, '2': 81} | {'0': 81, '1': 0, '2': 0} | 0/81 |

I1 numerical values use the conditional-minus-marginal chain-rule calculation from the exact likelihood. They quantify retained-label information under the synthetic model; they do not supply the unknown response map to the runtime estimator. I2 treats that response as known and is diagnostic only.

## Controls

- `phi=0` label invariance: passed; maximum probability difference `0`.
- Single-angle and same-angle controls: failed identification as predicted.
- Score-zero measurement control: passed.
- Logical-angle control: label blind as predicted.
- Distinct-angle design: oracle information can increase, but deployable I3 remains nonunique.
- Label shuffle: **nonevaluable protocol defect**. M3 froze the requirement but not a scalar shuffle statistic or the permutation realization. No replacement was introduced after the lock.
- `p=2`: not run; the frozen lock forbids using it to rescue the negative primary result.

## Finite-separation pairs

Distances use the full observed `(label,bitstring)` distribution under the exact synthetic model. Action relevance is nonevaluable because M3 did not freeze a target decision/action map for these reference contexts; every pair is retained as a failed action-relevant construction.

| Context | theta_ref | epsilon_1 | phi_1 | TV | Le Cam error lower bound | Action relevance |
|---|---:|---:|---:|---:|---:|---|
| G2-primary | 0.39269908 | +0.02 | -0.00785398 | 0.0036161146 | 0.49819194 | nonevaluable |
| G2-primary | 0.39269908 | -0.02 | +0.00785398 | 0.0036397199 | 0.49818014 | nonevaluable |
| G2-primary | 0.78539816 | +0.02 | -0.01570796 | 0.0054654616 | 0.49726727 | nonevaluable |
| G2-primary | 0.78539816 | -0.02 | +0.01570796 | 0.0056399188 | 0.49718004 | nonevaluable |
| G3-primary | 0.39269908 | +0.02 | -0.00785398 | 0.0054181907 | 0.4972909 | nonevaluable |
| G3-primary | 0.39269908 | -0.02 | +0.00785398 | 0.0054577025 | 0.49727115 | nonevaluable |
| G3-primary | 0.78539816 | +0.02 | -0.01570796 | 0.0069508658 | 0.49652457 | nonevaluable |
| G3-primary | 0.78539816 | -0.02 | +0.01570796 | 0.0072667181 | 0.49636664 | nonevaluable |

## Signed prediction-mismatch list

| Frozen prediction/control | Outcome | Disposition |
|---|---|---|
| Dressed semantic equivalence | Passed in the pre-existing 64-case checker and exact simulator tests | Match |
| I1 for `epsilon` is zero at `phi=0` | Passed numerically and analytically | Match |
| Logical-angle control is label blind | Passed | Match |
| Score-zero control has no information | Passed | Match |
| I2 can show unavailable oracle information | Observed in the exact diagnostic | Match; not admitted |
| Full Gate 1A failure | Confirmed under the frozen nuisance class | Prediction confirmed |
| Label-shuffled control evaluable | Not sufficiently specified by M3 | Protocol defect; no post-lock repair |
| Hard pairs imply different actions | Not evaluable from the frozen reference contexts | Failed construction retained |

## Limitations

The result is specific to the frozen synthetic compiled-angle model and saturated deployable nuisance boundary. It does not show that real virtual-Z hardware has E2, that all structured response models are blind, or that RC fails as an averaged-channel method. The small exact circuits make I2 computable, but using that quantity at runtime is explicitly forbidden. The Gate 1A failure cannot be generalized beyond the frozen task without a new study.

## Artifact

Machine-readable matrices, ranks, distances, and control records are in `results/gate1a/gate1a_results.json`.
