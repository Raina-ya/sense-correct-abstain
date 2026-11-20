# Problem-oriented literature library

**Status:** living research index, started 2026-11-20. This is not a protocol,
preregistration, or claim of novelty. A source's presence here does not mean
that its full text or derivations have been checked.

## Library at a glance (updated 2026-11-20)

The machine-readable library is [`library.csv`](library.csv): 62 entries.

- 8 inherited core sources, with the canonical states from the research plan;
- 40 entries reused from the predecessor's verified library (bibliographic
  fields verified there; relevance notes for this project are new and are
  routing notes, not content checks);
- 14 new entries whose bibliographic metadata and abstract were checked on
  2026-11-20 (no full text read).

Each row records the questions it serves (Q1–Q8 in `problem_matrix.md`), its
role, verification state, who checked it, why it matters, and its main
limitation for this project.

| Question | Entries | Keys |
|---|---:|---|
| Q1 | 5 | `wallman2016`, `winick2022`, `knill2005`, `hashim2021`, `ware2021pfr` |
| Q2 | 12 | `vyas2026`, `erhard2019`, `flammia2020pauli`, `chen2023learnability`, `nielsen2021gst`, `magesan2011`, `imbens2004`, `tamer2010`, `lipsitch2010`, `mitarai2018`, `schuld2019`, `vandervaart1998` |
| Q3 | 5 | `wallman2016`, `vyas2026`, `nielsen2021gst`, `farhi2014`, `zhou2020qaoa` |
| Q4 | 9 | `santos2024pst`, `bar2026lkik`, `henao2023akik`, `cai2023`, `proctor2022mirror`, `kimmel2015rpe`, `rudinger2017rpe`, `russo2021rpe`, `higgins2009` |
| Q5 | 4 | `czarnik2021`, `lowe2021`, `aaronson2004`, `gidney2021stim` |
| Q6 | 27 | `chen2023learnability`, `kueng2016`, `sanders2016`, `takagi2022`, `takagi2023`, `tsubouchi2023`, `quek2024`, `cai2023`, `govia2025`, `prodius2026`, `lecam1973`, `imbens2004`, `tamer2010`, `bechhofer1954`, `kimnelson2006`, `chen2000ocba`, `garivier2016`, `kaufmann2016`, `ghosh2017`, `scavino2026`, `koster2026`, `russo2021rpe`, `kelly2018dag`, `chow1970`, `herbei2006`, `howard1966voi`, `tsybakov2009` |
| Q7 | 9 | `santos2024pst`, `bar2026lkik`, `henao2023akik`, `kurita2023`, `hashim2021`, `sarovar2020`, `temme2017`, `kandala2019`, `ware2021pfr` |
| Q8 | 4 | `zhang2026spot`, `wald1945`, `howard2021`, `proctor2020drift` |

Thematic notes:

- [`notes/vyas_2026.md`](notes/vyas_2026.md): label likelihood, Fisher identity, parameter mapping, testability versus estimability.
- [`notes/wallman_winick_reading.md`](notes/wallman_winick_reading.md) and [`rc_assumption_table.md`](rc_assumption_table.md): RC assumptions.
- [`notes/phase_estimation_pamp_boundary.md`](notes/phase_estimation_pamp_boundary.md): robust phase estimation and the P-amp novelty boundary.
- [`notes/decision_theory_reject_option.md`](notes/decision_theory_reject_option.md): reject option, value of information, ranking and selection.
- [`notes/identification_and_information.md`](notes/identification_and_information.md): efficient information with nuisance, lower bounds, parameter-shift structure.
- [`p2_cdr_pamp_comparison.md`](p2_cdr_pamp_comparison.md) and [`novelty_claim_draft.md`](novelty_claim_draft.md).

## Purpose

This library supports four decisions that must be made before Gate 1 is run:

1. whether an RC-label contrast contains deployable information about the
   multiplicative error `epsilon`, rather than information available only from
   an ideal response curve;
2. which randomized-compiling assumptions survive angle-dependent easy-gate
   noise and label absorption;
3. whether the frozen P-amp fallback is scientifically distinct from existing
   phase-amplification, echo, KIK, and Clifford-reference methods; and
4. whether a sensed parameter can support a fixed-budget decision among no
   action, recalibration, and abstention.

