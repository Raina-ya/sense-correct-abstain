# HW-P1 pre-execution status

> **Historical pre-execution record (kept unchanged below).** Stage A was executed on 2026-11-23; see [`RESULTS.md`](RESULTS.md) and erratum [`HWP1-E001`](errata/HWP1-E001_precision_estimand.md).

**Status:** local and cloud preflight complete; lock generation and owner
approval pending; no hardware execution.

## Passed locally

- 18 frozen P-amp settings are generated for each injected point.
- 90 Qiskit Statevector circuit-point cases agree with the analytic phase model
  to maximum absolute error `1.6653345369377348e-15`.
- Four unit tests pass.
- The full eight-block deterministic sampled analysis pipeline completes.
- The design ledger is 720 P-amp circuits, 40 Z controls, 32 readout-calibration
  circuits, and 134,600 total executions.
- The official quick usage formula gives 63.11 seconds (1.052 minutes), before
  contingency and before real-backend duration information.

## Passed against live backend metadata (no QPU submission)

- `ibm_fez` and `ibm_marrakesh` were operational Heron revision 2 backends.
- All 90 unique P-amp circuits retained a two-qubit gate on both backends.
- Both transpiled sets had depth 1--423.
- `ibm_marrakesh` target 53/control 54 was selected: calibration-error score
  `0.010394652277849997`, lower than Fez's `0.012429572224712998`.
- The selected unique-circuit durations were 2.684--11.716 microseconds.

## Not passed or not attempted

- Qiskit Aer noisy execution is not usable in the local Windows environment;
  even one representative noisy circuit exceeded the 120-second preflight
  limit. No fake-backend pass is claimed.
- IBM Runtime imports successfully in the owner's Python 3.14 environment;
  Qiskit Aer remains blocked by Windows Smart App Control and is not required
  for the cloud preflight or QPU runner.
- No protocol lock, external timestamp, or hardware submission has occurred.

The deterministic sampled report is a code-path test only and is not a
scientific result of HW-P1.
