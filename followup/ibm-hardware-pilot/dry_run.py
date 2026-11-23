"""Run the complete HW-P1 Stage A pipeline locally; never contacts IBM."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics

import numpy as np

from hwp1 import (
    BLOCKS,
    INJECTED_POINTS,
    SHOTS,
    circuit_key,
    estimate_point,
    expected_xy,
    ideal_xy,
    iter_point_circuits,
    seed_for,
    usage_ledger,
)

ROOT = Path(__file__).resolve().parent


def noiseless_check() -> dict[str, float | int]:
    worst = 0.0
    cases = 0
    for epsilon, phi in INJECTED_POINTS:
        for setting, _ in iter_point_circuits(epsilon, phi):
            observed = ideal_xy(setting, epsilon, phi)
            expected = expected_xy(setting, epsilon, phi)
            worst = max(worst, *(abs(a - b) for a, b in zip(observed, expected, strict=True)))
            cases += 1
    if worst > 1e-12:
        raise RuntimeError(f"noiseless semantic check failed: {worst:.3e}")
    return {"cases": cases, "max_deviation": worst}


def sampled_pipeline(blocks: int) -> dict:
    visibility = 0.95
    estimates: dict[str, list[dict[str, float]]] = {
        f"{epsilon:+.3f},{phi:+.3f}": [] for epsilon, phi in INJECTED_POINTS
    }
    for block in range(blocks):
        for point_index, (epsilon, phi) in enumerate(INJECTED_POINTS):
            values = {}
            rng = np.random.default_rng(seed_for("sampled", block, point_index))
            for setting, _ in iter_point_circuits(epsilon, phi):
                x, y = expected_xy(setting, epsilon, phi)
                ideal_expectation = x if setting.basis == "x" else y
                p0 = (1 + visibility * ideal_expectation) / 2
                p0_observed = p0 * 0.98 + (1 - p0) * 0.03
                zero_count = int(rng.binomial(SHOTS, p0_observed))
                values[circuit_key(setting)] = (2 * zero_count - SHOTS) / SHOTS
            epsilon_hat, phi_hat, visibility_hat = estimate_point(values)
            estimates[f"{epsilon:+.3f},{phi:+.3f}"].append(
                {"epsilon_hat": epsilon_hat, "phi_hat": phi_hat, "visibility": visibility_hat}
            )
    summary = {}
    for key, rows in estimates.items():
        epsilon, phi = (float(value) for value in key.split(","))
        epsilon_values = [row["epsilon_hat"] for row in rows]
        phi_values = [row["phi_hat"] for row in rows]
        summary[key] = {
            "blocks": len(rows),
            "epsilon_mean": statistics.fmean(epsilon_values),
            "epsilon_bias": statistics.fmean(epsilon_values) - epsilon,
            "epsilon_se": statistics.stdev(epsilon_values) / math.sqrt(len(rows)) if len(rows) > 1 else None,
            "phi_mean": statistics.fmean(phi_values),
            "phi_bias": statistics.fmean(phi_values) - phi,
            "visibility_mean": statistics.fmean(row["visibility"] for row in rows),
        }
    return {
        "kind": "deterministic sampled analysis-pipeline test; not circuit-noise simulation",
        "sampling_parameters": {"visibility": visibility, "readout_0_to_1": 0.02, "readout_1_to_0": 0.03},
        "blocks": blocks,
        "estimates": summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dry_run_report.json")
    args = parser.parse_args()
    report = {
        "status": "simulation-only; no IBM service contacted",
        "noiseless": noiseless_check(),
        "sampled_pipeline": sampled_pipeline(BLOCKS),
        "usage_ledger": usage_ledger(BLOCKS),
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
