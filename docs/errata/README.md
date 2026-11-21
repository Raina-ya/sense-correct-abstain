# Post-lock errata (2026-11-21)

These errata record defects found in a post-lock audit of M2–M6
([`../audits/m2_m6_post_lock_audit.md`](../audits/m2_m6_post_lock_audit.md)).

## Policy

1. **Frozen files are never edited.** Every file listed in a lock or artifact
   manifest (`docs/freeze/*_manifest.sha256`, `results/*_artifact_manifest.sha256`)
   is left byte-for-byte unchanged, including the frozen program plan, work
   plan, contract, specifications, reports, and result JSON files.
   `python tools/check_errata_artifacts.py` verifies this.
2. **No frozen verdict is changed, rerun, or rescued.** Each erratum states
   whether the frozen verdict stands and on what basis.
3. **Evidence classes stay separate.** Every new quantity is labeled as one of:
   - *analytic* (a proof);
   - *deterministic check* (exact recomputation of a frozen-spec quantity or a
     semantic identity);
   - *post-hoc / exploratory* (specified after a result was known; it can
     neither support nor overturn a verdict).
4. **No new research data.** The audit only reads frozen artifacts, evaluates
   frozen circuits deterministically, or recomputes frozen per-unit functions
   to check provenance. Recomputed rows are not saved.
5. Errata outputs are in `results/errata/`, hashed in
   `results/errata/errata_manifest.sha256`.

## Index

| ID | Scope | Severity | Frozen verdict | Status after erratum |
|---|---|---|---|---|
| [E001](E001_gate1a.md) | Gate 1A: I3, recovery, and controls hard-coded; I1 mislabeled; pairs not at budget | critical | FAIL | **Stands.** Basis replaced by Lemma S1 (analytic) plus the frozen recovery rule |
| [E002](E002_gate1b.md) | Gate 1B: recovery was an inverse-crime algebra check; transfer by construction | major | PASS | **Stands** within the synthetic noiseless model; circuit semantics now checked |
| [E003](E003_gate2.md) | Gate 2: plan deviations, weak selectivity, noisy labels, structurally blind P2 | critical (interpretation) | PASS | **Stands formally**; the decision-relevance claim is narrowed |
| [E004](E004_gate34.md) | Gate 3: selection-conditioning defect in the N-path loss; power assessed too late | major | Gate 3 FAIL, Gate 4 PASS | **Both stand.** Gate 3 FAIL is robust to the corrected estimand |
| [E005](E005_governance.md) | Locks excluded analysis code; stale locked status; no environment pin; platform-dependent artifacts | major | — | Remedies recorded; nothing retroactively relocked |

## Net effect on the project route

The route is unchanged: Gate 1A FAIL → Gate 1B PASS (P-amp) → Gate 2 PASS →
**Gate 3 FAIL → Stop after M6 → MT7 synthesis.**

No confirmatory registration (M7) or holdout (M8) is authorized. The current
status is in [`../results/project_status.md`](../results/project_status.md).
