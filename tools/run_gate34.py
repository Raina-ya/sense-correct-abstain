"""Execute the pre-data-locked M6 Gate-3/4 split-99 study once."""

from __future__ import annotations

from collections import Counter
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
    GAMMA_VALUES,
    estimate_from_xy,
    expected_score,
    score_distribution,
    target_probabilities,
)
from sense_correct_abstain.gate34 import (  # noqa: E402
    ERROR_POINTS,
    GAMMA_PAIR_INDICES,
    global_seed,
    policy_action,
    quantile_linear,
    seed_for,
    split99_graphs,
    unit_key,
)
from sense_correct_abstain.pamp import M_VALUES, THETA_VALUES  # noqa: E402


LOCK_COMMIT = "2dd9e2aec2ed185e40ef42448cd2ba41aa9d95a6"
PAMP_SETTING_SHOTS = 135
INITIAL_SHOTS = 5467
CORRECTED_SHOTS = 5468
FULL_TARGET_SHOTS = 12150
SCORING_REPLICATES = 256
PRIMARY_LAMBDA = 0.25
COMPARATOR_PRIORITY = ("N-full", "N-sensor-allocation", "C-always", "A-always")


def rng(key: str, stream: str) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed_for(key, stream)))


def sample_mean(key: str, stream: str, distribution, shots: int) -> tuple[float, float]:
    counts = rng(key, stream).multinomial(shots, distribution)
    values = np.arange(len(distribution), dtype=float) / (len(distribution) - 1)
    mean = float(counts @ values / shots)
    variance = float(counts @ ((values - mean) ** 2) / max(1, shots - 1))
    return mean, variance


def scoring_accuracy(key: str, stream: str, distributions, shots: int, ideal_a: bool) -> float:
    values = np.arange(len(distributions[0]), dtype=float) / (len(distributions[0]) - 1)
    correct = 0
    for replicate in range(SCORING_REPLICATES):
        mean_a = float(rng(key, f"{stream}-A|{replicate}").multinomial(shots, distributions[0]) @ values / shots)
        mean_b = float(rng(key, f"{stream}-B|{replicate}").multinomial(shots, distributions[1]) @ values / shots)
        correct += (mean_a >= mean_b) == ideal_a
    return correct / SCORING_REPLICATES


def sample_expectation(generator: np.random.Generator, expectation: float) -> float:
    probability = min(1.0, max(0.0, (1 + expectation) / 2))
    successes = generator.binomial(PAMP_SETTING_SHOTS, probability)
    return 2 * successes / PAMP_SETTING_SHOTS - 1


def pamp_estimate(key: str, epsilon: float, phi: float):
    generator = rng(key, "pamp")
    repetitions = []
    for theta in THETA_VALUES:
        for m in M_VALUES:
            phase = m * theta + m * (epsilon * theta + phi)
            repetitions.append((sample_expectation(generator, math.cos(phase)),
                                sample_expectation(generator, math.sin(phase))))
    echoes = []
    for m in M_VALUES:
        phase = 2 * m * phi
        echoes.append((sample_expectation(generator, math.cos(phase)),
                       sample_expectation(generator, math.sin(phase))))
    try:
        epsilon_hat, phi_hat = estimate_from_xy(repetitions, echoes)
    except ValueError:
        return None
    unambiguous = all(16 * abs(epsilon_hat * theta + phi_hat) < math.pi / 2
                      for theta in THETA_VALUES) and 32 * abs(phi_hat) < math.pi / 2
    return epsilon_hat, phi_hat, unambiguous


