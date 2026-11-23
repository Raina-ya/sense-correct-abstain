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
   response-free nuisance classes (Lemma S1′, E006 §2, owner-reviewed in E007);
2. sensor-independent decision theory: the three-action risk identity,
   blindness lemma, finite-pilot bound, and collapse result (draft proofs);
3. a documented negative result: a P-amp-guided three-action policy shows no
   detectable value over always correcting at the frozen budget.

## MT7.4 citation and novelty audit (completed 2026-11-21)

**Method and scope.** The audit searched the project library and primary-source
records for randomized-compiling labels, robust phase estimation, CDR/vnCDR,
pseudo twirling, Adaptive/Layered KIK, decision-aware QEM, fixed-budget
calibration, and reject/abstain policies. It is a scoped prior-art audit, not a
systematic review and not evidence of priority. Verification levels in
`library.csv` remain controlling; an abstract or publisher HTML reading is not
silently promoted to a reproduced theorem.

**Primary-source comparison.** The audit establishes the following boundaries:

1. Kimmel--Low--Yoder RPE already estimates amplitude and off-resonance errors
   with a repetition ladder and a known single-qubit reference. Russo et al.
   already add consistency checks that flag when later RPE estimates should
   not be trusted. P-amp therefore carries no novelty as an estimator or as a
   sensor-level trust check.
2. CDR and vnCDR already use classically tractable near-Clifford training
   circuits and learned transfer maps from noisy to ideal observables. The
   project's P2 twin belongs to this known-reference neighborhood, but one
   deterministic twin does not inherit CDR's transfer evidence and was
   structurally blind on half of the frozen Gate 2 units.
3. Pseudo twirling changes control-pulse signs for general non-Clifford gates,
   distinguishes controlled over/under-rotation from other coherent errors,
   and explicitly does not eliminate the controlled rotation error. It is a
   pulse-level mitigation/calibration method, not evidence that retained RC
   labels identify the project's compiled-angle `epsilon`.
4. Adaptive KIK uses pulse-based inverse evolutions and polynomial
   combinations of expectation values under a time-local-noise assumption;
   Layered KIK extends that mitigation architecture to dynamic circuits. These
   methods mitigate observables rather than choose among issue, recalibrate,
   and abstain under the project's fixed budget.
5. Scavino's decision-kernel work is the closest decision-level QEM source: it
   independently shows that expectation-value accuracy need not improve
   downstream gap-based decisions and studies fixed-allocation finite-shot
   limits. Therefore neither “decision-aware QEM” nor “fixed-budget decision
   relevance” is novel by itself.

**Search result.** Within this scoped search, no primary source was found that
combines all of: retained-label identifiability with the ideal target response
treated as nuisance; a fixed total sensing/re-execution budget; and a
three-action issue/recalibrate/abstain policy evaluated against locked fixed
policies. This is only a description of the searched neighborhood. It must not
be rewritten as “first”, “unique”, or a comprehensive absence claim.

**Final novelty boundary.** The report may present the work as a documented
combination and negative boundary study: it separates deployable
identifiability, benefit selection, and net policy value, then shows that the
frozen combination fails to produce detectable value. The sensor mechanisms,
decision-aware evaluation, rejection option, and fixed-budget analysis each
have prior art. No priority claim is made.

**Attributions verified after synthesis.** The exact Chow (1970) threshold
rule and Tsybakov Lemmas 2.3 and 2.6 were checked on 2026-11-23 against scans
of the published article and book; bibliographic metadata was checked
separately against DOI/publisher records. The project proofs remain
self-contained and do not rely on those attributions.
Lemma S1′ and Lemma B were owner-reviewed and accepted with corrections (E007;
`docs/theory/S1prime_B_rigorous.pdf`).
