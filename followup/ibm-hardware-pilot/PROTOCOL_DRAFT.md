# HW-P1: IBM Quantum hardware pilot — protocol draft

**Status: DRAFT. Not locked, not approved, nothing executed.** This is a new
study. It does not revise, rescue, validate, or confirm any verdict of the
frozen sense-correct-abstain study (Gates 1A–4, errata E001–E009). Its results,
whatever they are, will be reported as results of HW-P1 only.

**Gate to execution (all required, in order):** (1) owner decisions in §9;
(2) noiseless and fake-backend dry-runs of §6 pass; (3) circuit count and usage
estimate recomputed from the transpiled circuits; (4) a protocol lock under
`docs/protocols/lock_template_v2.md` that hashes this file, all code, the
environment, seeds, and the exact command; (5) explicit written approval by the
owner. No hardware job is submitted before step 5.

---

## 1. What carries over to hardware, and what does not

| Element of the frozen study | On IBM hardware | Consequence |
|---|---|---|
| Compiled-angle error `RZ(a) -> RZ((1+eps)a + phi)` | IBM `rz` is a virtual frame change, implemented at zero error and zero duration. A tagged `rz` therefore has **no physical over-rotation**. | The error cannot be *found* on an `rz`. It can only be **injected deterministically** by compiling `rz((1+eps)a + phi)` in place of `rz(a)`. The injected values are then known to the experimenter (but withheld from the estimator). |
| RZZ cost blocks | Without fractional gates, `RZZ(theta)` is decomposed into CZ and single-qubit gates; the `theta`-dependence sits in a virtual `rz`. On Heron with fractional gates enabled, `RZZ(theta)` is a native pulse for `0 < theta <= pi/2`. | A *native* fractional `RZZ(theta)` is the only plausible physical carrier of an angle-dependent coherent error in this circuit family. Whether its error is angle-proportional is unknown (§8, option B). |
| RC labels (Pauli frames) | Implementable as Pauli gates or virtual frame updates; `X`/`Y` labels are physical gates with their own errors. | Not used in HW-P1: Gate 1A showed labels cannot identify `eps` at `phi = 0` even noiselessly. |
| P-amp sensor `CX - RZ((1+eps)a + phi) - CX`, control in `|0>`, target in `|+>` | Maps directly: CX becomes CZ plus single-qubit gates; `rz` is virtual; `<X>`, `<Y>` by basis rotation before readout. | Usable. Risk: the transpiler may simplify a CX whose control is `|0>`; barriers and an ISA check (§6) are required. |
| Visibility = 1 | Real readout error, T1/T2 during CZ and idles, leakage. | The frozen resource condition fails for visibility below 0.99263; a hardware pass is not expected and must not be presumed either way. |
| Shot noise only, i.i.d. shots | Drift, recalibration, crosstalk, and non-stationary readout. | Replicates must be interleaved in time; drift is a measured quantity. |
| Sensor and target share one `(eps, phi)` | True for the *injected* part by construction; real noise differs between sensor and target circuits. | Context mismatch becomes real and is part of what HW-P1 measures. |
| Fixed shot budget `N = 24,300` | Implementable exactly as shot counts; queue time and job overhead are outside `N`. | Ledger records shots per path and QPU usage separately. |

**Observed** in HW-P1: bitstring counts, job metadata, the backend calibration
snapshot. **Known by design but hidden from the estimator:** injected
`(eps, phi)`. **Latent:** native coherent errors (CZ phase, ZZ crosstalk),
per-circuit visibility, drift process, true readout channel (partly estimable
from calibration circuits). In the optional stage B, the correct candidate
`k*` is computed classically from the ideal circuit and used only for scoring.

## 2. Claims kept apart

- **Frozen study (unchanged):** in the synthetic compiled-angle model with
  shot noise only, P-amp identifies `(eps, phi)` with a 0.7% resource margin,
  Gate 2 is a formal pass without useful benefit selection, and Gate 3 fails.
- **HW-P1 question (new):** when a known compiled-angle error is injected on a
  real IBM processor, what are the P-amp standard error, bias, effective
  visibility, and drift at the frozen sensing budget `n_S = 2430`, and does
  the standard error meet the frozen threshold `0.0071429`?
- **Not a question of HW-P1:** whether IBM hardware *has* an angle-proportional
  error on `rz` (it cannot, `rz` being virtual), or whether the frozen policy
  "works on hardware".

## 3. Minimal design

### Stage A — P-amp under injected error (primary)

