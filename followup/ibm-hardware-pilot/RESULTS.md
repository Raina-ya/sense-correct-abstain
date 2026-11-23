# HW-P1 Stage A hardware results

**Evidence type:** IBM Quantum hardware-derived counts from a separately
locked follow-up study.

> **Correction (HWP1-E001, 2026-11-23).** The locked script reported the
> standard error of the *mean of eight blocks* instead of the protocol's
> single-estimate precision at 2430 shots, and labelled all five points
> "meets". Those labels are **retracted**. Under the protocol's estimand the
> precision is **inconclusive** at every point and pooled (pooled SD 0.00769,
> 95% interval [0.00523, 0.00845], threshold 0.0071429). See
> [`errata/HWP1-E001_precision_estimand.md`](errata/HWP1-E001_precision_estimand.md). These results do not revise any frozen Gate 1--4
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

## Locked primary analysis (precision labels retracted)

The stage validity checks passed. Per-block maximum single-qubit readout
assignment errors ranged from 0.8% to 1.7%, below the locked 5% bound. None of
the four Bonferroni-adjusted Z-control comparisons was significant. The
zero-injection drift slope was `0.0001017` epsilon units per block.

| Injected `(epsilon, phi)` | Mean `epsilon_hat` | Bias | Locked "SE" (= SE of 8-block mean) | Its bootstrap 95% interval | Locked label (retracted) |
|---|---:|---:|---:|---:|---|
| `(0.00, 0.00)` | -0.01283 | -0.01283 | 0.00218 | [0.00095, 0.00291] | ~~meets~~ |
| `(0.02, 0.00)` | 0.01658 | -0.00342 | 0.00207 | [0.00080, 0.00253] | ~~meets~~ |
| `(-0.02, 0.00)` | -0.02100 | -0.00100 | 0.00187 | [0.00046, 0.00257] | ~~meets~~ |
| `(0.04, 0.01)` | 0.03221 | -0.00779 | 0.00271 | [0.00127, 0.00357] | ~~meets~~ |
| `(-0.04, -0.01)` | -0.04600 | -0.00600 | 0.00412 | [0.00190, 0.00515] | ~~meets~~ |

These "SE" values are the standard error of the mean of eight 2430-shot
estimates, not the protocol estimand, so their comparison with the
single-estimate threshold `0.0071429` is invalid (HWP1-E001).

## Corrected precision (post-lock)

| Injected `(epsilon, phi)` | SD of one 2430-shot estimate | 95% block-bootstrap interval | Label |
|---|---:|---:|---|
| `(0.00, 0.00)` | 0.00618 | [0.00264, 0.00815] | inconclusive |
| `(0.02, 0.00)` | 0.00587 | [0.00227, 0.00721] | inconclusive |
| `(-0.02, 0.00)` | 0.00528 | [0.00129, 0.00723] | inconclusive |
| `(0.04, 0.01)` | 0.00768 | [0.00312, 0.01012] | inconclusive |
| `(-0.04, -0.01)` | 0.01167 | [0.00572, 0.01456] | inconclusive |
| pooled within-point (35 d.f.) | 0.00769 | [0.00523, 0.00845] (joint bootstrap) | inconclusive |

Output: [`results/stage_a_postlock/analysis_corrected.json`](results/stage_a_postlock/analysis_corrected.json),
from `analyze_stage_a_postlock.py`. Eight blocks give coarse intervals; read
the labels as descriptive.

## Bias, visibility, drift (locked analysis; unaffected)

The zero-injection bias interval was
`[-0.01661, -0.00863]`, which triggered the locked bias flag. Mean effective
visibility ranged from 0.9475 to 0.9574, below the synthetic study's 0.99263
resource-condition value.

## Supported conclusion

Under deterministic compiled-angle injection on this backend and layout, the
single-estimate precision of P-amp at the frozen 2430-shot budget was
inconclusive against the frozen threshold, with a pooled point estimate 8%
above it, and the estimator showed a material offset at zero injection. A
native coherent phase on the physical pair (for example from CZ or ZZ
interactions) is a possible cause; HW-P1 did not test it. HW-P1 does **not**
support a claim that P-amp met its precision threshold on hardware, accurate
recovery without bias characterisation, the natural presence of an
angle-proportional hardware error, correction benefit, or operational
usefulness of the three-action policy. Approval for execution was recorded
after the run ([`OWNER_APPROVAL_POSTHOC.md`](OWNER_APPROVAL_POSTHOC.md)); the
study was prespecified under an internal lock and is not preregistered.

The locked machine-readable output is
[`results/stage_a/analysis_primary.json`](results/stage_a/analysis_primary.json)
(unchanged; its precision labels are superseded by HWP1-E001).
All 17 raw and analysis artifacts are hash-bound in
[`../../docs/freeze/hwp1_stage_a_lock_v2.json`](../../docs/freeze/hwp1_stage_a_lock_v2.json),
which passed the v2 post-lock checker in the execution environment.
