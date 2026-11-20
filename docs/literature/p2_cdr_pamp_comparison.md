# P2 vs. CDR vs. P-amp

**Status:** Part 1 comparator decision draft. P2 facts are taken from the
predecessor audit at predecessor commit `cd5e576`. CDR literature remains
unverified beyond the identified primary-source metadata/abstract; no CDR
novelty conclusion is frozen here. P-amp is a prespecified fallback concept,
not yet a complete circuit specification.

| Dimension | Predecessor P2 | CDR family | Proposed P-amp |
|---|---|---|---|
| Purpose | Alarm on bias of a deterministic nearest-Clifford twin. | Learn a mapping from noisy to ideal observables using classically tractable training circuits. | Identify or bound the angle-dependent error strongly enough to support Gate 2 after Gate 1A fails. |
| Runtime data | Observed gap of two twin circuits. | Noisy observables from a set of training circuits and the target. | Repeated/amplified and echo-reference outcomes; exact statistic is not yet frozen. |
| Known reference | Twin's own noiseless gap, computed classically; target ideal gap is forbidden. | Ideal values of classically simulable training circuits. | Must use a frozen null/echo or analytically known reference; target ideal gap remains forbidden. |
| Structural knowledge | Structure-agnostic secondary rule can always use P2. Transfer from twin to target remains an assumption. | Requires a training-circuit generation rule and a transfer model. | Sensor is prespecified for angle-dependent coherent bias; it may not read the true `epsilon` or error-structure label at runtime. |
| Output | Scalar alarm score `abs(g_twin,obs - g_twin,ideal)`; not an established `epsilon` estimator. | Corrected target observable from a fitted relation. | Intended estimate/interval for `epsilon` or directly for correction benefit. |
| Cost | Two extra circuits in the predecessor protocol; probe shots are charged. | Multiple training circuits, classical ideal simulations, fitting, and target shots. | Amplification repetitions, echo/reference circuits, depth-induced noise, and re-execution must all be charged. |
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

