# HW-P1 Stage A lock review

**Status:** technical review complete; owner execution approval pending. This
record is not an independent review or an external preregistration.

## Fixed technical choices

- Study: HW-P1 Stage A only; deterministic injected compiled-angle error.
- Backend: `ibm_marrakesh`, Heron revision 2, fractional gates disabled.
- Physical qubits: target 53, control 54.
- Selection rule: minimum recorded sum of the two readout errors and directed
  CZ error. The recorded score is `0.010394652277849997`, versus
  `0.012429572224712998` for the zero-queue alternative `ibm_fez`.
- Eight interleaved blocks; unmitigated counts are primary.
- Maximum execution time is 22 QPU seconds per submitted block, so eight
  blocks have a service-enforced aggregate ceiling of 176 QPU seconds. The
  design estimate is 63.11 QPU seconds in total, but IBM bills measured usage.
- No automatic retry, backend substitution, Stage B, fractional-RZZ study, or
  silent rerun is authorized by this lock.

## Preflight evidence

Both candidate backends retained two-qubit gates in all 90 unique P-amp
circuits. Both had depth 1--423. The selected Marrakesh pair had lower
calibration-error score; its maximum unique-circuit duration was 11.716 us.
These are calibration-snapshot and transpilation facts, not hardware results.

## Owner approval still required

Before execution, the owner must confirm in writing: Stage A only; backend and
qubit pair; a maximum total authorization of 3 QPU minutes; unmitigated counts
as primary; whether an external timestamp is wanted; and the exact canonical
  SHA-256 of the generated lock file. Approval does not change the per-block
22-second safety limit.
