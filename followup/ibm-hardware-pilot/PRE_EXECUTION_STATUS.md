# HW-P1 pre-execution status

**Status:** local preparation complete; cloud/backend checks and owner approval
pending; no hardware execution.

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

## Not passed or not attempted

- Qiskit Aer noisy execution is not usable in the local Windows environment;
  even one representative noisy circuit exceeded the 120-second preflight
  limit. No fake-backend pass is claimed.
- IBM Runtime import is blocked locally by Windows Smart App Control.
- No IBM backend has been selected or queried.
- No real-backend transpilation, dry-run service call, protocol lock, external
  timestamp, or hardware submission has occurred.

The deterministic sampled report is a code-path test only and is not a
scientific result of HW-P1.
