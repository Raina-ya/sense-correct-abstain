# Gate 2 development report

**Run time (UTC):** 2026-11-21T06:42:12.081758+00:00

**Gate 2 lock commit:** `38d900dbeef3f9e468aed8e21377c1aba59c8c20`

**Evidence:** development-only synthetic noisy simulation; no holdout and no hardware.

## Verdict

**Gate 2 PASS.** The frozen P-amp transfer rule had balanced accuracy `0.5871` versus `0.5000` for the frozen no-information baseline. Its full improvement was `0.0871` and its leave-one-graph-out robustness lower bound was `0.0658`; passage required positive full improvement and a lower bound of at least `0.05`.

## Evaluation population

- Generated units: 6600.
- Evaluable units: 4905.
- Rule-development / evaluation: 1179 / 3726.
- Evaluation positives / negatives: 287 / 3439.
- Frozen baseline prediction: nonpositive correction benefit.

## Same-budget P2 comparator

P2 balanced accuracy was `0.5224`, full improvement `0.0224`, and robustness lower bound `0.0209`. P2 is a comparator only and cannot rescue the primary verdict.

## Failure separation and controls

- Undefined or ideal-tie units are retained in the machine-readable artifact.
- P-amp estimation/ambiguity failures: 0.
- Matched-null units: 327.
- The asymmetric-negative-angle control is scoring-only and did not contribute to the verdict; its mean absolute `phi` estimation error was `0.007026`.
- Every shot is charged under the frozen `24,300`-shot ledger. Net policy value is not tested here.

## Claim boundary and routing

This result concerns decision relevance only in the locked synthetic development model. It does not establish net value, action non-degeneracy, confirmatory generalization, device realism, or hardware benefit.

Route: **Gate3/Gate4**.
