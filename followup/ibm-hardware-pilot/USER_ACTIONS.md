# HW-P1 actions requiring the owner

Real-backend metadata preflight is complete. No hardware job has been
submitted. IBM credentials remain private and are not part of the repository.

## Completed preparation

- IBM Open Plan and `open-instance` access confirmed.
- Qiskit 2.6.2 and qiskit-ibm-runtime 0.50.1 import successfully.
- Fez and Marrakesh were compared without QPU submission.
- Marrakesh target 53/control 54 is the lock candidate.
- Stage A is limited to eight blocks. Each block has a 22-QPU-second service
  limit, so the aggregate service-enforced ceiling is 176 seconds.

## Final lock

Do not submit circuits yet. From the repository root, generate and check the
environment-bound lock in the same Python environment that will execute it:

```powershell
python followup/ibm-hardware-pilot/prepare_lock.py
python tools/check_protocol_lock.py docs/freeze/hwp1_stage_a_lock_v2.json --phase pre
```

The owner must then:

1. confirm Stage A only, `ibm_marrakesh` target 53/control 54, eight blocks,
   fractional gates off, and unmitigated counts as primary;
2. authorize at most 3 QPU minutes;
3. choose whether to deposit the lock externally before execution;
4. sign `LOCK_REVIEW.md` and approve the lock's canonical SHA-256.

Only after those decisions and a passing pre-lock check should the approved
hash be placed in the process environment and the exact locked command run:

```powershell
$env:HWP1_APPROVED_LOCK_SHA256 = "APPROVED_CANONICAL_HASH"
python followup/ibm-hardware-pilot/run_stage_a.py --submit
```

The runner refuses a mismatched hash or an existing result directory. It never
retries a failed block, substitutes a backend, or starts Stage B.
