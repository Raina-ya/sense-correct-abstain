# Source ledger

The verification states for the eight inherited sources are copied without
upgrade from the research plan. Links below point to primary publisher or arXiv
pages when located. Notes are routing notes, not literature-review conclusions.

## Inherited core sources

| Priority | Source and link | Canonical verification state | Questions | What must be checked before use |
|---:|---|---|---|---|
| 1 | Wallman & Emerson, 2016, *Physical Review A* 94, 052325, [publisher](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.052325) | **verified previously; relevant full text reread 2026-11-20** | Q1, Q3 | Exact easy/hard-cycle construction and gate-dependence boundary are summarized in `rc_assumption_table.md`; application to the proposed decomposition remains open. |
| 2 | Vyas, 2026, *Label and Recover Coherent Errors: Randomized Compiling Does Not Destroy Coherent-Error Information*, arXiv:2607.26756, [arXiv](https://arxiv.org/abs/2607.26756) | **full text read 2026-11-20; Fisher chain rule independently checked; code/hardware not reproduced** | Q2, Q3 | The likelihood and oracle audit are in `notes/vyas_2026.md`. Its `s theta` model does not by itself establish label sensitivity to logical-angle `epsilon`. |
| 3 | Santos, Bar & Uzdin, 2024, *npj Quantum Information* 10, 100, [publisher](https://www.nature.com/articles/s41534-024-00889-8) | **abstract checked only** | Q4, Q7 | Which controllable drive signs PST requires; which over/under-rotations it does not suppress; resulting channel class; circuit and twirl cost. |
| 4 | Bar, Santos & Uzdin, 2026, Layered KIK, DOI 10.1038/s41534-026-01207-0, [publisher](https://www.nature.com/articles/s41534-026-01207-0) | **abstract checked only** | Q4, Q7 | Dynamic-circuit contribution versus inherited Adaptive-KIK properties; inverse implementation; applicability to logical cost rotations; resource overhead. |
| 5 | Henao, Santos & Uzdin, 2023, *npj Quantum Information* 9, 120, [publisher](https://www.nature.com/articles/s41534-023-00785-7) | **abstract checked only** | Q4, Q7 | Survival-probability reference, pulse-based inverse assumptions, time-local noise requirement, calibration example, and how RC is integrated. |
| 6 | Winick et al., 2022, arXiv:2212.07500, [arXiv](https://arxiv.org/abs/2212.07500) | **full text read 2026-11-20; proofs not independently reproduced** | Q1 | Assumptions, non-Markovian scope, single/many-randomization distinction, and adversarial failure mechanism are summarized in `rc_assumption_table.md`. |
| 7 | Kurita et al., 2023, *Quantum* 7, 1184, [publisher](https://quantum-journal.org/papers/q-2023-11-20-1184/) | **abstract checked only** | Q7 | Coherent-noise models, VQE setting, RC construction, ZNE cost, and whether the result concerns mitigation rather than parameter sensing. |
| 8 | Zhang, Seshadri & Knill, 2026, arXiv:2602.08114, [arXiv](https://arxiv.org/abs/2602.08114) | **abstract fragment seen only** | Q8 | Non-i.i.d. model, spot-check allocation, certificate target, finite-sample guarantee, and applicability to calibration drift. Defer to Chapter 4. |

## Comparator candidates

These sources were not part of the inherited eight. They remain **unverified**
for project claims until a dedicated note is completed, even where an official
metadata or abstract page has been located.

| Candidate | Verification state | Why it may matter | Required check |
|---|---|---|---|
| Czarnik et al., 2021, *Error mitigation with Clifford quantum-circuit data*, *Quantum* 5, 592 | **unverified** | Original CDR source behind the predecessor's P2 family. | Training/reference construction, transfer assumption, classical cost, and failure when the target and Clifford surrogate respond differently to angle-dependent noise. |
| Lowe et al., 2021, *Unified approach to data-driven quantum error mitigation*, *Physical Review Research* 3, 033098, [publisher](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.033098) | **unverified** | Frames CDR and variable-noise CDR in a common data-driven model. | Whether any theorem or diagnostic supports using one deterministic twin as an `epsilon` sensor; do not infer this from benchmark improvements. |
| Project predecessor P2, frozen protocol at predecessor commit `cd5e576` | **locally located; audit file not yet present in this repo** | Direct project comparator: nearest-Clifford twin, two extra circuits, and the twin's own classically computable ideal gap. | Reconcile `docs/audits/predecessor_e2_audit.md`; distinguish alarm visibility from estimating `epsilon`; charge reference computation and shots; state target-to-twin transfer failure. |

## Working comparison fields for Gate 1 sensors

Do not fill a cell from analogy. Every populated cell needs a source note or a
project derivation.

| Method | Runtime observable | Known reference | Extra circuits/depth | Estimates `epsilon`? | Deployable without target ideal? | Primary unresolved issue |
|---|---|---|---|---|---|---|
| Gate 1A RC labels | Label--outcome contrasts | None allowed for the pass criterion | Intended zero extra circuit families; shots still charged | Open | Open | Whether efficient information for `epsilon` survives when the ideal response is nuisance and `phi=0`. |
| Gate 1B P-amp | Frozen repeated/echo response | To be frozen | To be frozen before Gate 1A runs | Intended | Open | Identifiability, aliasing, depth/noise cost, and novelty relative to known amplification. |
| Predecessor P2 | Twin observed gap minus twin ideal gap | Clifford twin's ideal gap, not target ideal | Two extra circuits in predecessor protocol | Not established; predecessor used an alarm score | Yes under predecessor definition | Transfer from twin bias to target decision bias under angle-dependent E2. |
| Vyas labeled estimator | To be extracted from full text | To be extracted | Abstract claims no extra circuit cost; not yet checked | Abstract says coherent parameters | Not established for QAOA E2 | Applicability of its error and circuit model to logical-angle cost rotations. |
| PST / KIK family | Method-specific expectation or survival data | Method-specific | To be extracted | Not assumed | Open | These are mitigation/calibration comparators, not automatically E2 sensors. |

## Next verification notes to create

1. `notes/wallman_emerson_2016.md`: theorem assumptions and gate-dependence
   boundary.
2. `notes/vyas_2026.md`: likelihood, Fisher decomposition, oracle audit, and
   circuit-model match.
3. `notes/p2_cdr_comparator.md`: predecessor P2 versus CDR versus P-amp.
4. `notes/pst_kik_comparator.md`: controlled sign/inverse, target error, and
   cost comparison.