def simulate_unit(cluster_id, graph, beta_i, gamma_i, gamma_j, error_i):
    key = unit_key(cluster_id, beta_i, gamma_i, gamma_j, error_i)
    beta = BETA_VALUES[beta_i]
    gammas = (GAMMA_VALUES[gamma_i], GAMMA_VALUES[gamma_j])
    epsilon, phi = ERROR_POINTS[error_i]
    partition = "policy-lock" if cluster_id < 33 else "evaluation"
    ideal_dist = tuple(score_distribution(graph, target_probabilities(graph, beta, gamma, 0.0, 0.0))
                       for gamma in gammas)
    ideal_means = tuple(expected_score(graph, distribution) for distribution in ideal_dist)
    ideal_gap = ideal_means[0] - ideal_means[1]
    if abs(ideal_gap) < 1e-12:
        return {"key": key, "cluster_id": cluster_id, "graph": graph.name,
                "partition": partition, "evaluable": False, "reason": "ideal_gap_tie"}
    ideal_a = ideal_gap > 0

    initial_dist = tuple(score_distribution(graph, target_probabilities(graph, beta, gamma, epsilon, phi))
                         for gamma in gammas)
    initial_samples = tuple(sample_mean(key, f"initial-{label}", distribution, INITIAL_SHOTS)
                            for label, distribution in zip(("A", "B"), initial_dist, strict=True))
    g0_hat = initial_samples[0][0] - initial_samples[1][0]
    se_g0 = math.sqrt(initial_samples[0][1] / INITIAL_SHOTS + initial_samples[1][1] / INITIAL_SHOTS)
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
    angle_sum = 2 * len(graph.edges) * (abs(gammas[0]) + abs(gammas[1]))
    rotation_count = 2 * len(graph.edges)
    instability_bound = (angle_sum * abs(epsilon_hat) + rotation_count * abs(phi_hat)
                         if estimate else float("nan"))
    action = policy_action(
        estimate_defined=estimate is not None,
        unambiguous=unambiguous,
        epsilon_hat=epsilon_hat,
        phi_hat=phi_hat,
        g0_hat=g0_hat,
        se_g0=se_g0,
        instability_bound=instability_bound,
    )

    sensor_accuracy = scoring_accuracy(key, "scoring-sensor", initial_dist, INITIAL_SHOTS, ideal_a)
    full_accuracy = scoring_accuracy(key, "scoring-full", initial_dist, FULL_TARGET_SHOTS, ideal_a)
    corrected_accuracy = (scoring_accuracy(key, "scoring-corrected", corrected_dist,
                                           CORRECTED_SHOTS, ideal_a)
                          if estimate is not None and unambiguous else None)
    losses = {
        "N-full": 1 - full_accuracy,
        "N-sensor-allocation": 1 - sensor_accuracy,
        "C-always": 1 - corrected_accuracy if corrected_accuracy is not None else PRIMARY_LAMBDA,
        "A-always": PRIMARY_LAMBDA,
    }
    if action == "N":
        policy_loss = losses["N-sensor-allocation"]
    elif action == "C":
        policy_loss = losses["C-always"]
    else:
        policy_loss = PRIMARY_LAMBDA
    return {
        "key": key,
        "cluster_id": cluster_id,
        "graph": graph.name,
        "partition": partition,
        "evaluable": True,
        "epsilon": epsilon,
        "phi": phi,
        "ideal_gap": ideal_gap,
        "initial_gap_observed": g0_hat,
        "initial_gap_se": se_g0,
        "observed_tie": g0_hat == 0,
        "epsilon_hat": epsilon_hat,
        "phi_hat": phi_hat,
        "pamp_defined": estimate is not None,
        "pamp_unambiguous": unambiguous,
        "instability_bound": instability_bound,
        "action": action,
        "policy_loss": policy_loss,
        "fixed_losses": losses,
        "sensor_correct_probability": sensor_accuracy,
        "full_correct_probability": full_accuracy,
        "corrected_correct_probability": corrected_accuracy,
        "correction_failed": corrected_accuracy is None,
    }


def cluster_means(rows, value):
    by_cluster = {}
    for row in rows:
        by_cluster.setdefault(row["cluster_id"], []).append(value(row))
    return {cluster: sum(values) / len(values) for cluster, values in by_cluster.items()}


def alternative_loss(row, action: str, weight: float) -> float:
    if action == "A" or (action == "C" and row["correction_failed"]):
        return weight
    if action == "C":
        return 1 - row["corrected_correct_probability"]
    return 1 - row["sensor_correct_probability"]


def fixed_alternative_loss(row, comparator: str, weight: float) -> float:
    if comparator == "A-always" or (comparator == "C-always" and row["correction_failed"]):
        return weight
    if comparator == "C-always":
        return 1 - row["corrected_correct_probability"]
    if comparator == "N-full":
        return 1 - row["full_correct_probability"]
    return 1 - row["sensor_correct_probability"]


