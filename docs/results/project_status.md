# Project status (authoritative, living document)

**Updated:** 2026-11-21, after the audit of `9201ba9` (E006) and the MT7
synthesis.

This is a **living document** (E006 §6). Its `9201ba9` snapshot is hash-checked
against git history; this working copy may change. The status tables inside
the M3-locked program plan and work plan are frozen at M3 and are **stale**.

## Route taken

| Step | Outcome | Record | Errata |
|---|---|---|---|
| M1 contracts | done | `docs/contracts/decision_problem_v1.md`, `docs/theory/three_action_theory_v1.md` | — |
| M2 semantics | frozen | `docs/theory/e2_semantics_v1.md`, `rc_construction_v1.md`, `conditional_likelihood_v1.md` | — |
| M3 Gate 1 lock | frozen (design documents only; code not locked) | `docs/freeze/gate1_design_lock.md` | E005 |
| Gate 1A (RC labels) | **FAIL**. Original basis invalid (hard-coded entries); corrected basis is Lemma S1′ plus the frozen recovery rule. Nuisance-class ambiguity disclosed. | `docs/results/gate1a_report.md` | E001, **E006 §2** |
| Gate 1B (P-amp) | **PASS** in the noiseless synthetic model; only a 0.7% visibility margin; visibility attenuation untested | `docs/results/gate1b_report.md` | E002 |
| Gate 2 | **formal PASS; practical conclusion narrowed** (wording below) | `docs/results/gate2_report.md` | E003, **E006 §3–4** |
| Gate 3 | **FAIL**, under both the frozen and the corrected estimand (the latter a post-lock reanalysis) | `docs/results/gate3_gate4_report.md` | E004 |
| Gate 4 | PASS (moot) | same | E004 |
| Stop rule | **stopped after M6 → MT7** | — | — |
| MT7 | **complete with declared open reviews.** 7.1 claim ledger, 7.2 report, 7.3 reproducibility package, and 7.4 scoped citation/novelty audit are complete. | see below | — |

**Gate 2 (authoritative wording):**

> Gate 2 formally passed its prespecified, internally locked rule, but the
> diagnostic did not demonstrate useful selective prediction of which units
> benefit from correction. Its precision was 0.093 versus a base rate of
> 0.077, and much of the apparent gain came from excluding large-gap units.
> Therefore Gate 2 is retained as a formal PASS but not interpreted as
> evidence of operationally useful benefit selection.

## MT7 deliverables

- Claim ledger: [`../claim_ledger.md`](../claim_ledger.md). It lists what may
  and may not be claimed.
- Technical report draft: [`../../paper/technical_report_v1.md`](../../paper/technical_report_v1.md)
- Reproducibility package: [`../reproducibility.md`](../reproducibility.md)
- Citation and novelty audit:
  [`../literature/novelty_claim_draft.md`](../literature/novelty_claim_draft.md),
  section "MT7.4 citation and novelty audit".
- Future-lock policy: [`../protocols/lock_template_v2.md`](../protocols/lock_template_v2.md)

## What is and is not authorized

- **Allowed:** later owner review of the draft proofs (Lemma S1′, Lemma B,
  theory note) and correction of explicitly unverified citation attributions.
- **Not allowed:** M7 registration, a holdout, any adaptive-policy or
  "method works" claim, any rerun or redesign of Gates 1–4 presented as the
  same study, calling internal recomputation third-party validation, or any
  hardware claim.

## Open owner items

1. Review the Lemma S1′ and Lemma B proofs when available; until then they
   remain proved drafts and are not represented as owner-approved.
2. Verify the exact Chow rule attribution and Tsybakov lemma numbering if the
   full texts become available.
3. Use lock template v2 for any new study.
