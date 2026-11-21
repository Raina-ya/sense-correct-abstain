"""Execute the pre-data-locked Gate-2 development study once."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate2 import (  # noqa: E402
    BETA_VALUES,
    EPSILON_VALUES,
    GAMMA_PAIRS,
    GAMMA_VALUES,
    GRAPHS,
    PHI_VALUES,
    estimate_from_xy,
    expected_score,
    nearest_clifford,
    partition,
    score_distribution,
    score_variance,
    seed_for,
    target_probabilities,
    unit_key,
)
from sense_correct_abstain.pamp import M_VALUES, THETA_VALUES  # noqa: E402


LOCK_COMMIT = "38d900dbeef3f9e468aed8e21377c1aba59c8c20"
SENSOR_SHOTS = 2430
INITIAL_PER_CANDIDATE = 5467
CORRECTED_PER_CANDIDATE = 5468
PAMP_SETTING_SHOTS = 135
SCORING_REPLICATES = 256
SE_EPSILON = 0.007090190179103527
SE_PHI = 0.002541716727064875


def rng(key: str, stream: str) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed_for(key, stream)))


def sample_mean(key: str, stream: str, distribution, shots: int) -> tuple[float, float]:
    counts = rng(key, stream).multinomial(shots, distribution)
    values = np.arange(len(distribution), dtype=float) / (len(distribution) - 1)
    mean = float(counts @ values / shots)
    variance = float(counts @ ((values - mean) ** 2) / max(1, shots - 1))
    return mean, variance


def scoring_accuracy(key: str, stream: str, distributions, shots: int, ideal_a: bool) -> float:
    correct = 0
    values = np.arange(len(distributions[0]), dtype=float) / (len(distributions[0]) - 1)
    for replicate in range(SCORING_REPLICATES):
        mean_a = float(rng(key, f"{stream}-A|{replicate}").multinomial(shots, distributions[0]) @ values / shots)
        mean_b = float(rng(key, f"{stream}-B|{replicate}").multinomial(shots, distributions[1]) @ values / shots)
        selected_a = mean_a >= mean_b
        correct += selected_a == ideal_a
    return correct / SCORING_REPLICATES


def sample_expectation(generator: np.random.Generator, expectation: float) -> float:
    probability = min(1.0, max(0.0, (1 + expectation) / 2))
    successes = generator.binomial(PAMP_SETTING_SHOTS, probability)
    return 2 * successes / PAMP_SETTING_SHOTS - 1


def pamp_estimate(key: str, epsilon: float, phi: float, *, asymmetric: bool = False):
    generator = rng(key, "pamp-asymmetric" if asymmetric else "pamp")
    repetitions = []
    for theta in THETA_VALUES:
        for m in M_VALUES:
            phase = m * theta + m * (epsilon * theta + phi)
            repetitions.append((sample_expectation(generator, math.cos(phase)),
                                sample_expectation(generator, math.sin(phase))))
    echoes = []
    for m in M_VALUES:
        phase = 0.0 if asymmetric else 2 * m * phi
        echoes.append((sample_expectation(generator, math.cos(phase)),
                       sample_expectation(generator, math.sin(phase))))
    try:
        epsilon_hat, phi_hat = estimate_from_xy(repetitions, echoes)
    except ValueError:
        return None
    unambiguous = all(16 * abs(epsilon_hat * theta + phi_hat) < math.pi / 2
                      for theta in THETA_VALUES) and 32 * abs(phi_hat) < math.pi / 2
    return epsilon_hat, phi_hat, unambiguous


def balanced_accuracy(rows, prediction_field: str, baseline_positive: bool) -> tuple[float, float, int, int]:
    positives = [row for row in rows if row["benefit_positive"]]
    negatives = [row for row in rows if not row["benefit_positive"]]
    if not positives or not negatives:
        return float("nan"), float("nan"), len(positives), len(negatives)
    sensitivity = sum(row[prediction_field] for row in positives) / len(positives)
    specificity = sum(not row[prediction_field] for row in negatives) / len(negatives)
    rule = (sensitivity + specificity) / 2
    baseline_sensitivity = float(baseline_positive)
    baseline_specificity = float(not baseline_positive)
    return rule, (baseline_sensitivity + baseline_specificity) / 2, len(positives), len(negatives)


def evaluate(rows, field: str, baseline_positive: bool):
    full, baseline, positives, negatives = balanced_accuracy(rows, field, baseline_positive)
    improvements = {"full": full - baseline}
    for graph in GRAPHS:
        subset = [row for row in rows if row["graph"] != graph.name]
        rule, base, _, _ = balanced_accuracy(subset, field, baseline_positive)
        improvements[f"leave_out_{graph.name}"] = rule - base
    return {
        "balanced_accuracy": full,
        "baseline_balanced_accuracy": baseline,
        "improvement": improvements["full"],
        "robustness_lower_bound": min(improvements.values()),
        "positive_units": positives,
        "negative_units": negatives,
        "leave_one_graph_out": improvements,
    }


def simulate_unit(graph, beta_i, gamma_i, gamma_j, epsilon_i, phi_i):
    key = unit_key(graph, beta_i, gamma_i, gamma_j, epsilon_i, phi_i)
    beta = BETA_VALUES[beta_i]
    gammas = (GAMMA_VALUES[gamma_i], GAMMA_VALUES[gamma_j])
    epsilon, phi = EPSILON_VALUES[epsilon_i], PHI_VALUES[phi_i]
    ideal_dist = tuple(score_distribution(graph, target_probabilities(graph, beta, gamma, 0.0, 0.0))
                       for gamma in gammas)
    ideal_means = tuple(expected_score(graph, dist) for dist in ideal_dist)
    if abs(ideal_means[0] - ideal_means[1]) < 1e-12:
        return {"key": key, "graph": graph.name, "partition": partition(key), "evaluable": False,
                "reason": "ideal_gap_tie"}
    ideal_a = ideal_means[0] > ideal_means[1]
    initial_dist = tuple(score_distribution(graph, target_probabilities(graph, beta, gamma, epsilon, phi))
                         for gamma in gammas)
    initial_samples = tuple(sample_mean(key, f"initial-{label}", dist, INITIAL_PER_CANDIDATE)
                            for label, dist in zip(("A", "B"), initial_dist, strict=True))
    g0_hat = initial_samples[0][0] - initial_samples[1][0]

    estimate = pamp_estimate(key, epsilon, phi)
    if estimate is None:
        epsilon_hat = phi_hat = float("nan")
        unambiguous = False
        corrected_dist = initial_dist
    else:
        epsilon_hat, phi_hat, unambiguous = estimate
        corrected_gammas = tuple(((2 * gamma - phi_hat) / (1 + epsilon_hat)) / 2 for gamma in gammas)
        corrected_dist = tuple(score_distribution(
            graph, target_probabilities(graph, beta, gamma, epsilon, phi)) for gamma in corrected_gammas)
    significant = estimate is not None and (
        abs(epsilon_hat) > 1.96 * SE_EPSILON or abs(phi_hat) > 1.96 * SE_PHI)
    angle_sum = 2 * len(graph.edges) * (abs(gammas[0]) + abs(gammas[1]))
    rotation_count = 2 * len(graph.edges)
    bound = angle_sum * abs(epsilon_hat) + rotation_count * abs(phi_hat) if estimate else float("nan")
    pamp_prediction = bool(estimate and unambiguous and significant and g0_hat != 0 and abs(g0_hat) <= bound)

    no_action_accuracy = scoring_accuracy(key, "scoring-initial", initial_dist, INITIAL_PER_CANDIDATE, ideal_a)
    corrected_accuracy = scoring_accuracy(key, "scoring-corrected", corrected_dist, CORRECTED_PER_CANDIDATE, ideal_a)
    benefit = corrected_accuracy - no_action_accuracy

    twin_beta = nearest_clifford(2 * beta) / 2
    twin_gammas = tuple(nearest_clifford(2 * gamma) / 2 for gamma in gammas)
    twin_ideal = tuple(score_distribution(graph, target_probabilities(graph, twin_beta, gamma, 0.0, 0.0))
                       for gamma in twin_gammas)
    twin_noisy = tuple(score_distribution(graph, target_probabilities(graph, twin_beta, gamma, epsilon, phi))
                       for gamma in twin_gammas)
    p2_samples = tuple(sample_mean(key, f"p2-{label}", dist, SENSOR_SHOTS // 2)
                       for label, dist in zip(("A", "B"), twin_noisy, strict=True))
    twin_observed_gap = p2_samples[0][0] - p2_samples[1][0]
    twin_ideal_gap = expected_score(graph, twin_ideal[0]) - expected_score(graph, twin_ideal[1])
    p2_alarm = abs(twin_observed_gap - twin_ideal_gap)
    p2_se = math.sqrt(p2_samples[0][1] / (SENSOR_SHOTS // 2) + p2_samples[1][1] / (SENSOR_SHOTS // 2))
    p2_prediction = p2_alarm > 1.96 * p2_se and g0_hat != 0 and abs(g0_hat) <= p2_alarm

    asymmetric = pamp_estimate(key, epsilon, phi, asymmetric=True)
    return {
        "key": key,
        "graph": graph.name,
        "partition": partition(key),
        "evaluable": True,
        "epsilon": epsilon,
        "phi": phi,
        "ideal_gap": ideal_means[0] - ideal_means[1],
        "initial_gap_observed": g0_hat,
        "epsilon_hat": epsilon_hat,
        "phi_hat": phi_hat,
        "pamp_unambiguous": unambiguous,
        "instability_bound": bound,
        "pamp_prediction": pamp_prediction,
        "p2_alarm": p2_alarm,
        "p2_prediction": p2_prediction,
        "no_action_correct_probability": no_action_accuracy,
        "corrected_correct_probability": corrected_accuracy,
        "correction_benefit": benefit,
        "benefit_positive": benefit > 0,
        "asymmetric_epsilon_hat": asymmetric[0] if asymmetric else None,
        "asymmetric_phi_hat": asymmetric[1] if asymmetric else None,
    }


def report_markdown(result):
    primary = result["primary"]
    p2 = result["p2"]
    return f"""# Gate 2 development report

