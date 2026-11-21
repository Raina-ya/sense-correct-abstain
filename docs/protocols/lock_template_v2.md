# Protocol lock template v2

**Status:** policy for any **future** locked computation in this repository,
adopted 2026-11-21 (E005 §5, E006 §7). It does not modify or retroactively
upgrade the M3, Gate 2, or Gate 3/4 locks.

## Why v2

The v1 locks hashed design documents only. Runner code, imported modules,
environment, seeds, and command were outside the lock, and results were
committed with the code afterwards (E005 §1). A v2 lock makes precedence
checkable.

## Procedure

1. **Write** the design document, the runner, every module it imports, its
   tests, and `requirements.txt`. Record the full environment.
2. **Fill** a lock record `docs/freeze/<lock_id>_lock_v2.json` (schema
   below). Every hash is SHA-256 after CRLF-to-LF canonicalization.
3. **Check:** `python tools/check_protocol_lock.py <lock.json> --phase pre`.
   The check fails if:
   - any hash is wrong;
   - any local import of the runner is not hashed;
   - the running Python or package versions differ from the record;
   - any field is "unknown"; or
   - any declared output already exists.
4. **Commit** the lock record and everything it hashes, together with a short
   written review note referenced in the design document.
5. **Run** the exact `command` from the locked commit. Commit the outputs and
   the run log immediately.
6. **Close:** add the `artifacts` map (output and log hashes) in a new commit,
   then run `python tools/check_protocol_lock.py <lock.json> --phase post`.
7. **Futility first.** If a power or futility assessment is part of the design,
   lock and run it as its own step before any evaluation outcome is
   generated.
8. **Status** lives in `docs/results/project_status.md`, never in hashed files.
9. **Platform-independent sampling.** Probabilities that feed a random sampler
   are rounded to a fixed number of decimals (or computed exactly) before
   sampling, or the platform is recorded and the lock states that bit-level
   reproduction is platform specific (E005 §4).

## Lock record schema

```json
{
  "schema": "protocol_lock_v2",
  "lock_id": "example",
  "design_files": {"docs/freeze/example_design.md": "<sha256>"},
  "code_files": {
    "tools/run_example.py": "<sha256>",
    "src/sense_correct_abstain/__init__.py": "<sha256>",
    "src/sense_correct_abstain/example.py": "<sha256>",
    "tests/test_example.py": "<sha256>"
  },
  "environment_files": {"requirements.txt": "<sha256>"},
  "environment": {
    "python": "3.x.y",
    "platform": "<platform.platform() output>",
    "packages": {"numpy": "x.y.z"}
  },
  "seeds": {"root": 0, "derivation": "SHA256(prefix|unit_key|stream)[:8], big-endian"},
  "command": ["python", "tools/run_example.py"],
  "runner": "tools/run_example.py",
  "outputs": ["results/example/"],
  "artifacts": {}
}
```

## Not allowed

- A lock whose environment contains "unknown".
- Editing any hashed file after the lock commit. Defects are reported in an
  append-only erratum.
- Calling an internal Git or SHA-256 lock a "preregistration"; that word
  requires an independent timestamp.
