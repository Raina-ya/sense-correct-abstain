# Presentation

Slides for the sense-correct-abstain technical report (thesis chapter 3):
**Fixed-Budget Error Sensing and Decision Policies for QAOA: Identifiability Limits and a Negative Policy Result.**

- [slides.pdf](slides.pdf): 62 slides, 16:9, vector PDF.
- [source/](source/): the deck as one HTML `<section>` per slide (`source/slides/*.html`), the slide order and sections (`source/deck.json`), and the shared stylesheet (`source/deck.css`). Formulas are embedded as path-only SVG rendered from LaTeX. Each slide's speaker notes are in its `<aside>` element (written in Traditional Chinese).

The deck follows the paper's structure: motivation, related work, decision problem, error model, three-action theory (T1, P1, C1/C2, L1, T2, D1, P2, with proof ideas), identifiability (S1′, the sharp identified set, Lemma B), experimental design, the four gate results, failure analysis, the HW-P1 hardware pilot, reproducibility, and conclusions.

Every number on the slides is taken from [paper/technical_report_v1.tex](../paper/technical_report_v1.tex); the paper is authoritative where the two differ. The slides introduce no new results.
