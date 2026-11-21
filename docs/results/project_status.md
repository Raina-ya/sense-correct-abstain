# Project status (authoritative)

**Updated:** 2026-11-21, after the post-lock audit.

The status tables inside the M3-locked program plan and work plan are frozen at
M3 and are **stale**. They are not edited, because they are hashed by the M3
lock (erratum E005 §2). This file is the current status.

## Route taken

| Step | Outcome | Record | Erratum |
|---|---|---|---|
| M1 contracts | done | `docs/contracts/decision_problem_v1.md`, `docs/theory/three_action_theory_v1.md` | — |
| M2 semantics | frozen | `docs/theory/e2_semantics_v1.md`, `rc_construction_v1.md`, `conditional_likelihood_v1.md` | — |
| M3 Gate 1 lock | frozen (design documents only; code not locked) | `docs/freeze/gate1_design_lock.md` | E005 |
| Gate 1A (RC labels) | **FAIL**, which stands; valid basis is Lemma S1 | `docs/results/gate1a_report.md` | **E001** |
| Gate 1B (P-amp) | **PASS** (synthetic, noiseless, known-reference) | `docs/results/gate1b_report.md` | E002 |
| Gate 2 (decision relevance) | **PASS** formally; claim narrowed | `docs/results/gate2_report.md` | **E003** |
| Gate 3 (net value) | **FAIL**; robust to the corrected estimand | `docs/results/gate3_gate4_report.md` | **E004** |
| Gate 4 (non-degeneracy) | PASS (moot after the Gate 3 failure) | same | E004 |
| Route | **Stop after M6 → MT7 synthesis** | — | — |

## What this authorizes

- **Allowed:** MT7 synthesis (claim ledger, report, reproducibility package),
  reporting the resource/value boundary, the RC-label negative
  identifiability result, and the three-action theory.
- **Not allowed:** M7 registration, a confirmatory holdout, any adaptive-policy
  claim, any rerun or redesign of Gates 1–4 presented as the same study, or
  any hardware claim.

## Claims that are and are not supported

| Supported (with stated scope) | Not supported |
|---|---|
| Under the synthetic compiled-angle model, retained RC labels carry zero deployable information about `epsilon` at `phi = 0`, so `epsilon` is not identified there (analytic, E001 Lemma S1). | That RC labels cannot sense `epsilon` on hardware, or under a structured response model. |
| The frozen P-amp design identifies `(epsilon, phi)` from its own known reference in the noiseless synthetic model (E002). | P-amp robustness to visibility loss, drift, or context mismatch; any P-amp vs P2 superiority. |
| The frozen Gate 2 rule met its frozen criterion; it flags almost all non-null, not-large-gap units (E003). | That the rule predicts which units benefit from correction. |
| No detectable net value of the deployable three-action policy over always-correct at the frozen budget; the design had about zero power (E004). | Any positive policy value. |

## Open owner items

1. Review Lemma S1 (E001) and the `B_hat` first-order statement (E003 §6).
2. Decide how MT7 reports the Gate 2 pass: the narrowed wording in E003 §8 is
   the strictest defensible statement.
3. Adopt the future-lock requirements in E005 §5 before any new study.
