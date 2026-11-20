# Identification, nuisance information, and lower bounds

**Status:** reading note, 2026-11-20 (Claude). `vandervaart1998`,
`tsybakov2009`, `mitarai2018`, and `schuld2019` were checked at metadata level
(and, for the books, chapter location from publisher pages). Inherited sources
were verified bibliographically in the predecessor project. Keys refer to
`../library.csv`.

## What Gate 1A needs from statistics

Gate 1A (research plan §3.2–3.3) counts only label-contrast information (I1)
and the non-oracle part of the efficient information with the ideal response as
nuisance (I3). Each term needs a standard source.

| Concept in the plan | Standard source | Use |
|---|---|---|
| Efficient score and efficient information with nuisance parameters (I3) | `vandervaart1998`, chapter on semiparametric models (efficient information matrix in its index) | Define I3 as the information in the projection of the `epsilon` score orthogonal to the nuisance scores. |
| Identification region and "blind in principle" | `imbens2004`, `tamer2010` (inherited) | Already used for Chapter 2's definitions; reuse unchanged. |
| Two-point lower bound | `lecam1973` (inherited), `tsybakov2009` (Chapter 2, minimax lower bounds) | Action-selection blindness lemma and finite-pilot bound. |
| Learnable versus unlearnable noise | `chen2023learnability` (inherited) | Template for "no probe in this family can see it"; theorem conditions not checked for non-Clifford circuits. |
| Fisher conservation with labels | `vyas2026` (agent full-text reading) | `F_cond = F_marg + E[F(s | b)]`; see `vyas_2026.md`. |

## Circuit structure that matters for the nuisance argument

`mitarai2018` and `schuld2019` give the parameter-shift structure: for a gate
whose generator has two distinct eigenvalues, the expectation value is a
first-degree trigonometric function of that gate's angle. Consequences:

1. The ideal response is not an arbitrary function. It lies in a known
   finite-dimensional class (trigonometric polynomials in the cost angles).
2. Therefore the "closure under rescaling" condition in the frame-covariance
   draft is unlikely to hold, as already noted there.
3. The right I3 calculation is parametric: unknown trigonometric coefficients
   as nuisance, `epsilon` and `phi` as parameters, data from the label patterns
   at one operating point. Gate 1A's information question becomes a rank and
   conditioning question for a finite design matrix, which can be checked
   exactly for 2–3 qubits.

## Testability versus estimability

A deployable **test** of `H0: phi = 0` exists from label contrasts because the
null distribution does not depend on the response. An **estimate** of `phi`
needs the response slope, which is nuisance. For `epsilon` at `phi = 0`, there
is neither (see `vyas_2026.md`). The statistical language for this split is the
difference between a test whose size is controlled uniformly over the nuisance
and a parameter whose efficient information is zero; Part 1 should state both
with `vandervaart1998` as the reference.

## Limits of the QEM lower-bound literature for this project

`takagi2022`, `takagi2023`, `tsubouchi2023`, and `quek2024` (inherited) bound the
cost of estimating an observable with error mitigation. They do not bound the
probability of choosing the wrong action. Chapter 3's lower bounds should cite
them as estimator-level context and say clearly that the action-level bound is a
different quantity.
