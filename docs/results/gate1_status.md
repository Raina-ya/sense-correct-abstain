# Gate 1 current status

This file records post-lock execution status without modifying the inputs hashed by the M3 design lock.

- **Milestone:** M4 achieved.
- **Gate 1A:** FAIL under the frozen saturated unknown-response nuisance model; route to Gate 1B.
- **Gate 1B:** PASS for the frozen P-amp design; route to Gate 2.
- **Primary Gate 2 sensor:** P-amp only.
- **P2 alarm comparison:** reported as nonevaluable because M3 did not freeze a twin circuit or alarm threshold. No superiority claim is made.
- **Evidence class:** synthetic analytic/exact-noiseless evaluation. These results are not noisy-simulation or hardware evidence.
- **Next task:** MT4 / Gate 2 has not started.

Detailed records:

- [Gate 1A report](gate1a_report.md)
- [Gate 1B report](gate1b_report.md)
- [Gate 1A machine-readable results](../../results/gate1a/gate1a_results.json)
- [Gate 1B machine-readable results](../../results/gate1b/gate1b_results.json)
- [Gate 1 artifact manifest](../../results/gate1_artifact_manifest.sha256)

The frozen schedule and program-plan files remain unchanged after M3 because they are covered by `docs/freeze/gate1_design_lock_manifest.sha256`.
