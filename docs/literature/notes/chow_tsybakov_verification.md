# Chow and Tsybakov attribution verification

**Checked:** 2026-11-23. This note verifies two attributions that remained open
after MT7. It changes no theorem statement, proof, frozen artifact, or gate
verdict.

## Chow (1970)

The bibliographic record is C. K. Chow, "On Optimum Recognition Error and
Reject Tradeoff," *IEEE Transactions on Information Theory* 16(1), 41-46,
1970, DOI `10.1109/TIT.1970.1054406`.

A scan of the published article was read in full. Section II defines

\[
m(v)=\max_i P(i\mid v)
\]

and states the optimum rule as accepting when `m(v) >= 1 - t` and rejecting
when `m(v) < 1 - t` (equations (2') and (4')). In the project's two-action
reduction, the wrong-answer probability is `e_N(x) = 1 - m(x)` and abstention
cost is `lambda_A`; hence `e_N(x) > lambda_A` is exactly
`m(x) < 1 - lambda_A`. The project's C2 threshold form is therefore a direct
specialization of Chow's published rule, with `t = lambda_A`.

Evidence boundary: the full text was accessed through a third-party scan; the
DOI, venue, volume, issue, pages, and year were checked independently against
publisher-indexed metadata. The project's proof remains self-contained.

## Tsybakov (2009)

The bibliographic record is A. B. Tsybakov, *Introduction to Nonparametric
Estimation*, Springer Series in Statistics, 2009, DOI `10.1007/b13794`.

The relevant pages of a scan of the published book were checked:

- Lemma 2.3, "Le Cam's inequalities," includes
  `integral min(dP,dQ) >= (1/2)(integral sqrt(dP dQ))^2`.
- Lemma 2.6 states
  `integral min(dP,dQ) >= (1/2) exp(-K(P,Q))`.

These are the two locations cited by the finite-pilot proof. The directions
and constants agree with the project's self-contained derivation.

Evidence boundary: the lemma text was checked in a third-party scan; the book
metadata and DOI were checked on the Springer page. No claim relies on the
scan alone.

