# Gate 1A/1B novelty claim draft

**Status:** conditional wording for prior-art review. Not a final novelty claim
and not evidence of priority. No phrase such as "first" may be used until the
remaining comparator literature has been read and searched systematically.

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

What is distinct from Vyas, if supported:

- logical-angle multiplicative error rather than an injected `s theta`
  coherent phase;
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

> Retained RC labels are blind to the frozen logical-angle multiplicative error
> under the deployable contrast criterion, but a prespecified amplification and
> echo reference can supply enough runtime evidence to test whether
> recalibration or abstention has positive decision value under the same total
> budget.

Here the novelty is **not** the existence of phase amplification, echo, known
references, or Clifford surrogate circuits. It is the decision-control layer:
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

## Prior-art work still required before freezing wording

- Full CDR/P2 transfer review.
- Full pseudo-twirling and KIK comparison.
- Search for fixed-budget calibration-or-abstention policies and decision-aware
  coherent-error sensing.
- Verify whether any existing work already separates label-only Fisher
  information from ideal-response information in a variational algorithm.

