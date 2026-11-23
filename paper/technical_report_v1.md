# Sense, Correct, or Abstain — paper pointer

The paper's single authoritative source is
[`technical_report_v1.tex`](technical_report_v1.tex), compiled to
[`technical_report_v1.pdf`](technical_report_v1.pdf) by
`python tools/build_technical_report.py`. This file is kept only so that
links from the errata and earlier documents still resolve; it is not a second
version of the paper.

**Evidence boundary:** analytic results and synthetic simulation only; no
hardware experiment and no independent validation. Every claim maps to
[`../docs/claim_ledger.md`](../docs/claim_ledger.md); the append-only errata
in [`../docs/errata/`](../docs/errata/README.md) take precedence over
superseded statements in frozen artifacts.

**One-paragraph summary (same evidence level as the paper).** Under a
synthetic compiled-angle error model and a fixed 24,300-shot budget, Gate 1A
failed (retained randomized-compiling labels cannot identify the
multiplicative error at `phi = 0` under the response-free nuisance classes),
Gate 1B passed only in a noiseless known-reference model with a 0.7%
visibility margin, and Gate 2 formally passed its prespecified, internally
locked rule, but the diagnostic did not demonstrate useful selective
prediction of which units benefit from correction (precision 0.093 versus a
base rate of 0.077; much of the apparent gain came from excluding large-gap
units). Gate 3 failed: `Delta_V = 0.0000804` with one-sided 95% lower bound
`-0.000743`; a corrected post-lock estimand also failed (`0.000237`,
`-0.000625`), and estimated power was 0.0004. The project stopped after M6.
These are boundary and negative results, not evidence that the method works.

The Markdown text of the shorter MT7 report that this file replaced is in the
git history (commit `4ecec2d`).
