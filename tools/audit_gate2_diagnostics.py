"""Post-lock audit (erratum E003): exploratory diagnostics of the frozen Gate 2
development result. EXPLORATORY ONLY: these quantities were not prespecified,
were computed after the verdict was known, and cannot change or support the
frozen Gate 2 verdict. They read only `results/dev/gate2_results.json`, except
the P2 structural check, which evaluates frozen twin circuits deterministically.

Reported:
1. Confusion counts of the frozen P-amp rule and of P2 on the evaluation partition.
2. Selectivity decomposition: balanced accuracy of the frozen rule, of its
   significance condition alone, of its |g0_hat| <= B_hat condition alone, and
   of the oracle indicator (epsilon, phi) != (0, 0).
3. Scoring-label noise: the binary label is the sign of the difference of two
   independent 256-replicate Monte Carlo accuracies; count positive labels within
   two Monte Carlo standard errors of zero, and positive labels among matched nulls.
4. P2 structural blindness: for beta in {pi/16, pi/8} the frozen rounding rule
   maps the twin mixer RX(2*beta) to the identity, so every twin outcome
   distribution is independent of the cost phases and of (epsilon, phi).

Usage: python tools/audit_gate2_diagnostics.py
Writes: results/errata/gate2_diagnostics.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate2 import (  # noqa: E402
    BETA_VALUES, EPSILON_VALUES, GAMMA_PAIRS, GAMMA_VALUES, GRAPHS, PHI_VALUES,
    nearest_clifford, score_distribution, target_probabilities,
)

SE_EPSILON = 0.007090190179103527
SE_PHI = 0.002541716727064875


def confusion(rows, predict):
    pos = [u for u in rows if u["benefit_positive"]]
    neg = [u for u in rows if not u["benefit_positive"]]
    tp = sum(bool(predict(u)) for u in pos)
    fp = sum(bool(predict(u)) for u in neg)
    sens = tp / len(pos)
    spec = 1 - fp / len(neg)
    return {"n": len(rows), "positives": len(pos), "negatives": len(neg), "true_positive": tp,
            "false_positive": fp, "predicted_positive": tp + fp, "sensitivity": sens,
            "specificity": spec, "balanced_accuracy": (sens + spec) / 2,
            "precision": tp / (tp + fp) if tp + fp else None,
            "base_rate": len(pos) / len(rows)}


def mc_sd(u):
    a, b = u["no_action_correct_probability"], u["corrected_correct_probability"]
    return math.sqrt(a * (1 - a) / 256 + b * (1 - b) / 256)


def p2_structural_check():
    blind_betas = [i for i, beta in enumerate(BETA_VALUES) if nearest_clifford(2 * beta) == 0.0]
    worst = 0.0
    checked = 0
    for graph in GRAPHS:
        for beta_i in blind_betas:
            twin_beta = nearest_clifford(2 * BETA_VALUES[beta_i]) / 2
            for gi, gj in GAMMA_PAIRS:
                for gamma in (GAMMA_VALUES[gi], GAMMA_VALUES[gj]):
                    twin_gamma = nearest_clifford(2 * gamma) / 2
                    ideal = score_distribution(graph, target_probabilities(graph, twin_beta, twin_gamma, 0.0, 0.0))
                    for epsilon in EPSILON_VALUES:
                        for phi in PHI_VALUES:
                            noisy = score_distribution(graph, target_probabilities(
                                graph, twin_beta, twin_gamma, epsilon, phi))
                            worst = max(worst, max(abs(a - b) for a, b in zip(ideal, noisy)))
                            checked += 1
    units = len(GRAPHS) * len(blind_betas) * len(GAMMA_PAIRS) * len(EPSILON_VALUES) * len(PHI_VALUES)
    return {"blind_beta_indices": blind_betas,
            "blind_beta_values": [BETA_VALUES[i] for i in blind_betas],
            "twin_mixer_after_rounding": 0.0,
            "max_abs_difference_noisy_vs_ideal_twin_distribution": worst,
            "twin_distributions_checked": checked,
            "generated_units_with_structurally_blind_p2": units,
            "generated_units_total": len(GRAPHS) * len(BETA_VALUES) * len(GAMMA_PAIRS)
            * len(EPSILON_VALUES) * len(PHI_VALUES)}


def main():
    frozen = json.loads((ROOT / "results" / "dev" / "gate2_results.json").read_text(encoding="utf-8"))
    E = [u for u in frozen["units"] if u["evaluable"] and u["partition"] == "evaluation"]

    def significant(u):
        return u["pamp_unambiguous"] and (abs(u["epsilon_hat"]) > 1.96 * SE_EPSILON
                                          or abs(u["phi_hat"]) > 1.96 * SE_PHI)

    def bound_only(u):
        g = u["initial_gap_observed"]
        return g != 0 and abs(g) <= u["instability_bound"]

    pos = [u for u in E if u["benefit_positive"]]
    null = [u for u in E if u["epsilon"] == 0 and u["phi"] == 0]
    intermediate = [u for u in E if 0.02 < u["no_action_correct_probability"] < 0.98]
    clearly_harmed = [u for u in E if u["correction_benefit"] < -2 * mc_sd(u)]
    result = {
        "schema": "erratum_E003_gate2_diagnostics_v1",
        "status": "EXPLORATORY post-hoc diagnostics; cannot change or support the frozen Gate 2 verdict",
        "frozen_rule": confusion(E, lambda u: u["pamp_prediction"]),
        "p2_comparator": confusion(E, lambda u: u["p2_prediction"]),
        "decomposition_balanced_accuracy": {
            "frozen_rule": confusion(E, lambda u: u["pamp_prediction"])["balanced_accuracy"],
            "significance_condition_only": confusion(E, significant)["balanced_accuracy"],
            "gap_bound_condition_only": confusion(E, bound_only)["balanced_accuracy"],
            "oracle_error_present_indicator": confusion(
                E, lambda u: u["epsilon"] != 0 or u["phi"] != 0)["balanced_accuracy"],
        },
        "intermediate_accuracy_units": confusion(intermediate, lambda u: u["pamp_prediction"]),
        "label_noise": {
            "positive_labels": len(pos),
            "positive_labels_within_2_mc_sd_of_zero": sum(u["correction_benefit"] <= 2 * mc_sd(u) for u in pos),
            "matched_null_units": len(null),
            "matched_null_positive_labels": sum(u["benefit_positive"] for u in null),
            "matched_null_intermediate_accuracy_units": sum(
                0.02 < u["no_action_correct_probability"] < 0.98 for u in null),
            "matched_null_intermediate_positive_labels": sum(
                u["benefit_positive"] for u in null if 0.02 < u["no_action_correct_probability"] < 0.98),
            "clearly_harmed_units_benefit_below_minus_2sd": len(clearly_harmed),
            "clearly_harmed_units_predicted_positive": sum(u["pamp_prediction"] for u in clearly_harmed),
        },
        "p2_structural_blindness": p2_structural_check(),
    }
    out = ROOT / "results" / "errata"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gate2_diagnostics.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                                encoding="utf-8")
    fr = result["frozen_rule"]
    print(f"frozen rule: predicted+ {fr['predicted_positive']}/{fr['n']}, sens {fr['sensitivity']:.3f}, "
          f"spec {fr['specificity']:.3f}, precision {fr['precision']:.3f}, base rate {fr['base_rate']:.3f}")
    print("decomposition:", {k: round(v, 4) for k, v in result["decomposition_balanced_accuracy"].items()})
    print("label noise:", result["label_noise"])
    print("P2 structural:", {k: v for k, v in result["p2_structural_blindness"].items()})


if __name__ == "__main__":
    main()