The unit of organization is a **research question**, not a paper. Start with
[`problem_matrix.md`](problem_matrix.md), then use
[`source_ledger.md`](source_ledger.md) to find the evidence and its verification
boundary.

## Goals

- Make oracle dependence, observable data, and resource cost explicit for every
  method considered for Gate 1A or Gate 1B.
- Keep RC noise tailoring, coherent-parameter sensing, error amplification, and
  action selection as separate claims.
- Record negative scope conditions and failure modes, not only positive results.
- Preserve the verification level supplied by the research plan until the
  source has actually been checked at the stronger level.
- Give Part 1 a bounded reading queue rather than an open-ended bibliography.

## Non-goals

- Collecting every QEM, calibration, or quantum-metrology paper.
- Treating citation count, publication venue, or a matching keyword as evidence
  that a method applies to E2.
- Calling an abstract check a derivation check.
- Treating a classically computable Clifford-twin reference as the unknown
  target's ideal value; both are oracle-related fields, but they are not the
  same field.
- Replacing the frozen Gate 1A/1B route after observing results.

## Who performed a check (added 2026-11-20)

Several notes record full-text reading performed by an AI agent. Each ledger
entry should state who read the source (agent or project owner) and on what
date. An agent's reading is a working note; the project owner confirms it before
any claim enters the paper. This does not change the state names below.

## Terminology (added 2026-11-20)

`epsilon` is an angle-proportional error; `phi` an additive, gate-independent
phase. Where the error acts is a separate choice: logical-angle model,
compiled-angle model, or control model (research plan §3.3). Avoid
"logical-angle `epsilon`".

## Verification states

Use only these states in the ledger:

| State | Meaning |
|---|---|
| `verified` | The cited bibliographic fact and the project-relevant claim were checked against the source at the level stated in the note. |
| `full text read` | The relevant sections, assumptions, and limitations were read; this does not imply reproduction of a proof. |
| `derivation checked` | The project-relevant derivation was reconstructed or independently checked. |
| `abstract checked only` | Only the abstract or publisher summary was checked. |
| `abstract fragment seen only` | Less than a complete abstract was previously available. |
| `unverified` | Candidate source; do not cite a substantive claim from it yet. |

Upgrades require a dated note stating which sections/equations were checked and
what claim the check supports. Discovery during a web search does not silently
upgrade the canonical state.

## Evidence fields required for every core source

Each core entry records:

- research question and proposed use;
- observable data and whether labels are retained;
- ideal, structural, or calibration information required;
- circuit, shot, depth, and classical-computation costs when reported;
- assumptions and explicit failure conditions;
- evidence type: analytic, noiseless simulation, noisy simulation,
  device-parameter simulation, or hardware-derived;
- relation to Gate 1A, Gate 1B, P2, Gate 2, or later chapters;
- verification state and next check.

`fake backend` evidence is always recorded as device-parameter simulation, not
hardware evidence.

## Bounded Part 1 workflow

1. Reconcile the predecessor audit into the repository. Done: the audit is in
   `docs/audits/predecessor_e2_audit.md` (commit `0aa627b`), with a review in
   `docs/audits/predecessor_e2_audit_review.md`.
2. Read Wallman--Emerson and Winick et al. for the exact easy/hard-cycle and
   gate-dependence assumptions.
3. Read Vyas in full and reconstruct the label--outcome likelihood. Check
   whether its Fisher-information statement assumes a known response,
   calibration circuit, or parameterization absent from QAOA E2.
4. Compare P-amp with P2/CDR, pseudo-twirling, Adaptive KIK, and Layered KIK.
   Record observable, reference value, amplification mechanism, and charged
   cost separately.
5. Only then write the novelty sentence and the Gate 1 negative controls.

Current synthesis documents:

- [`rc_assumption_table.md`](rc_assumption_table.md)
- [`notes/vyas_2026.md`](notes/vyas_2026.md)
- [`p2_cdr_pamp_comparison.md`](p2_cdr_pamp_comparison.md)
- [`novelty_claim_draft.md`](novelty_claim_draft.md)

Stop expanding the queue when every Gate 1 assumption and comparator has at
least one primary source and an explicit unresolved question. New papers enter
only if they can change a gate criterion, comparator, or novelty claim.
