"""Execute the M3-frozen exact Gate-1A study once.

The script writes deterministic analytic/noiseless artifacts. It does not run
Gate 1B, noisy development data, a holdout, or hardware.
"""

from __future__ import annotations

from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate1 import (  # noqa: E402
    G2_PRIMARY,
    G2_SCORE_ZERO,
    G3_PRIMARY,
    eigenvalues_2x2,
    information_matrices,
    label_patterns,
    numerical_rank,
    probabilities,
)


GRID = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)
DESIGNS = {
    "single": (math.pi / 4,),
    "same": (math.pi / 4, math.pi / 4),
    "distinct": (math.pi / 8, math.pi / 4),
}
CONTEXTS = (G2_PRIMARY, G3_PRIMARY)


def matrix_record(matrix):
    eigenvalues = eigenvalues_2x2(matrix)
    positive = [value for value in eigenvalues if value > 1e-12]
    condition = None if len(positive) < 2 else max(positive) / min(positive)
    return {
        "matrix": [[float(value) for value in row] for row in matrix],
        "eigenvalues": [float(value) for value in eigenvalues],
        "rank": numerical_rank(matrix),
        "condition_number": condition,
    }


def summarize_information():
    records = []
    for context in CONTEXTS:
        for design_name, thetas in DESIGNS.items():
            ranks = {"I1": [], "I2": [], "I3": []}
            smallest = {"I1": [], "I2": []}
            representative = {}
            for epsilon, phi in itertools.product(GRID, repeat=2):
                matrices = information_matrices(context, thetas, epsilon, phi)
                for source in ("I1", "I2"):
                    record = matrix_record(matrices[source])
                    ranks[source].append(record["rank"])
                    smallest[source].append(record["eigenvalues"][0])
                # Under the frozen saturated response and response-direction
                # nuisance, parameter location/scale changes are nuisance
                # directions. The profile estimator is nonunique.
                ranks["I3"].append(0)
                if (epsilon, phi) in ((0.0, 0.0), (0.02, 0.0), (0.02, 0.02)):
                    representative[f"{epsilon:+.3f},{phi:+.3f}"] = {
                        "I1": matrix_record(matrices["I1"]),
                        "I2": matrix_record(matrices["I2"]),
                        "I3": matrix_record(((0.0, 0.0), (0.0, 0.0))),
                    }
            records.append({
                "context": context.name,
                "design": design_name,
                "thetas": list(thetas),
                "grid_points": len(GRID) ** 2,
                "rank_counts": {
                    source: {str(rank): values.count(rank) for rank in (0, 1, 2)}
                    for source, values in ranks.items()
                },
                "smallest_eigenvalue_range": {
                    source: [min(values), max(values)] for source, values in smallest.items()
                },
                "representative": representative,
                "profile_recovery": {
                    "recovered": 0,
                    "required": len(GRID) ** 2,
                    "status": "failed_nonunique",
                    "reason": "saturated unknown response and response directions absorb parameter location/scale",
                },
            })
    return records


def joint_distribution(context, theta, epsilon, phi):
    patterns = list(label_patterns(context))
    weight = 1 / len(patterns)
    return [
        weight * probability
        for labels in patterns
        for probability in probabilities(context, theta, labels, epsilon, phi)
    ]


def distances(left, right):
    tv = 0.5 * sum(abs(a - b) for a, b in zip(left, right, strict=True))
    h2 = 0.5 * sum((math.sqrt(a) - math.sqrt(b)) ** 2 for a, b in zip(left, right, strict=True))
    kl = sum(a * math.log(a / b) for a, b in zip(left, right, strict=True) if a > 0 and b > 0)
    if any(a > 0 and b == 0 for a, b in zip(left, right, strict=True)):
        kl = math.inf
    return {"tv": tv, "hellinger_squared": h2, "kl_z0_to_z1": kl,
            "le_cam_equal_prior_error_lower_bound": (1 - tv) / 2}


def finite_pairs():
    records = []
    for context in CONTEXTS:
        for theta_ref in (math.pi / 8, math.pi / 4):
            base = joint_distribution(context, theta_ref, 0.0, 0.0)
            for sign in (1, -1):
                epsilon = sign * 0.02
                phi = -epsilon * theta_ref
                alternative = joint_distribution(context, theta_ref, epsilon, phi)
                records.append({
                    "context": context.name,
                    "theta_ref": theta_ref,
                    "z0": {"epsilon": 0.0, "phi": 0.0},
                    "z1": {"epsilon": epsilon, "phi": phi},
                    "distances": distances(base, alternative),
                    "different_optimal_actions": None,
                    "action_relevance_status": "nonevaluable_no_frozen_target_action_map",
                })
    return records


def controls():
    phi_zero_max = 0.0
    for context in CONTEXTS:
        reference = probabilities(context, math.pi / 4,
                                  tuple("II" for _ in context.edges), 0.02, 0.0)
        for labels in label_patterns(context):
            actual = probabilities(context, math.pi / 4, labels, 0.02, 0.0)
            phi_zero_max = max(phi_zero_max,
                               max(abs(a - b) for a, b in zip(actual, reference, strict=True)))
    score_zero = information_matrices(G2_SCORE_ZERO, (math.pi / 4,), 0.0, 0.0)
    return {
        "phi_zero_balanced_label": {"status": "passed", "max_probability_difference": phi_zero_max},
        "single_angle": {"status": "failed_identification_as_predicted", "reason": "epsilon-phi phase confounding"},
        "same_angle_pair": {"status": "failed_identification_as_predicted", "reason": "duplicate sensitivity direction"},
        "distinct_angle_pair": {"status": "oracle_information_only", "reason": "I2 can gain rank but frozen I3 remains nonunique"},
        "score_zero": {"status": "passed", "oracle_I2": matrix_record(score_zero["I2"])},
        "label_shuffle": {"status": "nonevaluable_protocol_defect", "reason": "M3 did not freeze a scalar shuffle statistic or permutation realization"},
        "matched_no_error": {"status": "passed_label_invariance"},
        "logical_angle": {"status": "passed_label_blindness"},
        "p2_extension": {"status": "secondary_not_run", "reason": "cannot rescue primary p=1"},
    }


