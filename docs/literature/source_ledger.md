# Source ledger

The verification states for the eight inherited sources are copied without
upgrade from the research plan. Links below point to primary publisher or arXiv
pages when located. Notes are routing notes, not literature-review conclusions.

## Inherited core sources

| Priority | Source and link | Canonical verification state | Questions | What must be checked before use |
|---:|---|---|---|---|
| 1 | Wallman & Emerson, 2016, *Physical Review A* 94, 052325, [publisher](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.94.052325) | **verified previously; relevant full text reread 2026-11-20** | Q1, Q3 | Exact easy/hard-cycle construction and gate-dependence boundary are summarized in `rc_assumption_table.md`; application to the proposed decomposition remains open. |
| 2 | Vyas, 2026, *Recovering Coherent Errors from Randomized-Compiling Labels* (title as on the arXiv abstract page, checked 2026-11-20; an earlier entry gave a different title, to be checked against the PDF), arXiv:2607.26756, [arXiv](https://arxiv.org/abs/2607.26756) | **full text read 2026-11-20 (by AI agent; not yet confirmed by the project owner); Fisher chain rule independently checked; code/hardware not reproduced** | Q2, Q3 | The likelihood and oracle audit are in `notes/vyas_2026.md`. Its `s theta` model does not by itself establish label sensitivity to logical-angle `epsilon`. |
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
| Czarnik et al., 2021, *Error mitigation with Clifford quantum-circuit data*, *Quantum* 5, 592, DOI 10.22331/q-2021-11-26-592 | **bibliographic fields verified in the predecessor library; content unverified for this project** | Original CDR source behind the predecessor's P2 family. | Training/reference construction, transfer assumption, classical cost, and failure when the target and Clifford surrogate respond differently to angle-dependent noise. |
| Lowe et al., 2021, *Unified approach to data-driven quantum error mitigation*, *Physical Review Research* 3, 033098, [publisher](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.3.033098) | **bibliographic fields verified in the predecessor library; content unverified for this project** | Frames CDR and variable-noise CDR in a common data-driven model. | Whether any theorem or diagnostic supports using one deterministic twin as an `epsilon` sensor; do not infer this from benchmark improvements. |
| Project predecessor P2, frozen protocol at predecessor commit `cd5e576` | **audited: `docs/audits/predecessor_e2_audit.md` (commit `0aa627b`) and review** | Direct project comparator: nearest-Clifford twin, two extra circuits, and the twin's own classically computable ideal gap. | Reconcile `docs/audits/predecessor_e2_audit.md`; distinguish alarm visibility from estimating `epsilon`; charge reference computation and shots; state target-to-twin transfer failure. |

## Sources added 2026-11-20 (Claude; metadata and abstract only)

Full rows are in `library.csv`. None of these has been read in full.

| Key | Source | Why added |
|---|---|---|
| `kimmel2015rpe` | Kimmel, Low & Yoder, *Phys. Rev. A* 92, 062315 (2015), arXiv:1502.02677 | Robust phase estimation of amplitude errors: P-amp's closest known construction. Erratum: *Phys. Rev. A* 104, 069901 (2021). |
| `rudinger2017rpe` | Rudinger, Kimmel, Lobser & Maunz, *Phys. Rev. Lett.* 118, 190502 (2017) | Experimental RPE. |
| `russo2021rpe` | Russo, Kirby, Rudinger, Baczewski & Kimmel, *Phys. Rev. A* 103, 042609 (2021), arXiv:2011.13442 | Consistency tests for RPE: sensor-level "do not trust" rule. |
| `higgins2009` | Higgins et al., *New J. Phys.* 11, 073023 (2009) | Non-adaptive Heisenberg-limited phase estimation underlying RPE. |
| `ware2021pfr` | Ware et al., *Phys. Rev. A* 103, 042604 (2021) | Hardware Pauli-frame randomization with GST. |
| `kelly2018dag` | Kelly et al., arXiv:1803.03226 (2018) | Cost and structure of recalibration (the C action). |
| `proctor2020drift` | Proctor et al., *Nat. Commun.* 11, 5396 (2020) | Drift detection (Chapter 4). |
| `mitarai2018`, `schuld2019` | *Phys. Rev. A* 98, 032309 (2018); *Phys. Rev. A* 99, 032331 (2019) | Parameter-shift structure of the response (nuisance class). |
| `chow1970` | Chow, *IEEE Trans. Inf. Theory* 16, 41–46 (1970) | Optimal reject rule. |
| `herbei2006` | Herbei & Wegkamp, *Can. J. Stat.* 34, 709–721 (2006) | Reject option with explicit cost. |
| `howard1966voi` | Howard, *IEEE Trans. Syst. Sci. Cybern.* SSC-2 (1966) | Value of information; page range unconfirmed. |
| `vandervaart1998` | van der Vaart, *Asymptotic Statistics*, Cambridge (1998) | Efficient information with nuisance (I3). |
| `tsybakov2009` | Tsybakov, *Introduction to Nonparametric Estimation*, Springer (2009) | Minimax lower bounds, Le Cam's method. |
| `mckay2017vz` | McKay et al., *Phys. Rev. A* 96, 022330 (2017), arXiv:1612.00858 | Virtual Z gates: a physical `RZ` may carry no angle error, so E2 needs another carrier. |

## Working comparison fields for Gate 1 sensors

Do not fill a cell from analogy. Every populated cell needs a source note or a
project derivation.

| Method | Runtime observable | Known reference | Extra circuits/depth | Estimates `epsilon`? | Deployable without target ideal? | Primary unresolved issue |
|---|---|---|---|---|---|---|
| Gate 1A RC labels | Label--outcome contrasts | None allowed for the pass criterion | Intended zero extra circuit families; shots still charged | Open | Open | Whether efficient information for `epsilon` survives when the ideal response is nuisance and `phi=0`. |
| Gate 1B P-amp | X/Y outcomes of 6 repetition and 3 echo circuits (plan §3.4.1) | Known single-qubit phases | 18 settings in `f*N`; depth up to 32 blocks; numbers frozen in week 4 | Intended | Yes by construction (own reference only) | Aliasing, depth/noise cost, target-context transfer, and novelty relative to known amplification. |
| Predecessor P2 | Twin observed gap minus twin ideal gap | Clifford twin's ideal gap, not target ideal | Two extra circuits in predecessor protocol | Used as an alarm; a first-order estimate is possible in principle (see comparison note) | Yes under predecessor definition | Transfer from twin bias to target decision bias under angle-dependent E2. |
| Vyas labeled estimator | Label--outcome correlation `E[s b]` | Visibility `v` from benchmarking or fitted (see note) | No extra circuit families; benchmarking cost for `v` not free | Yes for its `s theta` model, which maps to the project's additive `phi` | Not for QAOA: the analogue of `v` is the unknown target-response slope | Whether any angle-proportional term acquires a label-dependent sign under the frozen placement. |
| PST / KIK family | Method-specific expectation or survival data | Method-specific | To be extracted | Not assumed | Open | These are mitigation/calibration comparators, not automatically E2 sensors. |

## Next verification notes to create

1. Done as `notes/wallman_winick_reading.md` and `rc_assumption_table.md`.
2. Done as `notes/vyas_2026.md` (agent reading; owner confirmation pending).
3. Done as `p2_cdr_pamp_comparison.md`; CDR sources still unverified.
4. Open: `notes/pst_kik_comparator.md` (controlled sign/inverse, target error,
   and cost comparison).
5. Done at metadata/abstract level: robust phase estimation sources and
   `notes/phase_estimation_pamp_boundary.md`. Full-text reading of
   `kimmel2015rpe` (with erratum) and `russo2021rpe` remains open.
6. Open: full-text reading of `scavino2026` (decision kernels for QEM), the
   closest decision-level QEM work, before any novelty wording is frozen.
