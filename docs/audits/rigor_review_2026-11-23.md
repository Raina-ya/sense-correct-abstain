# Full rigor review before manuscript expansion (2026-11-23)

**Scope.** README, contracts, theory notes and owner-reviewed proofs, gate
reports, errata E001–E009, freeze documents, protocols, claim ledger,
reproducibility record, literature library and novelty audit, `paper/`, tools,
tests, CI, artifact/lock/errata/archive manifests. Reviewed at `4ecec2d`
(`origin/main`), before any manuscript change.

**Method.** Each mathematical statement was checked against the owner-reviewed
proof that governs it (E007–E009). Every number in the technical report was
traced to a frozen artifact or to an append-only audit output, and
recomputed from the stored per-unit records where that was possible. All
frozen-artifact checks were rerun. No holdout, gate evaluation, or other
data-generating process was run. No frozen, registered, or hash-locked file
was modified.

**Evidence labels used below.** *frozen* = artifact covered by a gate lock or
an errata manifest; *post-lock* = append-only analysis specified after the
result; *deterministic recomputation* = arithmetic on stored fields, done for
this review.

## 1. Baseline state

| Item | Result |
|---|---|
| Branch / HEAD | `main` at `4ecec2d`, equal to `origin/main` |
| Worktree | clean under `core.autocrlf=true`; the 20 files plain Linux git lists as modified differ only in CRLF |
| Untracked | `tmp/` (owner's), `_zipcheck.zip`, `_zipcheck_sums.txt` (archive check, deleted after use) |
| Frozen checks | errata (6 manifests, 40 entries, 6 frozen checks), Gate 1/2/3–4 lock and artifact checks, archive manifest, RC (64 cases), P-amp (729 cases, max dev. 3.44e-15), library (63/63): all pass |
| Tests | 24 tests pass (`python -m unittest discover -s tests`) |
| Zenodo archive | SHA-256 and MD5 match the record; all 119 files map one-to-one to commit `66feb06`; 114 differ only by CRLF line endings, 5 are byte-identical; the ZIP comment is the commit id |

## 2. Audit table

Severity: **critical** = a stated conclusion is false or unsupported;
**major** = a stated claim is mis-scoped or inconsistent with the governing
proof, but the conclusion survives; **minor** = wording, completeness, or
presentation.

| # | Item | Status | Evidence | Problem | Severity | Affects a conclusion? | Action |
|---|---|---|---|---|---|---|---|
| 1 | Lemma B scope in the report | inconsistent | `paper/technical_report_v1.tex` §2.2; ledger A7; `S1prime_B_rigorous.tex` Thm. 8 | The report calls Lemma B "local, instance-dependent ... not a global uniform guarantee". The owner-reviewed theorem is global in `(epsilon, phi)`, exact (no Taylor remainder), with sharp constant 1/2; it is instance-dependent only through `A` and `M`. The report understates what is proved and contradicts the ledger. | major | no (the bound is not used for any verdict) | Manuscript states the proved theorem, its assumptions, and what it does not cover (`B_hat`, coverage, decisions). The review request's "local Taylor bound with remainder" framing is superseded by E006 §3/E007; the first-order statement of E003 §6 is shown as a corollary. |
| 2 | Gate 1A identification wording | imprecise | report §4.1; `S1prime_B_rigorous.tex` Thm. 2, Prop. 4; E009 | "distinct local parameterizations with the same first-order observable response" and "local ... not an unrestricted global claim". The governing results are exact observational equivalences: local non-identification under N-q/N-loc, global under N-loc and N-free, and *failure* of global non-identification under N-q (bounded identified interval). Zero efficient information is a separate, first-order statement. | major | no | Manuscript separates the three notions and states the class-by-class identified sets. |
| 3 | Gate 2 population size | factual error | report §3; `docs/freeze/gate2_dev_design.md` lines 27–28; `results/dev/gate2_results.json` | Report says "10 graphs with 2-4 qubits". The frozen strata include path-5, cycle-5, star-5: 2–5 qubits (660 units each). | minor | no | Corrected in the manuscript. |
| 4 | Gate 1A two-point bounds | valid but loose | `tools/audit_gate1a_pairs_budget.py`; `results/errata/gate1a_pairs_at_budget.json` | The reported equal-prior error bounds (0.185–0.232) use the Le Cam / Bretagnolle–Huber lower bounds on `1 - TV_n`. The same audit also computes `TV_n <= sqrt(1 - BC_n^2)`, which gives a tighter valid bound `(1 - TV_n)/2 >= 0.245–0.366`. Both directions and constants are correct. | minor | no | Manuscript reports both, labelled; the tighter value is a deterministic recomputation from stored `BC_n`, not new data. |
| 5 | Hellinger normalisation | two conventions | theory note §5 (`H^2 = int (sqrt p - sqrt q)^2`, `BC = 1 - H^2/2`); Gate 1A artifact field `hellinger_squared = (1/2) sum (...)^2 = 1 - BC` | Both are internally consistent, but a reader mixing them would be off by a factor 2. | minor | no | Manuscript fixes one convention and states the artifact's. |
| 6 | Gate 3 frozen estimand | defect disclosed (E004 §1) | E004; `results/errata/gate34_estimand.json` | Frozen N-path loss is the unconditional always-issue error, ignoring selection on the same shots. | major (disclosed) | no (both estimands FAIL) | Manuscript derives the bias exactly: per unit, frozen minus conditional N-path contribution equals `-Cov(1{N}, 1{W})`. Post-lock status kept explicit. |
| 7 | Gate 3 decomposition | not reported | stored per-unit `delta`, `action` | `Delta_V` comes entirely from N and A units (C units contribute exactly 0). Frozen: N −0.000260, A +0.000341; corrected: N −0.000104, A +0.000340. | minor | no | Added as a deterministic descriptive decomposition of frozen records. |
| 8 | Power computed in the same run | disclosed in E004 §3, absent from report | E004 §3 | The report states power 0.0004 without saying that it was computed in the same execution as the evaluation. | minor | no | Stated in the manuscript's failure analysis. |
| 9 | Review record / pace | disclosed in E005 §3, absent from report | E005 §3 | Locks marked "owner-approved" without review notes; 2–34 min between lock and run. | minor | no | Stated in the manuscript's failure analysis. |
| 10 | Monte Carlo granularity | disclosed in E004 §2 | E004 §2 | Stored losses have granularity 1/256 against `\|Delta_V\| < 0.001`; exact probabilities were computable. | minor | no | Stated. |
| 11 | Gate 2 label estimand | disclosed in E003 §4 | E003 §4 | Gate 2 labels are unconditional unit-level benefits, not the decision-time quantity of Gate 3. | minor | no | Stated. |
| 12 | Example E1 / E2 status | governed by E008 | E008 §2–3 | E1 needs equal stage-1 laws including `X_T0`; E2's second condition is open. | minor | no | Manuscript gives the repaired E1 and labels E2 conditional/open. |
| 13 | "Nonunique maximiser ⇒ FAIL" | specification inference | E007 §3.1 | Checked against spec §7, §9 and the box `[-0.05,0.05]^2`; not a theorem. | — | no | Labelled "specification inference". |
| 14 | Do the readings cover spec §5.3? | open specification question | E007 §3.2, E009 | Readings (a)–(d) are proved; whether they exhaust §5.3 is not a mathematical question. | — | no | Labelled open. |
| 15 | Report build path | process | `tools/build_technical_report.py` | The `.tex` is generated from Markdown and the PDF is drawn by ReportLab from the Markdown, so the PDF is not a rendering of the `.tex`. Expanding the `.tex` by hand would be overwritten by the generator. | minor | no | `.tex` becomes the single authoritative source; the builder compiles it with LaTeX; the Markdown becomes a short pointer, so no competing version remains. |
| 16 | Ledger cross-references | stale | `docs/claim_ledger.md` header and row D "First" | Header points to the Markdown report; row D says "MT7.4 open" although the scoped audit is complete. | minor | no | Ledger pointers updated (living document). |
| 17 | Bibliography | completeness | `paper/references.bib` | 10 entries, cited by `\nocite{*}` only; keys differ from `library.csv`. | minor | no | Rebuilt from `library.csv` fields only; every entry cited in text; unverifiable metadata (e.g. short-title entries) not cited. |
| 18 | CI | new, unconfirmed | `.github/workflows/checks.yml` | Added on 2026-11-22; a green hosted run has not been confirmed in this review. | minor | no | Disclosed; internal recomputation only. |
| 19 | Archive verification | completed | §1 above | The archive is content-identical to `66feb06` up to line endings. | — | no | Recorded in `docs/reproducibility.md` §0. |

No **critical** issue was found. Every gate verdict, the primary endpoint,
the comparator policy, and the stopping rule are unaffected.

## 3. Numbers recomputed from frozen per-unit records (deterministic)

| Quantity | Stored / reported | Recomputed here |
|---|---|---|
| Gate 3 frozen `Delta_V` | 0.0000804 | 0.0000804 (3545 evaluation units) |
| Contribution by action, frozen | — | N −0.0002600, C 0, A +0.0003405 |
| Policy-lock cluster-mean average | −0.00063 | −0.000635 |
| Minimum detectable mean | 0.000665 | `1.669 x 0.003235 / sqrt(66)` = 0.000665 |
| Gate 3 evaluation cluster means | 66 clusters | 30 exactly zero, 12 positive, 24 negative |
| Gate 4 frequencies | N 25.9%, C 72.6%, A 1.5% | 919 / 2573 / 53 of 3545 |
| Gate 2 precision / base rate | 0.093 / 0.077 | 272/2932 = 0.0928; 287/3726 = 0.0770 |
| Gate 1B margin | 0.7% | `1 - 0.0070902/0.0071429` = 0.74%; fails for `v < 0.99263` |
| Gate 2 strata | "2–4 qubits" | 2–5 qubits (item 3) |

## 4. Classification of issues after this review

- **Corrected in the manuscript:** items 1, 2, 3, 15, 16, 17.
- **Disclosed only (cannot be fixed without new data or editing frozen
  files):** items 6, 8, 9, 10, 11 and the code-outside-lock defect (E005 §1).
- **Open (specification or theory):** items 12 (E2 second condition), 13, 14.
- **Added as deterministic restatements of stored quantities:** items 4, 7.