**Run time (UTC):** {result['run_utc']}

**Gate 2 lock commit:** `{result['lock_commit']}`

**Evidence:** development-only synthetic noisy simulation; no holdout and no hardware.

## Verdict

**Gate 2 {result['verdict'].upper()}.** The frozen P-amp transfer rule had balanced accuracy `{primary['balanced_accuracy']:.4f}` versus `{primary['baseline_balanced_accuracy']:.4f}` for the frozen no-information baseline. Its full improvement was `{primary['improvement']:.4f}` and its leave-one-graph-out robustness lower bound was `{primary['robustness_lower_bound']:.4f}`; passage required positive full improvement and a lower bound of at least `0.05`.

## Evaluation population

- Generated units: {result['counts']['generated']}.
- Evaluable units: {result['counts']['evaluable']}.
- Rule-development / evaluation: {result['counts']['rule_development']} / {result['counts']['evaluation']}.
- Evaluation positives / negatives: {primary['positive_units']} / {primary['negative_units']}.
- Frozen baseline prediction: {'positive' if result['baseline_positive'] else 'nonpositive'} correction benefit.

## Same-budget P2 comparator

P2 balanced accuracy was `{p2['balanced_accuracy']:.4f}`, full improvement `{p2['improvement']:.4f}`, and robustness lower bound `{p2['robustness_lower_bound']:.4f}`. P2 is a comparator only and cannot rescue the primary verdict.