| Item | Proposal |
|---|---|
| Backend | One Heron-family QPU, chosen by the rules below, fixed for the whole stage. |
| Qubits | 2 (P-amp control and target), fixed by `initial_layout`. |
| Selection rule | At lock time, from the calibration snapshot: among connected pairs, minimise `readout_error(control) + readout_error(target) + CZ_error(pair)`; exclude qubits flagged non-operational; record the full snapshot. |
| Circuits | 9 P-amp circuits (6 repetition, 3 echo) x 2 measurement bases = 18 settings, as frozen; depth after transpilation recorded. |
| Injected points | `(0,0)`, `(+0.02,0)`, `(-0.02,0)`, `(+0.04,+0.01)`, `(-0.04,-0.01)` (the Gate 3–4 grid). |
| Shots | 135 per setting, 2430 per estimate (as frozen). |
| Replication | 8 blocks; each block contains all 5 points in a seeded random order, plus 4 readout-calibration circuits (`00,01,10,11`, 1000 shots each) and one phase-insensitive control (P-amp measured in Z, 135 shots per point). |
| Totals | 5 x 8 x 2430 = 97,200 P-amp shots; 32,000 calibration shots; 5,400 control shots; about 134,600 shots, about 800 circuit instances, 8 jobs (one per block) in batch mode. |
| Transpilation | `optimization_level=1`, fixed `seed_transpiler`, barriers around each P-amp block, no approximation; dynamical decoupling and twirling **off**; injected angles applied before transpilation. |
| Primary analysis | Unmitigated counts. Secondary: readout-mitigated with the block's calibration matrix. Both reported. |

### Stage B — decision units (optional; separate approval after stage A)

2-qubit edge and 3-qubit path graphs at `p = 1`, 3 candidate pairs, injected
points `(0,0)`, `(0.02,0)`, `(0.04,0.01)`, 2 replicates: 18 units. Each unit
runs the full-target issue path (24,300 shots) and the sensor-allocation path
(2,430 P-amp + 10,934 initial + 10,936 corrected rerun), about 48,600 shots per
unit and about 875,000 shots in total. With one realised run per unit and 18
units, stage B is **descriptive only**: it can show whether corrected decisions
differ from issued ones under real noise, not estimate `Delta_V`.

## 4. Usage estimate (to be recomputed from transpiled circuits)

IBM bills QPU time; for standard QPU workloads 1 resource unit equals 1 minute
of QPU time. The documented local estimate is
`~2 s per sub-job + (rep_delay + circuit length) x executions`, with default
`rep_delay` 250 µs on most backends, and the quick form
`2 + 0.00035 x executions` seconds.

| Stage | Executions | Sub-jobs (est.) | Quick-form estimate | With 2x contingency |
|---|---:|---:|---:|---:|
| A | ~134,600 | 8 | ~63 s (~1.1 min) | ~2.2 min |
| B | ~875,000 | ~12 | ~330 s (~5.5 min) | ~11 min |
| A + B | | | ~6.6 min | ~13 min |

The Open Plan allows up to 10 minutes of QPU time per rolling 28-day window,
and dry-run jobs that report usage without charging it are available only on
Flex, Premium and On-Prem plans. On an Open Plan, stage A fits comfortably;
A + B with contingency does not fit one window. Set `max_execution_time` on
every job to cap overruns. Queue time is not billed but affects drift.

## 5. Controls, criteria, and stopping

- **Negative controls:** zero injection `(0,0)`; Z-basis P-amp (phase-blind, must
  show no dependence on the injected phase); sign-symmetric pairs
  `(+eps,+phi)` / `(-eps,-phi)` (estimates must flip sign).
- **Drift controls:** interleaved blocks; zero-injection estimate per block;
  calibration snapshot fetched before and after each job.
- **Pre-specified estimands (stage A, descriptive):**
  1. `SE_hw(eps_hat)` at 2430 shots, from the spread of the 8 block estimates
     at each point (pooled), with a block-bootstrap 95% interval;
  2. bias `mean(eps_hat - eps_inj)` and `mean(phi_hat - phi_inj)` per point;
  3. effective visibility `v_hat` from the amplitude `sqrt(<X>^2 + <Y>^2)` of each
     setting;
  4. drift: slope of the zero-injection estimates over blocks.
- **Outcome labels (fixed before data):** SE *meets* the frozen threshold if the
  upper interval end is below `0.0071429`; *fails* if the lower end is above it;
  otherwise *inconclusive*. Bias is *flagged* if its interval excludes zero by more
  than `0.0071429`. These labels describe HW-P1 only.
- **Validity checks (any failure voids the stage, reported, not rerun silently):**
  transpiled circuits pass the ISA/structure check of §6; readout assignment
  error on the chosen qubits below 5% in every block; the Z-basis control shows
  no phase dependence beyond its shot noise.
