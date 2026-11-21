# Erratum E005 — Governance, locking, and reproducibility (2026-11-21)

**Scope:** process defects that affect how much the M3–M6 locks prove. No
verdict is changed. Nothing is retroactively relocked or backdated.

## 1. Analysis code was outside every lock

| Gate | Lock commit (hashes) | Code committed with the results | Gap |
|---|---|---|---|
| 1A/1B | `14432b2` (design documents and `check_gate1_lock.py`) | `gate1.py`, `pamp.py`, `run_gate1a.py`, `run_gate1b.py` in `eb08d50` | Gate 1A ran at 2026-11-20 08:04 UTC; results and code were committed about 22 hours later. |
| 2 | `38d900d` (design document only) | `gate2.py`, `run_gate2.py` in `1e3fa30` | Code untracked at run time. |
| 3/4 | `2dd9e2a` (design document only) | `gate34.py`, `run_gate34.py` in `017bc76` | Code untracked at run time. |

The runners verify `HEAD == lock commit` and refuse to overwrite outputs.
Since the runners were untracked files at run time, the repository cannot show
that the code that produced each artifact existed, unchanged, before
execution. In Gate 1A that code contains the hard-coded verdict (E001). The
artifact manifests hash the code *as committed afterwards*, which proves
consistency, not precedence.

## 2. Locked plan files cannot carry status or deviations

The M3 manifest hashes `docs/research_program_plan_v0.md`,
`docs/schedule/research_schedule_v1.md`, and
`docs/contracts/decision_problem_v1.md`. Consequences:

- Status tables in the locked work plan are frozen at M3. They still show
  MT3 "Gate 1A computation not started" and MT4–MT6 "not started".
- Deviations from the program plan (E003 §1, E004 §3–4) could not be recorded
  as the dated revision notes that the plan's change control requires.

**Remedy.** Current status lives in
[`../results/project_status.md`](../results/project_status.md), and plan
deviations are recorded in these errata. The locked files are left unchanged
on purpose. Editing them would break the M3 manifest.

## 3. Pace and review record

| Interval | Duration |
|---|---|
| M2 commit (`17438aa`) → M3 lock (`14432b2`) | 34 min |
| Gate 2 design (`b89ca4b`) → content-changing re-lock (`38d900d`) → run (`1e3fa30`) | 2 min + 6 min |
| Gate 3/4 lock (`2dd9e2a`) → run (`017bc76`) | 7 min |

Several locks state "owner-approved", but no review record exists. Nothing
here shows misconduct. A reader, however, cannot verify that the design
choices were scrutinized before execution, and several defects (E001 §1,
E003 §1, E004 §1 and §3) are of the kind that review catches.

## 4. Environment and platform dependence

- **No environment pin existed.** `requirements.txt` now records NumPy 2.3.5,
  the version stored in the Gate 2 and Gate 3/4 artifacts. The original
  Python version and platform were not recorded and cannot be recovered.
- **Full recomputation** (`tools/audit_reproducibility.py 1`, NumPy 2.3.5,
  Python 3.13.18, Linux x86-64) →
  `results/errata/reproducibility_full.json`:

  | Study | Units recomputed | Units with any differing stored float | Verdict-relevant fields changed | Gate statistic |
  |---|---:|---:|---|---|
  | Gate 2 | 6600 | 416 (mostly `p2_alarm`) | none (predictions and labels identical) | identical |
  | Gate 3/4 | 5940 | 31 (25 evaluation, 6 policy-lock) | `policy_loss` and `fixed_losses` in 31 units; actions identical | `Delta_V` and lower bound identical |

- **Second environment (sampled).** `tools/audit_reproducibility.py 50` was
  run on Linux, Python 3.10.12, NumPy 2.2.6, recomputing every 50th unit in
  frozen generation order. Gate 2: 15 of 132 units differ. Gate 3/4: 1 of 119
  units differs. No verdict-relevant field changed. The audit outputs in
  `results/errata/` regenerate byte-identically there.
- **Cause.** Last-bit differences in the computed outcome probabilities (for
  example `0.25` against `0.24999999999999997`) occasionally change one
  multinomial count. The artifacts are reproducible at the verdict level, not
  bit for bit across platforms.

## 5. Requirements for any future locked study in this repository

1. The lock commit must contain and hash the runner, every imported module,
   the tests, and `requirements.txt`. A design document alone is not
   sufficient.
2. Results must be committed immediately after execution, with the run log.
3. Probabilities that feed a sampler must be rounded or computed exactly so
   that sampling is platform independent, or the platform must be recorded.
4. Power or futility assessment must have its own commit before any
   evaluation outcome is generated.
5. Status must not live in hashed files.
6. Each lock must reference a written review note, even a short one.