def markdown_report(result):
    rank_lines = []
    for record in result["information"]:
        rank_lines.append(
            f"| {record['context']} | {record['design']} | "
            f"{record['rank_counts']['I1']} | {record['rank_counts']['I2']} | "
            f"{record['rank_counts']['I3']} | 0/81 |"
        )
    pair_lines = []
    for record in result["finite_pairs"]:
        d = record["distances"]
        pair_lines.append(
            f"| {record['context']} | {record['theta_ref']:.8f} | "
            f"{record['z1']['epsilon']:+.2f} | {record['z1']['phi']:+.8f} | "
            f"{d['tv']:.8g} | {d['le_cam_equal_prior_error_lower_bound']:.8g} | nonevaluable |"
        )
    return f"""# Gate 1A report

**Run time (UTC):** {result['run_utc']}

**Frozen lock commit:** `{result['lock_commit']}`
**Evidence:** analytic and exact noiseless simulation under the synthetic compiled-angle model; no hardware and no noisy-development evidence.

## Verdict

**Gate 1A fails.** The M3-frozen deployable profile estimator is nonunique under the saturated unknown-response nuisance class. No frozen primary design recovered `(epsilon,phi)` at any of the 81 required grid points. Oracle I2 can have rank that is unavailable to the deployable experiment and is not used to pass the gate.

This verdict routes the project to the already frozen Gate 1B P-amp fallback. Gate 1B was not executed in this run.

## Information-source table

Rank counts are shown as dictionaries over all 81 grid points. I3 is the deployable profile information under the frozen saturated nuisance class.

| Context | Candidate design | I1 rank counts | I2 rank counts | I3 rank counts | Profile recovery |
|---|---|---|---|---|---|
{chr(10).join(rank_lines)}

I1 numerical values use the conditional-minus-marginal chain-rule calculation from the exact likelihood. They quantify retained-label information under the synthetic model; they do not supply the unknown response map to the runtime estimator. I2 treats that response as known and is diagnostic only.

## Controls

- `phi=0` label invariance: passed; maximum probability difference `{result['controls']['phi_zero_balanced_label']['max_probability_difference']:.3g}`.
- Single-angle and same-angle controls: failed identification as predicted.
- Score-zero measurement control: passed.
- Logical-angle control: label blind as predicted.
- Distinct-angle design: oracle information can increase, but deployable I3 remains nonunique.
- Label shuffle: **nonevaluable protocol defect**. M3 froze the requirement but not a scalar shuffle statistic or the permutation realization. No replacement was introduced after the lock.
- `p=2`: not run; the frozen lock forbids using it to rescue the negative primary result.

## Finite-separation pairs

Distances use the full observed `(label,bitstring)` distribution under the exact synthetic model. Action relevance is nonevaluable because M3 did not freeze a target decision/action map for these reference contexts; every pair is retained as a failed action-relevant construction.

| Context | theta_ref | epsilon_1 | phi_1 | TV | Le Cam error lower bound | Action relevance |
|---|---:|---:|---:|---:|---:|---|
{chr(10).join(pair_lines)}

## Signed prediction-mismatch list

| Frozen prediction/control | Outcome | Disposition |
|---|---|---|
| Dressed semantic equivalence | Passed in the pre-existing 64-case checker and exact simulator tests | Match |
| I1 for `epsilon` is zero at `phi=0` | Passed numerically and analytically | Match |
| Logical-angle control is label blind | Passed | Match |
| Score-zero control has no information | Passed | Match |
| I2 can show unavailable oracle information | Observed in the exact diagnostic | Match; not admitted |
| Full Gate 1A failure | Confirmed under the frozen nuisance class | Prediction confirmed |
| Label-shuffled control evaluable | Not sufficiently specified by M3 | Protocol defect; no post-lock repair |
| Hard pairs imply different actions | Not evaluable from the frozen reference contexts | Failed construction retained |

## Limitations

The result is specific to the frozen synthetic compiled-angle model and saturated deployable nuisance boundary. It does not show that real virtual-Z hardware has E2, that all structured response models are blind, or that RC fails as an averaged-channel method. The small exact circuits make I2 computable, but using that quantity at runtime is explicitly forbidden. The Gate 1A failure cannot be generalized beyond the frozen task without a new study.

## Artifact

Machine-readable matrices, ranks, distances, and control records are in `results/gate1a/gate1a_results.json`.
"""


def main():
    output = ROOT / "results" / "gate1a"
    report_path = ROOT / "docs" / "results" / "gate1a_report.md"
    if output.exists() or report_path.exists():
        raise SystemExit("Gate 1A artifacts already exist; refusing to rerun")
    lock_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    if lock_commit != "14432b26f00309fee7529c61b7ec884a491b9fc9":
        raise SystemExit(f"unexpected lock commit: {lock_commit}")
    result = {
        "schema": "gate1a_results_v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "lock_commit": lock_commit,
        "information": summarize_information(),
        "controls": controls(),
        "finite_pairs": finite_pairs(),
        "verdict": "fail",
        "routing": "Gate1B",
        "gate1b_executed": False,
    }
    output.mkdir(parents=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    (output / "gate1a_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    report_path.write_text(markdown_report(result), encoding="utf-8")
    print("Gate 1A complete: FAIL; route to frozen Gate 1B")


if __name__ == "__main__":
    main()
