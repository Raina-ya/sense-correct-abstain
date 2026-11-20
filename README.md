# sense-correct-abstain
Fixed-budget decision control under angle-dependent coherent bias in QAOA. Tests whether randomized compiling labels can identify multiplicative over-rotation and guide no action, recalibration, or abstention, while deriving limits on when no probe can choose reliably. Simulation-first; hardware only as a registered addendum.

## North-star question

> Under a fixed quantum-execution budget, when is runtime evidence sufficient to decide whether to trust, correct, or withhold a quantum decision?

## Current status

Planning only. No experiment has been run, no protocol has been independently registered, and no hardware execution is authorized.

The full scientific rationale and gate criteria are in [the research program plan](docs/research_program_plan_v0.md). The public task hierarchy, research branches, subtasks, and extension tracks are in [the research work plan](docs/schedule/research_schedule_v1.md).

The problem-oriented reading queue, verification rules, and source ledger are in [docs/literature/](docs/literature/README.md).

An unreviewed analytic draft for Gate 1 (frame bookkeeping for RC labels, with one single-qubit numerical check) is in [docs/theory/gate1_frame_covariance_draft.md](docs/theory/gate1_frame_covariance_draft.md). It is not a proof and not a result.

Main Task 1 drafts (unreviewed, not frozen): the [decision-problem contract](docs/contracts/decision_problem_v1.md) (units, actions, loss, deployability boundary, primary endpoint, and the owner decisions D1–D3 laid out as options) and the [three-action theory draft](docs/theory/three_action_theory_v1.md) (risk identity, blindness lemma, finite-pilot lower bound, value of information, non-degeneracy).
