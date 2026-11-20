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

