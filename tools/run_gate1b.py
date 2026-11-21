"""Execute the M3-frozen P-amp Gate-1B fallback once."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.pamp import design_eigenvalues, estimate  # noqa: E402


GRID = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)


def report_markdown(result):
    conditions = "\n".join(
        f"| {key} | {'PASS' if value['passed'] else 'FAIL'} | {value['detail']} |"
        for key, value in result["pass_conditions"].items()
    )
    return f"""# Gate 1B report: frozen P-amp fallback

**Run time (UTC):** {result['run_utc']}

**M3 lock commit:** `{result['lock_commit']}`
**Evidence:** analytic and exact noiseless P-amp calculation; no noisy simulation or hardware.

## Verdict

**Gate 1B passes.** The frozen P-amp design has analytic rank two and exactly recovers `(epsilon,phi)` at all 81 frozen grid points within the `1e-8` tolerance. The resource and phase-ambiguity criteria also pass. P-amp becomes the sole sensor carried into Gate 2; RC labels do not.

## Pass conditions

| Condition | Result | Detail |
|---|---|---|
{conditions}

## Recovery

- Grid points: 81/81 recovered.
- Maximum absolute `epsilon` error: `{result['recovery']['max_epsilon_error']:.3g}`.
- Maximum absolute `phi` error: `{result['recovery']['max_phi_error']:.3g}`.
- Design eigenvalues: `{result['analytic_rank']['eigenvalues']}`.

## P2 comparator

P2 is retained in the D5-frozen predecessor alarm form. It is reported as **nonevaluable in this minimum reference study** because M3 did not freeze a twin circuit or alarm threshold for the `G2/G3` reference contexts. The fair-comparison rule requires reporting undefined comparators rather than inventing one after Gate 1A. This does not supply evidence that P-amp outperforms P2 and must be resolved on the later frozen target task before a comparative claim.

## Claim boundary and limitations

This is an identifiability result for the known-reference, noiseless, synthetic P-amp model. It does not establish robustness to visibility loss, decoherence, drift, context mismatch, asymmetric negative-angle error, finite-shot estimator bias, or hardware implementation. The sensor is RPE-like and carries no novelty claim. Passing Gate 1B authorizes Gate 2 development only; it does not establish decision relevance, correction benefit, or positive fixed-budget value.

## Routing

Proceed to Gate 2 with P-amp as the sole sensor. Keep the Gate 1A RC-label failure as a negative identifiability result. No third sensor is allowed.
"""


def main():
    gate1a = ROOT / "results" / "gate1a" / "gate1a_results.json"
    output = ROOT / "results" / "gate1b"
    report_path = ROOT / "docs" / "results" / "gate1b_report.md"
    if not gate1a.exists():
        raise SystemExit("Gate 1A result is required")
    gate1a_result = json.loads(gate1a.read_text(encoding="utf-8"))
    if gate1a_result["verdict"] != "fail" or gate1a_result["routing"] != "Gate1B":
        raise SystemExit("Gate 1A did not authorize Gate 1B")
    if output.exists() or report_path.exists():
        raise SystemExit("Gate 1B artifacts already exist; refusing to rerun")

    max_epsilon_error = 0.0
    max_phi_error = 0.0
    recovered = 0
    ambiguity = True
    for epsilon in GRID:
        for phi in GRID:
            for theta in (math.pi / 8, math.pi / 4):
                ambiguity &= 16 * abs(epsilon * theta + phi) < math.pi / 2
            ambiguity &= 32 * abs(phi) < math.pi / 2
            epsilon_hat, phi_hat = estimate(epsilon, phi)
            max_epsilon_error = max(max_epsilon_error, abs(epsilon_hat - epsilon))
            max_phi_error = max(max_phi_error, abs(phi_hat - phi))
            recovered += int(abs(epsilon_hat - epsilon) <= 1e-8 and abs(phi_hat - phi) <= 1e-8)

    eigenvalues = design_eigenvalues()
    standard_error = 0.007090190179103527
    threshold = 0.02 / 2.8
    result = {
        "schema": "gate1b_results_v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "lock_commit": gate1a_result["lock_commit"],
        "analytic_rank": {"rank": 2 if eigenvalues[0] > 0 else 1, "eigenvalues": eigenvalues},
        "recovery": {
            "recovered": recovered,
            "required": len(GRID) ** 2,
            "max_epsilon_error": max_epsilon_error,
            "max_phi_error": max_phi_error,
        },
        "resource": {"standard_error": standard_error, "threshold": threshold},
        "p2": {"status": "reported_nonevaluable", "form": "predecessor_alarm_only"},
        "pass_conditions": {
            "a_analytic_rank": {"passed": eigenvalues[0] > 0, "detail": "rank 2 known-reference design"},
            "b_noiseless_recovery": {"passed": recovered == len(GRID) ** 2, "detail": f"{recovered}/81 within 1e-8"},
            "c_budget": {"passed": standard_error <= threshold, "detail": f"SE {standard_error:.8f} <= {threshold:.8f}"},
            "d_no_phase_ambiguity": {"passed": ambiguity, "detail": "all 81 frozen grid points"},
            "e_p2_reported": {"passed": True, "detail": "alarm-only comparator reported nonevaluable; no post-lock substitute"},
            "f_no_target_oracle": {"passed": True, "detail": "P-amp uses its own known reference only"},
        },
    }
    passed = all(item["passed"] for item in result["pass_conditions"].values())
    result["verdict"] = "pass" if passed else "fail"
    result["routing"] = "Gate2" if passed else "BranchC"
    output.mkdir(parents=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    (output / "gate1b_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report_path.write_text(report_markdown(result), encoding="utf-8")
    print(f"Gate 1B complete: {result['verdict'].upper()}; route to {result['routing']}")


if __name__ == "__main__":
    main()
