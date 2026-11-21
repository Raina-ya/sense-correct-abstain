# sense-correct-abstain
Fixed-budget decision control under angle-dependent coherent bias in QAOA. Tests whether randomized compiling labels can identify multiplicative over-rotation and guide no action, recalibration, or abstention, while deriving limits on when no probe can choose reliably. Simulation-first; hardware only as a registered addendum.

## North-star question

> Under a fixed quantum-execution budget, when is runtime evidence sufficient to decide whether to trust, correct, or withhold a quantum decision?

## Current status

Planning only. No experiment has been run, no protocol has been independently registered, and no hardware execution is authorized.

The full scientific rationale and gate criteria are in [the research program plan](docs/research_program_plan_v0.md). The public task hierarchy, research branches, subtasks, and extension tracks are in [the research work plan](docs/schedule/research_schedule_v1.md).

The problem-oriented reading queue, verification rules, and source ledger are in [docs/literature/](docs/literature/README.md).

M2 freezes the synthetic E2 and RC semantics in the [E2 semantics note](docs/theory/e2_semantics_v1.md), [RC construction](docs/theory/rc_construction_v1.md), and [conditional likelihood](docs/theory/conditional_likelihood_v1.md). The corrected [frame-covariance note](docs/theory/gate1_frame_covariance_draft.md) proves the local Pauli identity and the zero-I1 statement at `phi=0`; it contains no Gate-1 result.

M3 freezes the pre-computation [Gate 1 mathematical specification](docs/theory/gate1_math_spec_v1.md) and [Gate 1 design lock](docs/freeze/gate1_design_lock.md). These are protocol artifacts, not Gate 1 results; the committed SHA-256 manifest is an internal lock rather than an independent preregistration.

Gate 1 was then executed once against that lock. [Gate 1A](docs/results/gate1a_report.md) failed under the deployable unknown-response nuisance model; the prespecified [Gate 1B](docs/results/gate1b_report.md) P-amp fallback passed its analytic and exact-noiseless criteria and is the sole sensor routed to Gate 2. These are synthetic/noiseless findings, not noisy-simulation or hardware evidence.

Main Task 1 is recorded in the [decision-problem contract](docs/contracts/decision_problem_v1.md) and [three-action theory draft](docs/theory/three_action_theory_v1.md). D1–D3 are decided; theorem proofs remain project drafts unless stated otherwise.