def report_markdown(result):
    gate3 = result["gate3"]
    gate4 = result["gate4"]
    comparator_rows = "\n".join(
        f"| {name} | {loss:.6f} | {'selected' if name == result['selected_comparator'] else ''} |"
        for name, loss in result["policy_lock_fixed_losses"].items()
    )
    action_rows = "\n".join(
        f"| {action} | {item['count']} | {item['frequency']:.4f} | {item['graph_clusters']} | {'yes' if item['clears'] else 'no'} |"
        for action, item in gate4["actions"].items()
    )
    return f"""# Gate 3 and Gate 4 development report

**Run time (UTC):** {result['run_utc']}

**M6 lock commit:** `{result['lock_commit']}`

**Evidence:** split-99 development simulation only; no confirmatory holdout and no hardware.

## Decisions

- **Gate 3: {gate3['verdict'].upper()}**. `Delta_V = {gate3['delta_v']:.6f}` and the frozen one-sided 95% graph-cluster bootstrap lower bound is `{gate3['lower_bound']:.6f}`.
- **Gate 4: {gate4['verdict'].upper()}**. {gate4['clearing_action_count']} actions clear both the 5% unit-frequency and 10-cluster requirements.
- Route: **{result['routing']}**.

## Fixed comparator selection

The comparator was selected only on the 33 policy-lock graph clusters.

| Fixed policy | Mean primary loss | Status |
|---|---:|---|
{comparator_rows}

Selected comparator: **{result['selected_comparator']}**.

## Gate 4 action frequencies

| Action | Units | Frequency | Graph clusters | Clears |
|---|---:|---:|---:|---|
{action_rows}

Observed policy-input gap ties: {gate4['observed_ties']}. Ties take the frozen abstain branch and do not count as evidence of non-degeneracy.

## Power and resource accounting

- Prospective 66-cluster power estimate from the 33 policy-lock clusters: `{result['power']['estimated_power']:.4f}`.
- Policy-lock cluster SD: `{result['power']['cluster_sd']:.6f}`.
- Approximate minimum detectable positive mean: `{result['power']['minimum_detectable_mean']:.6f}`.
- Generated / evaluable evaluation units: {result['counts']['evaluation_generated']} / {result['counts']['evaluation_evaluable']}.
- Infrastructure missing rate: `{result['counts']['infrastructure_missing_rate']:.4f}`.
- Budget: 24,300 shots per unit on every action path; classical computation is reported separately.

## Secondary loss sensitivity

| Abstention/failure weight | Delta_V |
|---:|---:|
| 0.10 | {result['sensitivity']['0.10']:.6f} |
| 0.50 | {result['sensitivity']['0.50']:.6f} |

These sensitivities cannot rescue or replace the primary result at weight 0.25.

## Claim boundary

The decisions are development evidence under the frozen synthetic model. They do not establish confirmatory generalization, physical-device realism, or hardware benefit. Proceeding to M7 is allowed only if both Gates pass and the required adversarial pre-data audit and independent registration are completed before any holdout is read.
"""


