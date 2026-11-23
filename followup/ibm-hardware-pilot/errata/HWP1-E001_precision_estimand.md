# HWP1-E001 — Precision estimand implemented as SE of the mean; five "meets" labels retracted

**Study:** HW-P1 Stage A (separate IBM hardware follow-up; not part of the
frozen sense-correct-abstain study and not covered by errata E001–E009).
**Date:** 2026-11-23. **Type:** append-only post-lock correction.
**Affected artifacts (unchanged, still hash-bound):**
`followup/ibm-hardware-pilot/analyze_stage_a.py` (locked code),
`followup/ibm-hardware-pilot/results/stage_a/analysis_primary.json` (locked
output), recorded in `docs/freeze/hwp1_stage_a_lock_v2.json` as committed in
`ead7168` (execution-time lock, canonical SHA-256
`f4b60e026386769918327196883a74c406179c0356e348262f5ece5ec76f1a56`) and with
post-run artifact hashes in `88eb721`. None of these files, nor any raw QPU
result, is modified by this erratum.

## 1. The defect

The locked protocol (`PROTOCOL_DRAFT.md` §5, estimand 1) specifies
`SE_hw(eps_hat)` **at 2430 shots**, from the spread of the eight block
estimates, pooled over points, with outcome labels comparing it to the frozen
threshold `0.0071429`. That threshold refers to the standard error of a
**single** 2430-shot estimate (the frozen Gate 1 resource condition).

The locked analysis implemented the per-point "SE" as

```python
def sample_se(values):
    return statistics.stdev(values) / math.sqrt(len(values))   # len(values) == 8
```

which divides the spread of the eight 2430-shot estimates by an extra
`sqrt(8)` (about 2.83). That is the standard error of the **mean of eight
blocks** (about 19,440 shots per point), not the protocol estimand. Its
bootstrap interval and outcome label inherit the error. The protocol's pooled
estimate was not implemented at all.

The locked protocol and the locked code therefore disagree. The protocol
defines the estimand; the code is its implementation. The estimand definition
governs.

## 2. Retraction

All five locked precision labels are **retracted**:

| Injected `(epsilon, phi)` | Locked value (SE of 8-block mean) | Locked label | Corrected: SD of one 2430-shot estimate | 95% block-bootstrap interval | Corrected label |
|---|---:|---|---:|---|---|
| `(0.00, 0.00)` | 0.00218 | ~~meets~~ | 0.00618 | [0.00264, 0.00815] | inconclusive |
| `(+0.02, 0.00)` | 0.00207 | ~~meets~~ | 0.00587 | [0.00227, 0.00721] | inconclusive |
| `(-0.02, 0.00)` | 0.00187 | ~~meets~~ | 0.00528 | [0.00129, 0.00723] | inconclusive |
| `(+0.04, +0.01)` | 0.00271 | ~~meets~~ | 0.00768 | [0.00312, 0.01012] | inconclusive |
| `(-0.04, -0.01)` | 0.00412 | ~~meets~~ | 0.01167 | [0.00572, 0.01456] | inconclusive |
| **pooled within-point** | not computed | — | **0.00769** (35 d.f.) | [0.00523, 0.00845], joint bootstrap | **inconclusive** |

The pooled point estimate is 1.08 times the threshold. No point and no pooled
estimate meets the threshold. Any statement that HW-P1 "met the precision
threshold" is withdrawn.

Machine-readable output:
`followup/ibm-hardware-pilot/results/stage_a_postlock/analysis_corrected.json`,
produced by `followup/ibm-hardware-pilot/analyze_stage_a_postlock.py`
(post-lock; it recomputes the per-block estimates from raw counts without
Qiskit and checks them against the locked per-block estimates, maximum absolute
difference 2.1e-17). Both are hash-bound in `hwp1_errata_manifest.sha256`.

**Caveat.** Eight blocks give coarse intervals; percentile bootstrap intervals
for an SD from n = 8 tend to be too narrow and biased low. The corrected labels
are descriptive and must not be read as a test.

## 3. What is not affected

- The raw counts, job IDs, calibration snapshots, usage (56 QPU-charge seconds,
  0.849416 resource units), and the absence of recalibration between blocks.
- The validity checks: readout assignment error 0.8–1.7% per block (below 5%);
  no significant Z-control comparison (Bonferroni familywise 0.05); the stage
  is valid.
- The bias results, computed correctly by the locked code: zero-injection
  `epsilon` bias −0.01283 with 95% interval [−0.01661, −0.00863], which
  triggers the locked bias flag; `phi` bias between +0.0075 and +0.0094 at every
  injected point.
- Effective visibility 0.9475–0.9574 and drift slope 0.0001017 per block.

## 4. Related disclosures

1. **Approval record.** The locked `LOCK_REVIEW.md` and `PROTOCOL_DRAFT.md` say
   owner approval was pending. At execution the only approval evidence was the
   runner's hash gate (`HWP1_APPROVED_LOCK_SHA256` had to equal the lock's
   canonical hash). A written record was added after execution:
   `OWNER_APPROVAL_POSTHOC.md`.
2. **Timing and status.** The lock was committed at 15:01:20 (+08:00) and the
   first job was created about two minutes later; there is no external
   timestamp. HW-P1 is a prespecified study under an internal lock, **not** a
   preregistered study.
3. **Locked wording now stale.** The locked `PROTOCOL_DRAFT.md` header says
   "nothing executed". It is hash-locked and stays unchanged; this erratum and
   `RESULTS.md` record that Stage A was executed on 2026-11-23.
4. **Possible cause of the offset (hypothesis only).** The common `phi` offset
   and the zero-injection `epsilon` offset are consistent with a native
   coherent phase on the physical pair 53/54, for example from CZ or ZZ
   interactions. HW-P1 did not test this; it is a possible cause, not a
   finding.
5. **Not executed:** Stage B, the fractional-RZZ option, and any further QPU
   job.