## Failure separation and controls

- Undefined or ideal-tie units are retained in the machine-readable artifact.
- P-amp estimation/ambiguity failures: {result['failures']['pamp']}.
- Matched-null units: {result['controls']['matched_null_units']}.
- The asymmetric-negative-angle control is scoring-only and did not contribute to the verdict; its mean absolute `phi` estimation error was `{result['controls']['asymmetric_phi_mae']:.6f}`.
- Every shot is charged under the frozen `24,300`-shot ledger. Net policy value is not tested here.

## Claim boundary and routing

This result concerns decision relevance only in the locked synthetic development model. It does not establish net value, action non-degeneracy, confirmatory generalization, device realism, or hardware benefit.

Route: **{result['routing']}**.
"""


def main():
    output = ROOT / "results" / "dev"
    report = ROOT / "docs" / "results" / "gate2_report.md"
    if output.exists() or report.exists():
        raise SystemExit("Gate 2 artifacts already exist; refusing to rerun")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != LOCK_COMMIT:
        raise SystemExit(f"Gate 2 requires lock commit {LOCK_COMMIT}; found {head}")
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_gate2_lock.py")], check=True)

    rows = []
    for graph in GRAPHS:
        for beta_i in range(len(BETA_VALUES)):
            for gamma_i, gamma_j in GAMMA_PAIRS:
                for epsilon_i in range(len(EPSILON_VALUES)):
                    for phi_i in range(len(PHI_VALUES)):
                        rows.append(simulate_unit(graph, beta_i, gamma_i, gamma_j, epsilon_i, phi_i))
        print(f"completed {graph.name}: {len(rows)} units", flush=True)

    evaluable = [row for row in rows if row["evaluable"]]
    development = [row for row in evaluable if row["partition"] == "rule-development"]
    evaluation = [row for row in evaluable if row["partition"] == "evaluation"]
    baseline_positive = sum(row["benefit_positive"] for row in development) > len(development) / 2
    primary = evaluate(evaluation, "pamp_prediction", baseline_positive)
    p2 = evaluate(evaluation, "p2_prediction", baseline_positive)
    class_counts_ok = primary["positive_units"] >= 20 and primary["negative_units"] >= 20
    passed = class_counts_ok and primary["improvement"] > 0 and primary["robustness_lower_bound"] >= 0.05
    asymmetric_errors = [abs(row["asymmetric_phi_hat"] - row["phi"]) for row in evaluable
                         if row["asymmetric_phi_hat"] is not None]
    result = {
        "schema": "gate2_development_v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "lock_commit": LOCK_COMMIT,
        "numpy_version": np.__version__,
        "budget": {"total": 24300, "sensor": 2430, "initial": 10934, "reserve": 10936},
        "counts": {
            "generated": len(rows),
            "evaluable": len(evaluable),
            "rule_development": len(development),
            "evaluation": len(evaluation),
        },
        "baseline_positive": baseline_positive,
        "primary": primary,
        "p2": p2,
        "failures": {"pamp": sum(not row.get("pamp_unambiguous", False) for row in evaluable)},
        "controls": {
            "matched_null_units": sum(row.get("epsilon") == 0 and row.get("phi") == 0 for row in evaluable),
            "asymmetric_phi_mae": sum(asymmetric_errors) / len(asymmetric_errors),
        },
        "verdict": "pass" if passed else "fail",
        "routing": "Gate3/Gate4" if passed else "Stop-after-Gate2",
        "units": rows,
    }
    output.mkdir(parents=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    (output / "gate2_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report.write_text(report_markdown(result), encoding="utf-8")
    print(f"Gate 2 complete: {result['verdict'].upper()}; route to {result['routing']}")


if __name__ == "__main__":
    main()
