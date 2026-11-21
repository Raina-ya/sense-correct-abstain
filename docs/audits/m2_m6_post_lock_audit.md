# Post-lock audit of M2–M6 (2026-11-21)

**Auditor:** Claude, at the project owner's request, reviewing as a
postdoc, examiner, or referee would.
**Commit audited:** `017bc76` (Gate 3/4 run).
**Method:** read every M2–M6 document, lock, runner, module, test, and result;
reran all lock, artifact, and semantic checkers and all tests; independently
re-derived the RC label table and the P-amp resource bound; ran the
deterministic audit tools listed below. No frozen file was edited and no
verdict was rerun.

## Verdict

The project's change-control discipline is visible and largely honest: locks,
refusal-to-rerun guards, explicit nonevaluable records, and claim boundaries.
The M2 mathematics is correct. However:

- one gate verdict was asserted rather than computed (Gate 1A);
- one gate's pass carries little evidential weight (Gate 2);
- one gate used a mis-specified estimand (Gate 3); and
- no lock covered analysis code.

None of these changes the project route, which ends at Gate 3 FAIL → MT7.
Each is now recorded as an erratum.

## Findings

| Severity | Finding | Erratum |
|---|---|---|
| Critical | Gate 1A: I3 rank, profile recovery, verdict, and five control statuses are hard-coded literals; the specification-required computations were not run. | E001 §1 |
| Critical | Gate 1A: the reported "I1" is a known-response (oracle) quantity, and the single-angle control mismatch is recorded as "Match". | E001 §1 |
| Critical (interpretation) | Gate 2: the rule predicts positive for 79% of units (precision 0.093 vs base rate 0.077). Its gain over a constant baseline comes from excluding large-gap units; labels are Monte Carlo coin flips at intermediate accuracy. | E003 §2–4 |
| Major | Gate 2 deviates from the program plan: no uncertainty bound, no power analysis, resolution-based margin. | E003 §1 |
| Major | The frozen Gate 1A nuisance class is ambiguous ("saturated" vs "local first-order"); the two readings give different I3. | E001 §3 |
| Major | Gate 3: the N-path loss ignores selection on the same shots. Corrected-estimand reanalysis: `Delta_V` 0.000237, lower bound −0.000625 (FAIL is robust). | E004 §1 |
| Major | Gate 3/4 power (0.0004) was computed in the same run as the evaluation, so no futility decision point existed. | E004 §3 |
| Major | No lock hashed runner code; Gate 1A results were committed about 22 hours after the run. | E005 §1 |
| Major | Gate 1B recovery was an inverse-crime algebra check; sensor–target transfer holds by construction; the resource margin is 0.7% (fails for visibility < 0.9926). | E002 |
| Major | The P2 comparator is structurally blind on 3300 of 6600 Gate 2 units (twin mixer rounds to identity). | E003 §5 |
| Major | Finite-separation pairs were reported per shot. At budget, the two-point error lower bound is 0.185–0.232, not about 0.498. | E001 §4 |
| Moderate | Artifacts are not bit-reproducible across platforms (416 and 31 units differ); verdict-level results are identical. No environment pin existed. | E005 §4 |
| Moderate | Locked plan files hold stale status and cannot record deviations. | E005 §2 |
| Minor | `B_hat` is called a bound; it is twice a first-order bound at the estimates. | E003 §6 |
| Minor | 25.7% of Gate 2 units were ideal ties; tie tolerance undocumented; unit clustering ignored in the pass statistic. | E003 §7 |
| Minor | Gate 4 thresholds were not derived from power analysis. | E004 §4 |

## What was verified as correct

- RC correction table: all 16 `CX` conjugations and signs re-derived by hand.
- Frame-covariance lemma proof; I1 = 0 at `phi = 0`; conditional likelihood
  specification.
- P-amp resource arithmetic (`SE = 0.0070902`).
- P-amp circuit semantics: 729 cases, maximum deviation `3.4e-15`
  (`tools/check_pamp_semantics.py`, new).
- **Lemma S1** (new, analytic): `epsilon` is not identified and has zero
  efficient information at `phi = 0` under any admissible nuisance class, so
  Gate 1A FAIL holds on a correct basis. Numerical check: at most `6.8e-21`.
- Gate 3 statistics reproduce exactly from stored fields; Gate 2 and Gate 3
  verdict-level results reproduce under full recomputation.
- All frozen lock and artifact checkers pass; 18 tests pass.

## Audit tools and outputs (`results/errata/`, hashed in `errata_manifest.sha256`)

| Tool | Output | Class |
|---|---|---|
| `tools/audit_gate1a_efficient_information.py` | `gate1a_efficient_information.json` | deterministic check of a frozen-spec quantity |
| `tools/audit_gate1a_pairs_budget.py` | `gate1a_pairs_at_budget.json` | deterministic restatement of stored quantities |
| `tools/check_pamp_semantics.py` | (pass/fail) | deterministic semantic check |
| `tools/audit_gate2_diagnostics.py` | `gate2_diagnostics.json` | exploratory, post hoc |
| `tools/audit_gate34_estimand.py` | `gate34_estimand.json` | post-hoc corrected estimand |
| `tools/audit_reproducibility.py` | `reproducibility_full.json` | provenance recomputation |
| `tools/check_errata_artifacts.py` | (pass/fail) | verifies errata hashes and that frozen files are intact |
