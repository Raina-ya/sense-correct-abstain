# Phase estimation and the P-amp novelty boundary

**Status:** reading note, 2026-11-20 (Claude). Sources were checked at the level
of bibliographic metadata and abstract only; no full text was read. Claims about
the papers below are limited to what their abstracts or official records say.
Keys refer to `../library.csv`.

## Why this note exists

Gate 1B's fallback sensor P-amp (research plan §3.4.1) repeats a cost block
`B(theta)` with `m` in {1, 4, 16} and adds echo pairs to separate the
angle-proportional error `epsilon` from the additive phase `phi`. Before any
novelty wording is frozen, P-amp must be placed next to the robust phase
estimation (RPE) family, which already estimates rotation-angle errors with
repetition ladders.

## What the sources establish (abstract level)

| Key | What the abstract or record states | Relevance to P-amp |
|---|---|---|
| `higgins2009` | An interferometric scheme for unambiguous phase estimation at the Heisenberg limit without adaptive measurements. | The non-adaptive repetition ladder that RPE builds on. P-amp's `m` ladder is the same idea. |
| `kimmel2015rpe` | A parameter-estimation technique that gauges amplitude and off-resonance errors in a single-qubit gate set, robustly and efficiently, with Heisenberg scaling, built on a robust version of Higgins et al.'s procedure. | An amplitude error is a multiplicative angle error, the single-qubit analogue of `epsilon`. RPE is therefore P-amp's closest known construction. |
| `kimmel2015rpe` (erratum) | An erratum was published (Phys. Rev. A 104, 069901, 2021), and arXiv v3 notes that a later paper supersedes one section's robustness analysis. | Any use of RPE's robustness guarantee must cite the corrected analysis. Not checked. |
| `rudinger2017rpe` | Experimental RPE on a trapped-ion qubit, without assuming perfect state preparation and measurement or ancillas, with Heisenberg scaling, cross-validated against gate set tomography. | Shows the method works on hardware for single-qubit rotation phases; no decision layer. |
| `russo2021rpe` | An extension of RPE that identifies results lying outside the expected statistical range; RPE's robustness depends on the noise meeting threshold assumptions, and consistency checks locate the point after which estimates should not be trusted. | A sensor-level version of "abstain when the evidence is unreliable". Closest prior idea to Gate 4's abstention arm at the sensor level. |

## Consequences for the plan

1. **P-amp is RPE-like.** Its repetition ladder, its target (an amplitude-type
   angle error), and its reliance on a known reference all match the RPE family.
   No novelty may be claimed for the sensor (consistent with
   `../novelty_claim_draft.md`, Branch B).
2. **What P-amp adds is context, not method.** It embeds the ladder in the
   tagged QAOA cost block (`CX - RZ - CX` with the control in `|0>`), uses echo
   pairs to separate `phi`, charges every shot to the fixed decision budget,
   and feeds a three-action decision. Each of these is a project choice to be
   justified, not a claim of a new estimator.
3. **Possible improvement before the week-4 freeze (owner's decision).** The
   current P-amp statistic is plain least squares on unwrapped phases. RPE's
   published ladder and estimator are designed for robustness to additive
   errors in the measurement probabilities. Replacing P-amp's estimator with
   the RPE estimator, or adding RPE-style consistency checks (`russo2021rpe`),
   is allowed only before week 4, because P-amp must be fixed before Gate 1A.
   After that, it cannot change.
4. **A new failure mode to record.** RPE's guarantees depend on noise thresholds
   (`russo2021rpe`). P-amp's pass condition (d) on phase ambiguity covers only
   one part of this; the plan's failure list for Gate 1B should add "noise above
   the robustness threshold of the ladder".

## Still to read

- Full text of `kimmel2015rpe` (and its erratum) for the exact experiment
  families, the robustness theorem, and its threshold.
- Full text of `russo2021rpe` for the consistency-check statistics, which may
  serve as negative controls.
