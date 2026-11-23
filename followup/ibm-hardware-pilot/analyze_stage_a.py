"""Analyze the eight locked HW-P1 Stage A blocks from unmitigated counts."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics

import numpy as np

from hwp1 import BLOCKS, INJECTED_POINTS, circuit_key, estimate_point, seed_for

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "followup" / "ibm-hardware-pilot" / "results" / "stage_a"
THRESHOLD = 0.0071429
BOOTSTRAPS = 10_000


def point_key(epsilon: float, phi: float) -> str:
    return f"{epsilon:+.3f},{phi:+.3f}"


def expectation(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    if total == 0:
        raise ValueError("empty counts")
    return (counts.get("0", 0) - counts.get("1", 0)) / total


def interval(values: list[float], statistic, seed_key: str) -> tuple[float, float]:
    rng = np.random.default_rng(seed_for("bootstrap", seed_key))
    array = np.asarray(values, dtype=float)
    sampled = array[rng.integers(0, len(array), size=(BOOTSTRAPS, len(array)))]
    estimates = np.asarray([statistic(row.tolist()) for row in sampled])
    low, high = np.quantile(estimates, [0.025, 0.975], method="linear")
    return float(low), float(high)


def sample_se(values: list[float]) -> float:
    return statistics.stdev(values) / math.sqrt(len(values))


def read_blocks(directory: Path) -> list[dict]:
    paths = sorted(directory.glob("block_*_result.json"))
    if len(paths) != BLOCKS:
        raise RuntimeError(f"expected {BLOCKS} completed blocks, found {len(paths)}")
    blocks = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    if [block["block"] for block in blocks] != list(range(BLOCKS)):
        raise RuntimeError("block indices are incomplete or duplicated")
    return blocks


def calibration_error(records: list[dict]) -> float:
    errors = []
    for record in records:
        label = record["label"]
        if label["kind"] != "readout_calibration":
            continue
        counts = record["counts"]
        total = sum(counts.values())
        prepared = label["prepared"]
        for bit_index in (0, 1):
            expected = prepared[-1 - bit_index]
            correct = sum(
                count
                for outcome, count in counts.items()
                if outcome.replace(" ", "").zfill(2)[-1 - bit_index] == expected
            )
            errors.append(1 - correct / total)
    if len(errors) != 8:
        raise RuntimeError("each block must contain four readout calibration records")
    return max(errors)


def analyze(directory: Path) -> dict:
    blocks = read_blocks(directory)
    estimates = {point_key(*point): [] for point in INJECTED_POINTS}
    z_counts = {point_key(*point): {"0": 0, "1": 0} for point in INJECTED_POINTS}
    calibration_errors = []

    for block in blocks:
        calibration_errors.append(calibration_error(block["records"]))
        values = {point_key(*point): {} for point in INJECTED_POINTS}
        for record in block["records"]:
            label = record["label"]
            if label["kind"] == "pamp":
                key = point_key(label["epsilon"], label["phi"])
                setting = (
                    label["family"],
                    label["theta"],
                    label["repetitions"],
                    label["basis"],
                )
                values[key][setting] = expectation(record["counts"])
            elif label["kind"] == "z_control":
                key = point_key(label["epsilon"], label["phi"])
                for outcome in ("0", "1"):
                    z_counts[key][outcome] += record["counts"].get(outcome, 0)
        for key, point_values in values.items():
            epsilon_hat, phi_hat, visibility = estimate_point(point_values)
            estimates[key].append({
                "block": block["block"],
                "epsilon_hat": epsilon_hat,
                "phi_hat": phi_hat,
                "visibility": visibility,
            })

    summary = {}
    for epsilon, phi in INJECTED_POINTS:
        key = point_key(epsilon, phi)
        rows = estimates[key]
        epsilon_values = [row["epsilon_hat"] for row in rows]
        phi_values = [row["phi_hat"] for row in rows]
        visibility_values = [row["visibility"] for row in rows]
        epsilon_se = sample_se(epsilon_values)
        se_interval = interval(epsilon_values, sample_se, f"se|{key}")
        epsilon_bias = statistics.fmean(epsilon_values) - epsilon
        bias_interval_raw = interval(epsilon_values, statistics.fmean, f"bias|{key}")
        bias_interval = (bias_interval_raw[0] - epsilon, bias_interval_raw[1] - epsilon)
        if se_interval[1] < THRESHOLD:
            outcome = "meets"
        elif se_interval[0] > THRESHOLD:
            outcome = "fails"
        else:
            outcome = "inconclusive"
        summary[key] = {
            "blocks": rows,
            "epsilon_mean": statistics.fmean(epsilon_values),
            "epsilon_bias": epsilon_bias,
            "epsilon_bias_95_interval": bias_interval,
            "epsilon_se": epsilon_se,
            "epsilon_se_95_interval": se_interval,
            "epsilon_se_threshold_outcome": outcome,
            "bias_flag": bias_interval[0] > THRESHOLD or bias_interval[1] < -THRESHOLD,
            "phi_mean": statistics.fmean(phi_values),
            "phi_bias": statistics.fmean(phi_values) - phi,
            "visibility_mean": statistics.fmean(visibility_values),
            "visibility_95_interval": interval(visibility_values, statistics.fmean, f"visibility|{key}"),
        }

    zero_key = point_key(0.0, 0.0)
    zero_counts = z_counts[zero_key]
    z_tests = {}
    z_critical = statistics.NormalDist().inv_cdf(1 - 0.05 / (2 * (len(INJECTED_POINTS) - 1)))
    for epsilon, phi in INJECTED_POINTS[1:]:
        key = point_key(epsilon, phi)
        other = z_counts[key]
        n0, n1 = sum(zero_counts.values()), sum(other.values())
        p0, p1 = zero_counts["0"] / n0, other["0"] / n1
        pooled = (zero_counts["0"] + other["0"]) / (n0 + n1)
        se = math.sqrt(pooled * (1 - pooled) * (1 / n0 + 1 / n1))
        z_score = math.inf if se == 0 and p0 != p1 else (0.0 if se == 0 else (p1 - p0) / se)
        z_tests[key] = {"z_score": z_score, "bonferroni_critical": z_critical, "flag": abs(z_score) > z_critical}

    zero_eps = [row["epsilon_hat"] for row in estimates[zero_key]]
    x = list(range(BLOCKS))
    x_mean = statistics.fmean(x)
    drift_slope = sum((a - x_mean) * b for a, b in zip(x, zero_eps, strict=True)) / sum(
        (a - x_mean) ** 2 for a in x
    )
    validity = {
        "readout_assignment_error_by_block": calibration_errors,
        "readout_below_5_percent_every_block": all(error < 0.05 for error in calibration_errors),
        "z_control_tests": z_tests,
        "z_control_pass": not any(test["flag"] for test in z_tests.values()),
    }
    return {
        "study": "HW-P1 Stage A",
        "evidence": "IBM hardware-derived counts; follow-up study only",
        "primary_analysis": "unmitigated counts",
        "threshold": THRESHOLD,
        "bootstrap_replicates": BOOTSTRAPS,
        "points": summary,
        "zero_injection_epsilon_drift_slope_per_block": drift_slope,
        "validity": validity,
        "stage_valid": validity["readout_below_5_percent_every_block"] and validity["z_control_pass"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.input / "analysis_primary.json"
    report = analyze(args.input)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
