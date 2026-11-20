# Review of the predecessor E2 audit

**Review date:** 2026-11-20  
**Mode:** read-only repository and commit inspection; no simulation rerun.

## Commit and provenance

- The predecessor checkout resolves to
  `cd5e5764eabff6f51c406048be393bfd109130d5`.
- The commit object exists locally.
- Every predecessor path cited by the audit's core argument exists at that
  commit, including circuit construction, simulation, channel, probe,
  reference, protocol, theory-matrix, and primary/secondary result files.
- The predecessor worktree was not modified during this review.

## Claims directly spot-checked at the cited commit

| Audit claim | Review result |
|---|---|
| E2 multiplies only the marked cost rotation at simulator execution | Confirmed in `src/simulate.py`: `rzc` executes with `(1 + over_rotation) * params[0]`. |
| Primary designated rule uses E2 -> P2 and therefore reads the structure class | Confirmed in `src/cells_v4.py`. |
| The holdout primary result is noisy simulation, split 20, read once | Confirmed in `docs/results/primary_endpoint_v4.md`. |
| E2 primary false-certification and coverage figures | Confirmed in the committed per-structure table: FC(R0) `0.060937`, FC(R1) `0.015938`, coverage `0.6025` to `0.3000`, 195 false certifications on 7 graphs. |
| Structure-agnostic P2 is secondary and has lower coverage loss than the designated primary rule | Confirmed in the committed primary report: secondary `dFC +0.006652` and coverage loss `+0.141830`; the primary pooled coverage loss is `+0.417679`. |

## Boundary of this review

The review did not rerun the audit's on-the-spot exact calculations, including
the reported `0.0` framed/plain difference under E2 and the `0.033` E3 control.
Those remain labeled `audit check` in the audit and are not promoted to an
independent result. The line-numbered semantic and implementation claims were
checked by commit inspection, while explanatory mechanisms remain hypotheses
as labeled in the audit.

## Disposition

The audit is suitable as the predecessor-semantics input to Part 1, with two
restrictions:

1. predecessor P3 provides no evidence for the new RC-label construction; and
2. predecessor P2 provides an internal comparator for visibility/alarm value,
   not evidence that `epsilon` is identified or that correction is beneficial.

## Addendum, 2026-11-20 (Claude, not independent)

These checks were made by the author of the audit and therefore are not an
independent review; they only close gaps noted above.

| Item | Check | Result |
|---|---|---|
| File integrity | Git blob of `docs/audits/predecessor_e2_audit.md` in the user's repository versus the audited version | Identical (`5f85432...`) |
| Quoted holdout numbers | Re-read from `results/holdout_v4/primary_endpoint_v4.json` and `secondary_endpoints_v4.json` at `cd5e576` | E2 FC(R0) 0.0609375, FC(R1) 0.0159375, C 0.6025 -> 0.3, 195 false certifications on 7 graphs, interception 0.7436; P2 alarm rate 0.471875 (flipped, 20 graphs) vs 0.42890625 (not flipped, 80 graphs); E1 and E3 rows as quoted |
| Semantic-test rows | `experiments/semantic/semantic_tests_v4.csv` | P1/E2 max 2.2e-16, P3/E2 max 3.9e-16 (invariant); P2/E2 max 0.208, median 0.0019 (sensitive) |
| Main operating point | `results/development_v4/strength_map_v4.csv` rows 4-5 | `-0.04` selected (development median beta/Delta -0.2286 versus -0.1139 for `+0.04`) |

Not covered by either review and still worth an independent look:

- the claim that cost angles are not wrapped (`[0, 2*pi)` draws, transpiled
  `rz` keeps the value); the audit checked this with Qiskit 2.6.2, while the
  predecessor ran Qiskit 2.2.3;
- the claim that single-qubit gates, including frame `x` gates, carry no noise
  (`src/simulate.py` 136-150);

Resolved during this addendum: the holdout median beta/Delta for E2 (-0.2286 in
`docs/results/boundary_synthesis_v4.md`) and the development median used to
choose the sign (-0.2286 in the strength map) only agree after rounding.
Recomputed from the raw reference files: holdout -0.228602 (100 graphs at
`epsilon = -0.04`, 20 flipped), development -0.228550 (50 graphs). No error.
