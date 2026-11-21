# sense-correct-abstain
Fixed-budget decision control under angle-dependent coherent bias in QAOA. Tests whether randomized compiling labels can identify multiplicative over-rotation and guide no action, recalibration, or abstention, while deriving limits on when no probe can choose reliably. Simulation-first; hardware only as a registered addendum.

## North-star question

> Under a fixed quantum-execution budget, when is runtime evidence sufficient to decide whether to trust, correct, or withhold a quantum decision?

## Current status

**Route completed: Gate 1A FAIL → Gate 1B PASS (P-amp) → Gate 2 PASS → Gate 3 FAIL → stop after M6.** The next task is MT7 synthesis. No confirmatory registration or holdout is authorized, and no hardware execution has been run or authorized. All evidence is analytic or synthetic simulation.

- Current status and supported claims: [docs/results/project_status.md](docs/results/project_status.md). The status tables inside the M3-locked plan files are frozen at M3 and stale.
- Post-lock audit: [docs/audits/m2_m6_post_lock_audit.md](docs/audits/m2_m6_post_lock_audit.md).
- **Errata E001–E005:** [docs/errata/](docs/errata/README.md). They correct the frozen Gate 1A–4 records without editing any frozen file. Read them before citing any gate report.

Main documents:

- Scientific rationale and gate criteria: [research program plan](docs/research_program_plan_v0.md). Task hierarchy: [research work plan](docs/schedule/research_schedule_v1.md). Both are frozen by the M3 lock.
- Main Task 1: [decision-problem contract](docs/contracts/decision_problem_v1.md) and [three-action theory draft](docs/theory/three_action_theory_v1.md).
- M2 semantics: [E2 semantics](docs/theory/e2_semantics_v1.md), [RC construction](docs/theory/rc_construction_v1.md), [conditional likelihood](docs/theory/conditional_likelihood_v1.md), [frame-covariance note](docs/theory/gate1_frame_covariance_draft.md).
- Gate records: [Gate 1A](docs/results/gate1a_report.md) (see E001), [Gate 1B](docs/results/gate1b_report.md) (E002), [Gate 2](docs/results/gate2_report.md) (E003), [Gates 3/4](docs/results/gate3_gate4_report.md) (E004).
- Literature: [docs/literature/](docs/literature/README.md).

## Reproducing the checks

```bash
pip install -r requirements.txt
python -m pytest -q tests
python tools/check_errata_artifacts.py   # errata hashes + every frozen lock/artifact check
python tools/check_rc_semantics.py
python tools/check_pamp_semantics.py
python tools/check_library.py
```
