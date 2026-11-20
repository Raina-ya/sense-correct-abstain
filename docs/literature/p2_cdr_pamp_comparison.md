# P2 vs. CDR vs. P-amp

**Status:** Part 1 comparator decision draft. P2 facts are taken from the
predecessor audit at predecessor commit `cd5e576`. CDR literature remains
unverified beyond the identified primary-source metadata/abstract; no CDR
novelty conclusion is frozen here. P-amp is specified in research plan
§3.4.1 (circuits, repetitions, statistic, budget share, pass conditions); its
numerical choices are drafts that must be confirmed and frozen in week 4,
before any Gate 1A check is run.

| Dimension | Predecessor P2 | CDR family | Proposed P-amp |
|---|---|---|---|
| Purpose | Alarm on bias of a deterministic nearest-Clifford twin. | Learn a mapping from noisy to ideal observables using classically tractable training circuits. | Identify or bound the angle-dependent error strongly enough to support Gate 2 after Gate 1A fails. |
| Runtime data | Observed gap of two twin circuits. | Noisy observables from a set of training circuits and the target. | X- and Y-basis outcomes of 9 circuits (6 repetitions `B(theta)^m`, `m` in {1,4,16}, `theta` in {pi/8, pi/4}; 3 echoes) = 18 settings (plan §3.4.1). |
| Known reference | Twin's own noiseless gap, computed classically; target ideal gap is forbidden. | Ideal values of classically simulable training circuits. | Analytically known single-qubit phases (`m*theta` for repetitions, 0 for echoes); target ideal gap remains forbidden. |
| Structural knowledge | Structure-agnostic secondary rule can always use P2. Transfer from twin to target remains an assumption. | Requires a training-circuit generation rule and a transfer model. | Sensor is prespecified for angle-dependent coherent bias; it may not read the true `epsilon` or error-structure label at runtime. |
| Output | Scalar alarm score `abs(g_twin,obs - g_twin,ideal)`; not an established `epsilon` estimator. | Corrected target observable from a fitted relation. | Least-squares `(epsilon_hat, phi_hat)` from unwrapped residual phases (plan §3.4.1). |
| How `epsilon` enters | Through the twin's rounded Clifford angles: a cost angle rounded to `k*pi/2` with `k != 0` executes as `(1+epsilon) k pi/2`; angles rounded to 0 carry no signal (predecessor audit §2). | Through whatever the training circuits contain. | Through `m * theta * epsilon` in repetitions; echoes cancel it and isolate `phi`. |
| Cost | Two extra circuits in the predecessor protocol; probe shots are charged. | Multiple training circuits, classical ideal simulations, fitting, and target shots. | Sensing share `f*N` split over 18 settings; depth up to 32 cost blocks (echo `m = 16`); correction re-execution charged separately under Gate 3. |
| Use of ML | No. | Regression/learning is intrinsic to standard CDR. | No ML; estimator and switching rule must be analytic and interpretable. |
| Main failure mode | Twin and target respond differently to angle-dependent error; alarm need not track target flips. | Training distribution or noise response does not transfer to the target; training cost can dominate. | Aliasing/nonmonotonic response, echo mismatch, depth noise masking the signal, or insufficient net value. |
| Evidence already available | In predecessor E2, P2 reduced false certification by abstaining but had similar alarm rates on flip and non-flip graphs; this is visibility, not selective correction evidence. | None established for this project. | None; only a frozen fallback route exists. |
| Relation to novelty | Strong, mandatory comparator because it already provides a known-reference, structure-agnostic alarm in the same predecessor pipeline. | Defines the broader known-reference/training-circuit neighborhood. | Sensor mechanism itself is unlikely to support a broad novelty claim; novelty must be in decision relevance and fixed-budget action selection. |

## Decision

P2 should be included in Part 1 as a **mandatory comparator**, subject to the
same total sensing budget as Gate 1B. It should not be promoted to a fourth
adaptive branch. Its roles are:

1. a known-reference baseline for sensing/alarm visibility;
2. a test of whether P-amp adds parameter or decision information beyond a
   deterministic Clifford twin; and
3. a guard against claiming novelty for "using a reference circuit to expose a
   coherent angle-dependent error."

CDR should remain a literature comparator, not an implemented method, because
the project forbids ML and because implementing a training-family regression
would expand the frozen method set. Before citation, the original CDR source
must be read in full and its transfer assumptions recorded.

## Note: P2 is closer to an `epsilon` estimator than its predecessor use suggests (added 2026-11-20)

The twin's ideal gap is classically computable, and so, to first order, is its
derivative with respect to `epsilon`: the derivative of a Clifford circuit's
expectation with respect to small rotations about its own `Z` angles is a sum of
Clifford expectations with inserted Paulis, which stabilizer simulation can
evaluate. In principle, therefore, `(g_twin,obs - g_twin,ideal) / (d g_twin / d epsilon)`
is a deployable first-order `epsilon` estimate wherever the derivative is not
small. This is a project derivation, not checked, and it is **not** a new branch:
it only strengthens the conclusion that the sensor mechanism cannot carry the
novelty claim, and it suggests that the P2 comparator should be reported both as
an alarm (predecessor form) and, if Part 1 freezes it before Gate 1A, as this
first-order estimate. D5 subsequently froze P2 in its predecessor alarm form
only, so this unproved estimate is not implemented in the locked Gate 1 study.
The usual P2 failure remains: the twin and target can
respond differently to the same `epsilon`.

## Fair-comparison requirements

- Same total sensing budget and the same accounting for classical reference
  computation.
- No target ideal value, true `epsilon`, or structure label as an input.
- Separate parameter estimation, alarm visibility, flip prediction, and final
  policy value.
- Report when a method is undefined or its reference is not classically
  tractable; do not replace it after inspection.
- P2 remains a comparator even if it performs poorly, because the predecessor
  makes it the closest internal prior method.

