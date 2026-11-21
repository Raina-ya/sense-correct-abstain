# Gate 1A/1B novelty claim draft

**Status:** conditional wording for prior-art review. Not a final novelty claim
and not evidence of priority. No phrase such as "first" may be used until the
remaining comparator literature has been read and searched systematically.

## Terminology (added 2026-11-20)

`epsilon` means an angle-proportional error. "Logical-angle model" is reserved
for the E2 placement in which the error acts before label absorption; under it,
labels are blind by construction, so Branch A cannot succeed under that
placement. Earlier wording "logical-angle multiplicative error" is replaced by
"angle-proportional error under the frozen placement".

## Shared contribution independent of the sensor outcome

The proposed contribution is a fixed-budget, deployable action-selection
framework that separates four questions often conflated in QEM:

1. is an error parameter identifiable from runtime evidence without target
   ideal values;
2. does the estimate predict candidate-gap bias or a decision flip;
3. does sensing and correction retain net value after all shots and reruns are
   charged; and
4. does the resulting policy genuinely choose among no action, correction, and
   abstention rather than collapse to a fixed action?

The general risk identity, action-selection blindness lemma, and finite-pilot
lower bound are not specific to QAOA, E2, RC labels, or P-amp.

## Branch A: Gate 1A succeeds

Candidate claim:

> For a frozen QAOA cost-rotation construction, we determine whether the
> information supplied specifically by retained randomized-compiling labels -
> after removing information that requires the target's ideal response - is
> sufficient to support a fixed-budget choice among no action, recalibration,
> and abstention.

Branch A is reachable only if the frozen placement is not the logical-angle
model and either (i) the compiler representation gives the label an
angle-proportional term (for example Z labels absorbed as `theta + pi` with
wrapping) or (ii) the admissible part of I3 is positive. The claim must name
which of the two produced the information.

What is distinct from Vyas, if supported:

- an angle-proportional error `epsilon`, whereas the paper's `s theta` phase
  corresponds to the project's additive `phi` (see the parameter mapping in
  `notes/vyas_2026.md`);
- explicit separation of label-contrast, absolute-level/oracle, and
  nuisance-profile information;
- candidate-gap and top-1 decision relevance rather than coherent-angle
  recovery alone;
- sensing, recalibration, re-execution, and abstention charged to one budget.

What must not be claimed:

- that label retention itself is new;
- that Fisher-information conservation is new;
- that RC universally corrects E2;
- that a 2--3 qubit existence result generalizes across QAOA or hardware.

## Branch B: Gate 1A fails and frozen Gate 1B succeeds

Candidate claim:

> Retained RC labels are blind to the frozen angle-proportional error
> under the deployable contrast criterion, but a prespecified amplification and
> echo reference can supply enough runtime evidence to test whether
> recalibration or abstention has positive decision value under the same total
> budget.

Here the novelty is **not** the existence of phase amplification, echo, known
references, or Clifford surrogate circuits. Predecessor P2 can itself be read
as a first-order `epsilon` estimator (see `p2_cdr_pamp_comparison.md`), which
further rules out any claim based on the sensor. It is the decision-control layer:
mapping bounded runtime evidence to actions, charging all costs, comparing with
P2, and stating when the policy must abstain or collapse.

## Branch C: both Gate 1A and Gate 1B fail

Candidate claim:

> For the frozen sensor family and resource model, observationally equivalent
> error states require different optimal actions; therefore no policy based on
> those runtime observations can reliably choose correction over abstention.

This branch reports the RC-label construction as a negative identifiability
example and the P-amp failure as a resource/model boundary. No third sensor is
introduced after inspection.

## A candidate theoretical contribution in every branch (added 2026-11-20, to be derived)

Labels can give a deployable **test** for an additive error without giving an
**estimate** of it, and give neither for an angle-proportional error at
`phi = 0` (see `notes/vyas_2026.md`, "Testability versus estimability"). If this
survives formal derivation, it supplies a clean decision-level statement: label
evidence can license abstention but not correction. Its novelty is unchecked.

## Prior-art work still required before freezing wording

- Full CDR/P2 transfer review.
- Full pseudo-twirling and KIK comparison.
- Search for fixed-budget calibration-or-abstention policies and decision-aware
  coherent-error sensing.
- Verify whether any existing work already separates label-only Fisher
  information from ideal-response information in a variational algorithm.


## MT7 status after the gate sequence (added 2026-11-21)

**Route taken:** Branch B (Gate 1A FAIL, Gate 1B PASS), then Gate 2 formal
PASS and Gate 3 FAIL. The Branch B candidate claim above ("can supply enough
runtime evidence to test whether recalibration or abstention has positive
decision value") was tested. Its answer is **negative** in the frozen
synthetic setting: no detectable net value, with power about 0.0004
(`docs/claim_ledger.md`, B5).

**What may be offered as a contribution** (still no priority claim):

1. a boundary result: under the synthetic compiled-angle model, retained RC
   labels do not identify the angle-proportional error at `phi = 0` under
   response-free nuisance classes (Lemma S1′, E006 §2);
2. sensor-independent decision theory: the three-action risk identity,
   blindness lemma, finite-pilot bound, and collapse result (draft proofs);
3. a documented negative result: a P-amp-guided three-action policy shows no
   detectable value over always correcting at the frozen budget.

**MT7.4 citation and novelty audit: NOT complete.** Outstanding:

- owner confirmation of the AI-agent full-text readings (Wallman & Emerson,
  Winick, Vyas);
- full-text reading of the robust phase-estimation papers, pseudo-twirling and
  KIK papers, and the closest decision-level QEM work (`scavino2026`);
- a systematic, documented search for fixed-budget calibrate-or-abstain
  policies and for label-only versus ideal-response information separation;
- full-text verification of the Chow (1970) rule form and the Tsybakov lemma
  locations.

Until these are done, the report uses only the verification states recorded
in `library.csv`, and no novelty wording is frozen.