def main():
    output = ROOT / "results" / "gate34"
    report = ROOT / "docs" / "results" / "gate3_gate4_report.md"
    power_report = ROOT / "docs" / "freeze" / "power_analysis.md"
    if output.exists() or report.exists() or power_report.exists():
        raise SystemExit("M6 artifacts already exist; refusing to rerun")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != LOCK_COMMIT:
        raise SystemExit(f"M6 requires lock commit {LOCK_COMMIT}; found {head}")
    subprocess.run([sys.executable, str(ROOT / "tools" / "check_gate34_lock.py")], check=True)

    rows = []
    graphs = split99_graphs()
    for cluster_id, graph in enumerate(graphs):
        for beta_i in range(len(BETA_VALUES)):
            for gamma_i, gamma_j in GAMMA_PAIR_INDICES:
                for error_i in range(len(ERROR_POINTS)):
                    rows.append(simulate_unit(cluster_id, graph, beta_i, gamma_i, gamma_j, error_i))
        if (cluster_id + 1) % 11 == 0:
            print(f"completed {cluster_id + 1}/99 graph clusters", flush=True)

    evaluable = [row for row in rows if row["evaluable"]]
    lock_rows = [row for row in evaluable if row["partition"] == "policy-lock"]
    evaluation = [row for row in evaluable if row["partition"] == "evaluation"]
    fixed_losses = {name: sum(row["fixed_losses"][name] for row in lock_rows) / len(lock_rows)
                    for name in COMPARATOR_PRIORITY}
    issue_winner = min(COMPARATOR_PRIORITY[:2], key=lambda name: (fixed_losses[name], COMPARATOR_PRIORITY.index(name)))
    candidates = (issue_winner, "C-always", "A-always")
    selected = min(candidates, key=lambda name: (round(fixed_losses[name], 12), COMPARATOR_PRIORITY.index(name)))

    for row in evaluable:
        row["selected_fixed_loss"] = row["fixed_losses"][selected]
        row["delta"] = row["selected_fixed_loss"] - row["policy_loss"]

    lock_cluster = cluster_means(lock_rows, lambda row: row["delta"])
    evaluation_cluster = cluster_means(evaluation, lambda row: row["delta"])
    if len(evaluation_cluster) != 66:
        raise SystemExit(f"expected 66 evaluable graph clusters, found {len(evaluation_cluster)}")
    cluster_values = np.array(list(evaluation_cluster.values()))
    bootstrap_rng = np.random.Generator(np.random.PCG64(global_seed("cluster-bootstrap")))
    bootstrap_indices = bootstrap_rng.integers(0, len(cluster_values), size=(10000, len(cluster_values)))
    bootstrap_means = cluster_values[bootstrap_indices].mean(axis=1).tolist()
    lower_bound = quantile_linear(bootstrap_means, 0.05)
    delta_v = sum(row["delta"] for row in evaluation) / len(evaluation)
    missing = [row for row in rows if row.get("reason") == "infrastructure_missing"]
    evaluation_generated = sum(row["partition"] == "evaluation" for row in rows)
    missing_rate = sum(row.get("partition") == "evaluation" for row in missing) / evaluation_generated
    gate3_pass = delta_v > 0 and lower_bound > 0 and missing_rate <= 0.01

    action_counts = Counter(row["action"] for row in evaluation)
    action_clusters = {action: len({row["cluster_id"] for row in evaluation if row["action"] == action})
                       for action in ("N", "C", "A")}
    action_results = {}
    for action in ("N", "C", "A"):
        frequency = action_counts[action] / len(evaluation)
        clears = frequency >= 0.05 and action_clusters[action] >= 10
        action_results[action] = {"count": action_counts[action], "frequency": frequency,
                                  "graph_clusters": action_clusters[action], "clears": clears}
    clearing = sum(item["clears"] for item in action_results.values())
    gate4_pass = clearing >= 2

    lock_values = np.array(list(lock_cluster.values()))
    cluster_sd = float(lock_values.std(ddof=1))
    power_rng = np.random.Generator(np.random.PCG64(global_seed("power-resampling")))
    power_indices = power_rng.integers(0, len(lock_values), size=(5000, 66))
    studies = lock_values[power_indices]
    lower_approx = studies.mean(axis=1) - 1.669 * studies.std(axis=1, ddof=1) / math.sqrt(66)
    estimated_power = float((lower_approx > 0).mean())
    minimum_detectable = 1.669 * cluster_sd / math.sqrt(66)

    sensitivity = {}
    for weight in (0.10, 0.50):
        differences = [fixed_alternative_loss(row, selected, weight)
                       - alternative_loss(row, row["action"], weight) for row in evaluation]
        sensitivity[f"{weight:.2f}"] = sum(differences) / len(differences)

    result = {
        "schema": "gate34_development_v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "lock_commit": LOCK_COMMIT,
        "numpy_version": np.__version__,
        "selected_issue_only_comparator": issue_winner,
        "selected_comparator": selected,
        "policy_lock_fixed_losses": fixed_losses,
        "counts": {
            "generated": len(rows),
            "evaluable": len(evaluable),
            "policy_lock_evaluable": len(lock_rows),
            "evaluation_generated": evaluation_generated,
            "evaluation_evaluable": len(evaluation),
            "ideal_ties": sum(not row["evaluable"] and row.get("reason") == "ideal_gap_tie" for row in rows),
            "infrastructure_missing": len(missing),
            "infrastructure_missing_rate": missing_rate,
        },
        "gate3": {"delta_v": delta_v, "lower_bound": lower_bound,
                  "verdict": "pass" if gate3_pass else "fail",
                  "cluster_means": evaluation_cluster},
        "gate4": {"actions": action_results, "clearing_action_count": clearing,
                  "observed_ties": sum(row["observed_tie"] for row in evaluation),
                  "verdict": "pass" if gate4_pass else "fail"},
        "power": {"estimated_power": estimated_power, "cluster_sd": cluster_sd,
                  "minimum_detectable_mean": minimum_detectable,
                  "policy_lock_cluster_means": lock_cluster},
        "sensitivity": sensitivity,
        "routing": "M7-pre-data-audit" if gate3_pass and gate4_pass else "Stop-after-M6",
        "units": rows,
    }
    output.mkdir(parents=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    power_report.parent.mkdir(parents=True, exist_ok=True)
    (output / "gate34_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report.write_text(report_markdown(result), encoding="utf-8")
    power_report.write_text(
        "# M6 power analysis\n\n"
        f"**Evidence:** split-99 policy-lock development simulation.\n\n"
        f"- Policy-lock graph clusters: 33.\n"
        f"- Prospective evaluation clusters: 66.\n"
        f"- Resampled studies: 5,000.\n"
        f"- Estimated power: `{estimated_power:.6f}`.\n"
        f"- Policy-lock cluster SD: `{cluster_sd:.6f}`.\n"
        f"- Approximate minimum detectable positive mean: `{minimum_detectable:.6f}`.\n\n"
        "This is a development design diagnostic. Gate 3 uses the separately frozen 10,000-sample graph-cluster bootstrap and cannot be rescued by this estimate.\n",
        encoding="utf-8",
    )
    print(f"M6 complete: Gate 3 {result['gate3']['verdict'].upper()}, "
          f"Gate 4 {result['gate4']['verdict'].upper()}; route to {result['routing']}")


if __name__ == "__main__":
    main()
