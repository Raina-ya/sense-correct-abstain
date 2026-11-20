# Problem matrix

This matrix converts the literature review into decisions for the frozen
Gate 1A/1B route. `Open` means the project must answer the question; it is not a
claim that the cited literature lacks an answer.

| ID | Research question | Why it matters | Evidence needed | Primary sources | Current state | Decision/output |
|---|---|---|---|---|---|---|
| Q1 | Under which easy/hard-cycle and gate-dependence assumptions does RC tailor noise? | Angle-dependent E2 may violate the assumptions used to justify ordinary RC. | Exact theorem assumptions; treatment of gate-dependent easy-gate noise; distinction between average channel and per-label data. | Wallman & Emerson 2016; Winick et al. 2022 | Wallman verified previously; Winick abstract only | Assumption table for the proposed label construction. |
| Q2 | What information is supplied by label contrasts without an ideal response curve? | Gate 1A must not pass because a small circuit's ideal value is classically available. | Label-contrast likelihood; absolute-level likelihood; nuisance-profile or efficient Fisher information; null at `phi=0`. | Vyas 2026; project frame-covariance draft | Vyas abstract only; project derivation unverified | Separate Fisher quantities and a deployable Gate 1A pass criterion. |
| Q3 | Does label absorption change a logical-angle, compiled-angle, or physical-control error? | The three E2 semantics produce different covariance and may determine whether a label signal exists. | Explicit circuit identities and control semantics; no inference from predecessor P3. | Wallman & Emerson 2016; Vyas 2026; predecessor audit | Open; predecessor audit file absent locally | Frozen E2 semantics and label map `g_t(theta)`. |
| Q4 | Is P-amp distinct from known phase amplification, echo, pseudo-twirling, or KIK constructions? | If Gate 1A fails, the novelty claim cannot rest on renaming a known sensor. | Circuit-by-circuit comparison of amplification mechanism, reference, assumptions, and cost. | Santos et al. 2024; Henao et al. 2023; Layered KIK 2026 | Abstract-level only under the inherited status rules | Comparator table and restricted novelty statement. |
| Q5 | Is predecessor P2 a fair comparator for P-amp? | P2 is structure-agnostic and uses a classically known twin reference, but its transfer to the target can fail. | P2 construction and cost; CDR transfer assumptions; whether it estimates `epsilon` or only raises an alarm. | Predecessor frozen protocol; Czarnik et al. 2021; Lowe et al. 2021 | Predecessor construction located; external sources unverified candidates | Part 1 decision: include P2, exclude it with a reason, or keep it exploratory. |
| Q6 | Can sensing or correction improve the final decision after all costs are charged? | Parameter identifiability is not decision relevance. | Fixed-budget risk identity; correction uncertainty; abstention loss; comparison with fixed policies. | This project's theory; prior two projects; QEM lower-bound literature | Open | Gate 2--4 estimands and one deployable primary endpoint. |
| Q7 | Which methods handle the E2 error itself, rather than a different coherent error? | PST/KIK/RC results on native scaled two-qubit gates must not be generalized to logical QAOA `RZ` over-rotation. | Gate family, controllable sign/inverse, error Hamiltonian, and claimed suppression target. | Santos et al. 2024; Henao et al. 2023; Layered KIK 2026; Kurita et al. 2023 | Abstract-level only | Applicability/exclusion table; no borrowed positive conclusion. |
| Q8 | Which sequential tools belong to Chapter 4 rather than Chapter 3? | Drift and repeated sensing must not expand the one-shot Chapter 3 scope. | Non-i.i.d. assumptions, stopping/certification guarantee, and sensing allocation. | Zhang, Seshadri & Knill 2026 | Abstract fragment only under inherited state | Chapter 4 reading note; no Chapter 3 method change. |

## Immediate reading order

1. Q1: Wallman & Emerson, then Winick et al.
2. Q2--Q3: Vyas, checked against the project frame-covariance derivation.
3. Q5: predecessor P2 specification, then the original CDR source and Lowe et
   al. only to identify transfer assumptions.
4. Q4 and Q7: pseudo-twirling, Adaptive KIK, Layered KIK, and RC+ZNE.
5. Q6: decision-theory and lower-bound sources after the sensor model is fixed.
6. Q8: defer to the Chapter 4 parallel track.

