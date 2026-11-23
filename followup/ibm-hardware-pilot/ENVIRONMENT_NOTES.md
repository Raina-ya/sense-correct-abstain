# HW-P1 environment notes

## Local Windows preflight

- Python: 3.12.14 in `.venv312` (untracked).
- Installed: Qiskit 2.6.2, qiskit-ibm-runtime 0.50.1, qiskit-aer 0.17.2.
- Qiskit circuit construction and `Statevector` execution pass.
- The complete deterministic sampled analysis-pipeline test passes.
- IBM Runtime import is blocked by Windows Smart App Control when an unsigned
  SciPy HiGHS native extension is loaded.
- `charset-normalizer`'s optional native extension is blocked by the same
  policy; `requests` falls back with a warning.
- Aer imports, but even one small noisy execution does not finish within the
  120-second preflight limit on this environment. It is therefore not recorded
  as a passed fake-backend check.

No Windows security control was disabled. Hardware connection, real-backend
transpilation, usage estimation from the selected backend target, and job
submission must be performed in a Linux environment with the locked package
versions. None has been performed as of 2026-11-23.