- **Stopping rule:** stop the stage and report if (a) the approved usage cap is
  reached; (b) the backend is recalibrated between blocks (record; restart only
  with new approval and a new snapshot); (c) a validity check fails; (d) stage A
  is complete — stage B never starts without a separate approval.

## 6. Dry-run and validation before any lock

1. **Noiseless check:** statevector simulation of the transpiled P-amp
   circuits reproduces the frozen phase model to `1e-12` at all injected points.
2. **ISA/structure check:** after transpiling against the chosen backend's
   target (offline, no execution), each P-amp circuit still contains its CZ
   gates and its injected `rz` angles up to frame merging (verified by
   noiseless equivalence of transpiled vs. intended circuits).
3. **Local pipeline checks:** (a) compare every Qiskit Statevector circuit
   against the analytic phase model; (b) run the complete eight-block estimator
   and reporting pipeline with deterministic binomial
   samples from an explicitly stated visibility/readout model. These are code
   smoke tests, never hardware results or a Heron model. A full backend-derived
   noisy simulation is deliberately omitted: it does not establish hardware
   behaviour and exceeded the practical local preflight budget. The real
   backend ISA and structure check remains mandatory after backend selection.
   Qiskit Aer and IBM Runtime native extensions are blocked by Windows Smart
   App Control on the development machine; this is recorded in
   `ENVIRONMENT_NOTES.md` and must not be described as a passed fake-backend
   check.
4. **Count and usage:** script that prints circuits, shots, sub-jobs and the
   usage estimate from the transpiled circuits.
5. **Lock:** lock template v2 record with code, environment (Python, qiskit,
   qiskit-ibm-runtime versions), seeds (`SHA256("hwp1|" + key)`), command,
   absent output directory, and post-run artifact hashes (raw counts with job
   IDs, calibration snapshots, analysis outputs).

## 7. Artifacts

`followup/ibm-hardware-pilot/` will hold: this protocol (frozen at lock), the
circuit builder, the runner, the analysis script, `requirements.txt` with exact
versions, the lock record, and after execution `results/` with raw counts, job
IDs, backend snapshots, analysis JSON, and a SHA-256 manifest. Nothing is
written into the frozen study's directories.

## 8. If the angle-proportional model does not fit the hardware

- **Option A (this draft): injected error.** The estimand changes from
  "a physical compiled-angle error" to "a known compiled-angle perturbation under
  real noise". This tests sensing and correction under real noise; it cannot show
  that such an error occurs naturally.
- **Option B: native fractional `RZZ(theta)` characterisation.** With fractional
  gates enabled on a Heron QPU, amplify `RZZ(theta)` (repetitions and echoes) at
  several angles in `(0, pi/2]` and fit the angle dependence of its coherent
  error. Estimand: the fitted error curve `delta(theta)`, with no assumption that
  it is proportional to `theta`. This is a **new research question**
  (characterisation), and only if it finds an angle-proportional component would
  a decision study on that carrier make sense.
- **Option C: stop at simulation** if neither option is approved.

## 9. Decisions needed from the owner before the lock

1. Plan and cap: Open Plan (10 min per 28 days) or a paid plan; maximum QPU
   minutes approved for HW-P1.
2. Option A (injected), option B (fractional `RZZ`), or both in sequence.
3. Stage A only, or A then B (B needs about 5.5–11 more minutes).
4. Backend family and whether to allow fractional gates.
5. Number of blocks (8 proposed; 4 halves usage and widens intervals).
6. Primary analysis unmitigated (proposed) or readout-mitigated.
7. Whether to deposit the locked protocol with an independent timestamp (for
   example a Zenodo record) before execution, which is the only way HW-P1 could
   later be called preregistered.
8. Who reviews the lock (E005 §5 asks for a written review note).

## Sources

- IBM Quantum documentation: fractional gates (`RZZ(theta)` for
  `0 < theta <= pi/2`, `RX(theta)`, Heron only):
  https://quantum.cloud.ibm.com/docs/en/guides/fractional-gates
- Qiskit `RZGate` documentation (virtual frame change, zero error and duration):
  https://docs.quantum.ibm.com/api/qiskit/0.37/qiskit.circuit.library.RZGate
- Workload usage and local estimate:
  https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time
- Plans, resource units, dry-run availability, Open Plan allowance:
  https://quantum.cloud.ibm.com/docs/guides/plans-overview
- Repetition delay: https://quantum.cloud.ibm.com/docs/en/guides/repetition-rate-execution

Checked on 2026-11-23; plans, limits and defaults change and must be rechecked
at lock time.
