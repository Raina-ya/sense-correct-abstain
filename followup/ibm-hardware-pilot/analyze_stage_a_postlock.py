"""POST-LOCK corrected analysis of HW-P1 Stage A (erratum HWP1-E001).

The locked analysis (`analyze_stage_a.py`, hash-bound in
`docs/freeze/hwp1_stage_a_lock_v2.json`) defined the "SE" of each point as
`stdev(block estimates) / sqrt(8)`, the standard error of the mean of eight
2430-shot estimates. The locked protocol (`PROTOCOL_DRAFT.md` §5, estimand 1)
asks for `SE_hw(eps_hat)` *at 2430 shots*, i.e. the spread of a single
2430-shot estimate, pooled over points, compared with the frozen threshold
0.0071429 that refers to one 2430-shot estimate. This script computes that
estimand:

* per point: the sample SD (ddof=1) of the eight block estimates, with a
  95% percentile block-bootstrap interval;
* pooled: the within-point SD pooled over the five points
  (sqrt(sum of squared deviations from each point mean / (40 - 5))), with a
  95% percentile interval from a *joint* block bootstrap (the same resampled
  block indices for every point in each replicate);
* the protocol's outcome rule: meets if the upper end < 0.0071429, fails if
  the lower end > 0.0071429, otherwise inconclusive.

It reads only the raw QPU result files and the locked analysis output, never
modifies them, recomputes the per-block estimates independently of `hwp1.py`
(no Qiskit dependency), and checks that they equal the locked output's
per-block estimates. Bias and visibility are copied from the locked output,
whose computation of those quantities is not affected by the erratum.

Status: post-lock analysis specified after the data were seen; it corrects an
implementation error against the locked protocol and is labelled as such.

Usage: python followup/ibm-hardware-pilot/analyze_stage_a_postlock.py [--check]
  --check  recompute and compare with the stored output instead of writing it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from sense_correct_abstain.gate2 import estimate_from_xy  # noqa: E402

RAW = ROOT / "followup" / "ibm-hardware-pilot" / "results" / "stage_a"
LOCKED_OUTPUT = RAW / "analysis_primary.json"
OUTPUT = ROOT / "followup" / "ibm-hardware-pilot" / "results" / "stage_a_postlock" / "analysis_corrected.json"
THRESHOLD = 0.0071429
BOOTSTRAPS = 10_000
BLOCKS = 8
POINTS = ((0.0, 0.0), (0.02, 0.0), (-0.02, 0.0), (0.04, 0.01), (-0.04, -0.01))
THETAS = (math.pi / 8, math.pi / 4)
REPS = (1, 4, 16)


def seed(*parts: object) -> int:
    key = "|".join(str(p) for p in parts)
    return int.from_bytes(hashlib.sha256(f"hwp1|postlock|{key}".encode()).digest()[:4], "big")


def point_key(eps: float, phi: float) -> str:
    return f"{eps:+.3f},{phi:+.3f}"


def expectation(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    return (counts.get("0", 0) - counts.get("1", 0)) / total


def block_estimates() -> np.ndarray:
    """Return an (8, 5) array of epsilon_hat, recomputed from raw counts."""
    paths = sorted(RAW.glob("block_*_result.json"))
    if len(paths) != BLOCKS:
        raise SystemExit(f"expected {BLOCKS} raw result files, found {len(paths)}")
    out = np.empty((BLOCKS, len(POINTS)))
    for b, path in enumerate(paths):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["block"] != b:
            raise SystemExit(f"unexpected block index in {path.name}")
        values: dict[tuple[float, float], dict] = {p: {} for p in POINTS}
        for record in data["records"]:
            label = record["label"]
            if label["kind"] == "pamp":
                key = (label["family"], label["theta"], label["repetitions"], label["basis"])
                values[(label["epsilon"], label["phi"])][key] = expectation(record["counts"])
        for j, p in enumerate(POINTS):
            v = values[p]
            rep = [(v[("repetition", t, m, "x")], v[("repetition", t, m, "y")]) for t in THETAS for m in REPS]
            echo = [(v[("echo", math.pi / 4, m, "x")], v[("echo", math.pi / 4, m, "y")]) for m in REPS]
            out[b, j] = estimate_from_xy(rep, echo)[0]
    return out


def label(low: float, high: float) -> str:
    if high < THRESHOLD:
        return "meets"
    if low > THRESHOLD:
        return "fails"
    return "inconclusive"


def pooled_sd(est: np.ndarray) -> float:
    dev = est - est.mean(axis=0, keepdims=True)
    return float(math.sqrt((dev ** 2).sum() / (est.size - est.shape[1])))


def analyze() -> dict:
    locked = json.loads(LOCKED_OUTPUT.read_text(encoding="utf-8"))
    est = block_estimates()

    # Cross-check against the locked per-block estimates.
    max_diff = 0.0
    for j, p in enumerate(POINTS):
        rows = locked["points"][point_key(*p)]["blocks"]
        stored = np.array([r["epsilon_hat"] for r in sorted(rows, key=lambda r: r["block"])])
        max_diff = max(max_diff, float(np.max(np.abs(stored - est[:, j]))))
    if max_diff > 1e-12:
        raise SystemExit(f"per-block estimates disagree with the locked output (max diff {max_diff})")

    points = {}
    for j, p in enumerate(POINTS):
        key = point_key(*p)
        rng = np.random.default_rng(seed("point-sd", key))
        idx = rng.integers(0, BLOCKS, size=(BOOTSTRAPS, BLOCKS))
        boot = est[idx, j].std(axis=1, ddof=1)
        low, high = (float(x) for x in np.quantile(boot, [0.025, 0.975]))
        sd = float(est[:, j].std(ddof=1))
        lp = locked["points"][key]
        points[key] = {
            "epsilon_hat_by_block": est[:, j].tolist(),
            "sd_single_2430_shot_estimate": sd,
            "sd_95_interval": [low, high],
            "corrected_label": label(low, high),
            "retracted_locked_label": lp["epsilon_se_threshold_outcome"],
            "locked_value_was_se_of_8_block_mean": lp["epsilon_se"],
            "bias_from_locked_output": {
                "epsilon_bias": lp["epsilon_bias"],
                "epsilon_bias_95_interval": lp["epsilon_bias_95_interval"],
                "bias_flag": lp["bias_flag"],
                "phi_bias": lp["phi_bias"],
            },
            "visibility_mean_from_locked_output": lp["visibility_mean"],
        }

    rng = np.random.default_rng(seed("pooled-sd", "joint"))
    idx = rng.integers(0, BLOCKS, size=(BOOTSTRAPS, BLOCKS))
    boot = np.array([pooled_sd(est[row]) for row in idx])
    low, high = (float(x) for x in np.quantile(boot, [0.025, 0.975]))
    pooled = pooled_sd(est)

    return {
        "study": "HW-P1 Stage A",
        "status": "POST-LOCK corrected analysis (erratum HWP1-E001); specified after the data were seen",
        "erratum": "followup/ibm-hardware-pilot/errata/HWP1-E001_precision_estimand.md",
        "estimand": "SD of a single 2430-shot epsilon estimate (protocol section 5, estimand 1)",
        "threshold": THRESHOLD,
        "bootstrap_replicates": BOOTSTRAPS,
        "bootstrap": "percentile; resample the 8 blocks with replacement; pooled uses the same block indices for all points",
        "seeds": "SHA256('hwp1|postlock|' + key)[:4], big-endian",
        "numpy_version": np.__version__,
        "inputs": {
            "raw_results": "followup/ibm-hardware-pilot/results/stage_a/block_0[0-7]_result.json",
            "locked_output": "followup/ibm-hardware-pilot/results/stage_a/analysis_primary.json",
        },
        "cross_check_max_abs_diff_vs_locked_block_estimates": max_diff,
        "points": points,
        "pooled_within_point_sd": {
            "value": pooled,
            "degrees_of_freedom": est.size - est.shape[1],
            "joint_bootstrap_95_interval": [low, high],
            "corrected_label": label(low, high),
            "ratio_to_threshold": pooled / THRESHOLD,
        },
        "caveat": "Eight blocks give coarse SD intervals; percentile intervals for an SD from n=8 tend to be too narrow and biased low.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = analyze()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.check:
        stored = json.loads(OUTPUT.read_text(encoding="utf-8"))
        fresh = json.loads(text)
        stored.pop("numpy_version", None)
        fresh.pop("numpy_version", None)

        def close(a, b) -> bool:
            if isinstance(a, dict):
                return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
            if isinstance(a, list):
                return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
            if isinstance(a, float) or isinstance(b, float):
                return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
            return a == b

        if not close(stored, fresh):
            raise SystemExit("post-lock corrected analysis does not reproduce the stored output")
        print("HW-P1 post-lock corrected analysis reproduces the stored output")
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
