# Proof review trail

Chronological record of how each piece of project mathematics was drafted,
reviewed, and accepted. All files are in this folder unless noted. The owner's
review notes are byte-identical to the files supplied by the owner, and their
SHA-256 hashes are in `results/errata/errata_manifest_v3.sha256` through
`errata_manifest_v6.sha256`. This index is a living document and is not
hashed.

| Round | Subject | Draft (Claude) | Owner review | Outcome | Erratum |
|---|---|---|---|---|---|
| 1 | Lemma S1′, Gate 1A corollary, Lemma B | `docs/errata/E006_audit_of_9201ba9.md` §2–§3; typeset as [`S1prime_B_review_draft.pdf`](S1prime_B_review_draft.pdf) ([`.tex`](S1prime_B_review_draft.tex)) | [`S1prime_B_rigorous.pdf`](S1prime_B_rigorous.pdf) ([`.tex`](S1prime_B_rigorous.tex)) | accept with corrections (non-nesting of N-q and N-free; translation construction; explicit nuisance paths; Gibbs characterization; sharp N-q interval; Lemma B assumptions and sharp 1/2) | [E007](../errata/E007_owner_review_lemmas.md) |
| 2 | A4–A6: T1, C1, C2, L1, T2, D1, P2 | [`three_action_theory_v1.md`](three_action_theory_v1.md) | [`A4_A6_rigorous.pdf`](A4_A6_rigorous.pdf) ([`.tex`](A4_A6_rigorous.tex)) | statements unchanged; implicit assumptions made explicit; Example E1 gap corrected; Example E2 status updated | [E008](../errata/E008_owner_review_A4_A6.md) |
| 3 | Extension S1″ (per-context shared response; visibility/offset) | E007 §3.2; typeset as [`S1doubleprime_review_draft.pdf`](S1doubleprime_review_draft.pdf) ([`.tex`](S1doubleprime_review_draft.tex)) | [`S1doubleprime_rigorous.pdf`](S1doubleprime_rigorous.pdf) ([`.tex`](S1doubleprime_rigorous.tex)) | accept with corrections (`phi' != 0` at both exceptional points; generality; box feasibility) | [E009](../errata/E009_owner_review_S1doubleprime.md) |

**Precedence.** Where a draft and a later review differ, the review and its
erratum govern. The drafts are kept only as the record of what was reviewed.

**Current state.** No draft proof remains open (E009 §4). The step
"nonunique profile maximizer ⇒ Gate 1A FAIL" and the readings of spec §5.3
are specification questions. The Chow (1970) rule form and the Tsybakov lemma
locations are unverified attributions; the corresponding proofs are
self-contained.

**Note on round 1.** The draft PDF typesets E006 §2–§3 without changing its
content. It was produced on 2026-11-21 and given to the owner for printing
before the owner's review. It was added to the repository afterwards, to
complete this record. Its `.tex` source is the exact file that produced the
PDF.
