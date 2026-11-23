# HW-P1 Stage A hardware results

**Evidence type:** IBM Quantum hardware-derived counts from a separately
locked follow-up study. These results do not revise any frozen Gate 1--4
verdict and do not test the adaptive decision policy on hardware.

## Execution record

- Backend: `ibm_marrakesh` (Heron revision 2).
- Physical layout: target 53, control 54; fractional gates disabled.
- Lock: `f4b60e026386769918327196883a74c406179c0356e348262f5ece5ec76f1a56`.
- Workload: eight completed blocks, 99 circuits per block, 134,600 total
  executions under the fixed design.
- Usage: 7 QPU-charge seconds per block, 56 seconds and 0.849416 resource
  units in total.
- Calibration snapshot timestamp: `2026-11-23T14:39:56+08:00` throughout;
  the runner detected no recalibration between blocks.
- IBM job IDs: `dc1uablhdvas73blbqg0`, `dc1uaginj2vs73dfsg70`,
  `dc1uakthdvas73blbqqg`, `dc1uasls2omc738b4s3g`,
  `dc1ub4ds2omc738b4sb0`, `dc1ubdds2omc738b4skg`,
  `dc1ubhls2omc738b4sr0`, and `dc1ubleq4uuc73a4f2t0`.

## Locked primary analysis

The stage validity checks passed. Per-block maximum single-qubit readout
assignment errors ranged from 0.8% to 1.7%, below the locked 5% bound. None of
the four Bonferroni-adjusted Z-control comparisons was significant. The
zero-injection drift slope was `0.0001017` epsilon units per block.

| Injected `(epsilon, phi)` | Mean `epsilon_hat` | Bias | SE | Bootstrap 95% interval for SE | Locked precision label |
|---|---:|---:|---:|---:|---|
| `(0.00, 0.00)` | -0.01283 | -0.01283 | 0.00218 | [0.00095, 0.00291] | meets |
| `(0.02, 0.00)` | 0.01658 | -0.00342 | 0.00207 | [0.00080, 0.00253] | meets |
| `(-0.02, 0.00)` | -0.02100 | -0.00100 | 0.00187 | [0.00046, 0.00257] | meets |
| `(0.04, 0.01)` | 0.03221 | -0.00779 | 0.00271 | [0.00127, 0.00357] | meets |
| `(-0.04, -0.01)` | -0.04600 | -0.00600 | 0.00412 | [0.00190, 0.00515] | meets |

All upper interval endpoints are below the locked `0.0071429` precision
threshold. The zero-injection bias interval was
`[-0.01661, -0.00863]`, which triggered the locked bias flag. Mean effective
visibility ranged from 0.9475 to 0.9574, below the synthetic study's 0.99263
resource-condition value.

## Supported conclusion

Under deterministic compiled-angle injection on this backend and layout, the
P-amp estimator met its locked repeatability threshold but exhibited a
material hardware offset at zero injection. HW-P1 therefore supports the
narrow claim that the sensor was precise under this run's real-noise
conditions; it does **not** support accurate recovery without additional bias
characterisation, the natural presence of an angle-proportional hardware
error, correction benefit, or operational usefulness of the three-action
policy.

The authoritative machine-readable output is
[`results/stage_a/analysis_primary.json`](results/stage_a/analysis_primary.json).
All 17 raw and analysis artifacts are hash-bound in
[`../../docs/freeze/hwp1_stage_a_lock_v2.json`](../../docs/freeze/hwp1_stage_a_lock_v2.json),
which passed the v2 post-lock checker in the execution environment.
