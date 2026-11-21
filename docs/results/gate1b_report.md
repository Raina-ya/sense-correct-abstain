# Gate 1B report: frozen P-amp fallback

**Run time (UTC):** 2026-11-20T08:06:52.936711+00:00

**M3 lock commit:** `14432b26f00309fee7529c61b7ec884a491b9fc9`
**Evidence:** analytic and exact noiseless P-amp calculation; no noisy simulation or hardware.

## Verdict

**Gate 1B passes.** The frozen P-amp design has analytic rank two and exactly recovers `(epsilon,phi)` at all 81 frozen grid points within the `1e-8` tolerance. The resource and phase-ambiguity criteria also pass. P-amp becomes the sole sensor carried into Gate 2; RC labels do not.

## Pass conditions

| Condition | Result | Detail |
|---|---|---|
| a_analytic_rank | PASS | rank 2 known-reference design |
| b_noiseless_recovery | PASS | 81/81 within 1e-8 |
| c_budget | PASS | SE 0.00709019 <= 0.00714286 |
| d_no_phase_ambiguity | PASS | all 81 frozen grid points |
| e_p2_reported | PASS | alarm-only comparator reported nonevaluable; no post-lock substitute |
| f_no_target_oracle | PASS | P-amp uses its own known reference only |

## Recovery

- Grid points: 81/81 recovered.
- Maximum absolute `epsilon` error: `1.25e-16`.
- Maximum absolute `phi` error: `2.08e-17`.
- Design eigenvalues: `(141.3843631775228, 1707.115793189461)`.

## P2 comparator

P2 is retained in the D5-frozen predecessor alarm form. It is reported as **nonevaluable in this minimum reference study** because M3 did not freeze a twin circuit or alarm threshold for the `G2/G3` reference contexts. The fair-comparison rule requires reporting undefined comparators rather than inventing one after Gate 1A. This does not supply evidence that P-amp outperforms P2 and must be resolved on the later frozen target task before a comparative claim.

## Claim boundary and limitations

This is an identifiability result for the known-reference, noiseless, synthetic P-amp model. It does not establish robustness to visibility loss, decoherence, drift, context mismatch, asymmetric negative-angle error, finite-shot estimator bias, or hardware implementation. The sensor is RPE-like and carries no novelty claim. Passing Gate 1B authorizes Gate 2 development only; it does not establish decision relevance, correction benefit, or positive fixed-budget value.

## Routing

Proceed to Gate 2 with P-amp as the sole sensor. Keep the Gate 1A RC-label failure as a negative identifiability result. No third sensor is allowed.
