# Gate 3 and Gate 4 development report

**Run time (UTC):** 2026-11-21T07:17:26.531410+00:00

**M6 lock commit:** `2dd9e2aec2ed185e40ef42448cd2ba41aa9d95a6`

**Evidence:** split-99 development simulation only; no confirmatory holdout and no hardware.

## Decisions

- **Gate 3: FAIL**. `Delta_V = 0.000080` and the frozen one-sided 95% graph-cluster bootstrap lower bound is `-0.000743`.
- **Gate 4: PASS**. 2 actions clear both the 5% unit-frequency and 10-cluster requirements.
- Route: **Stop-after-M6**.

## Fixed comparator selection

The comparator was selected only on the 33 policy-lock graph clusters.

| Fixed policy | Mean primary loss | Status |
|---|---:|---|
| N-full | 0.029243 |  |
| N-sensor-allocation | 0.029577 |  |
| C-always | 0.007914 | selected |
| A-always | 0.250000 |  |

Selected comparator: **C-always**.

## Gate 4 action frequencies

| Action | Units | Frequency | Graph clusters | Clears |
|---|---:|---:|---:|---|
| N | 919 | 0.2592 | 66 | yes |
| C | 2573 | 0.7258 | 66 | yes |
| A | 53 | 0.0150 | 29 | no |

Observed policy-input gap ties: 1. Ties take the frozen abstain branch and do not count as evidence of non-degeneracy.

## Power and resource accounting

- Prospective 66-cluster power estimate from the 33 policy-lock clusters: `0.0004`.
- Policy-lock cluster SD: `0.003235`.
- Approximate minimum detectable positive mean: `0.000665`.
- Generated / evaluable evaluation units: 3960 / 3545.
- Infrastructure missing rate: `0.0000`.
- Budget: 24,300 shots per unit on every action path; classical computation is reported separately.

## Secondary loss sensitivity

| Abstention/failure weight | Delta_V |
|---:|---:|
| 0.10 | 0.002323 |
| 0.50 | -0.003657 |

These sensitivities cannot rescue or replace the primary result at weight 0.25.

## Claim boundary

The decisions are development evidence under the frozen synthetic model. They do not establish confirmatory generalization, physical-device realism, or hardware benefit. Proceeding to M7 is allowed only if both Gates pass and the required adversarial pre-data audit and independent registration are completed before any holdout is read.
