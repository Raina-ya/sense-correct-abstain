# Problem-oriented literature library

**Status:** living research index, started 2026-11-20. This is not a protocol,
preregistration, or claim of novelty. A source's presence here does not mean
that its full text or derivations have been checked.

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

1. Reconcile the predecessor audit into the repository. The user reports an
   audit at `docs/audits/predecessor_e2_audit.md` tied to predecessor commit
   `cd5e576`, but that file was not present in this checkout when this library
   was created. Until it is available, its conclusions are user-provided audit
   summary, not locally reverified evidence.
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
