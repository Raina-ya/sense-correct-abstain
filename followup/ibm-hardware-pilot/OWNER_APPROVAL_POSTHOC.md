# HW-P1 Stage A — owner approval record (written after execution)

**This record was written on 2026-11-23, after Stage A had run.** No written
approval existed before execution. It documents what was approved and how, so
that the record is complete; it does not make HW-P1 preregistered, and it does
not alter any locked file. See erratum `errata/HWP1-E001_precision_estimand.md`
§4.

## How approval was given at execution time

The owner approved execution by setting `HWP1_APPROVED_LOCK_SHA256` to the
canonical SHA-256 of the execution-time lock,
`f4b60e026386769918327196883a74c406179c0356e348262f5ece5ec76f1a56`
(`docs/freeze/hwp1_stage_a_lock_v2.json` as committed in `ead7168`), and by
running the locked command `python followup/ibm-hardware-pilot/run_stage_a.py
--submit`. The runner refuses to submit unless that hash matches; all eight
submission receipts record this hash.

## Scope that was executed

- HW-P1 Stage A only: deterministic injected compiled-angle error, five
  injected points, eight interleaved blocks.
- Backend `ibm_marrakesh`, physical target 53 and control 54, fractional gates
  disabled, IBM Open Plan (`open-instance`).
- Unmitigated counts as the primary analysis.
- Per-block service limit of 22 QPU seconds (aggregate ceiling 176 s); measured
  usage was 56 QPU-charge seconds.
- No automatic retry, backend substitution, Stage B, or fractional-RZZ study.

## Status statements

- No external timestamp was deposited before execution; the study must not be
  called preregistered.
- The lock was reviewed by its preparer (`LOCK_REVIEW.md`); there was no
  independent reviewer.
- Stage B and any further QPU job require a new, separate approval.

Owner confirmation (post hoc): Zhen-Jun Liu, 2026-11-23.
