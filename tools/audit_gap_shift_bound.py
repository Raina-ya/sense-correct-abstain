"""Post-lock audit (erratum E006): numerical check of the gap-shift bound.

Lemma B (E006 §3) states that, for every unit,
    |g(epsilon, phi) - g(0, 0)| <= (|epsilon| * A + |phi| * M) / 2 = B(epsilon, phi) / 2,
where g is the exact expected normalized-cut gap (candidate A minus B), A is the
sum of absolute tagged ideal angles over both candidates and M the number of
tagged rotations over both candidates. The lemma is proved analytically; this
script is a deterministic NUMERICAL CHECK over every generated unit of the
frozen Gate 2 and Gate 3/4 populations, using the frozen exact-probability
functions (no sampling, no new research data).

Usage: python tools/audit_gap_shift_bound.py
Writes: results/errata/gap_shift_bound_check.json
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate2 import (  # noqa: E402
    BETA_VALUES, EPSILON_VALUES, GAMMA_PAIRS, GAMMA_VALUES, GRAPHS, PHI_VALUES,
    expected_score, score_distribution, target_probabilities,
)
from sense_correct_abstain.gate34 import ERROR_POINTS, GAMMA_PAIR_INDICES, split99_graphs  # noqa: E402


def gap(graph, beta, gammas, epsilon, phi):
    means = [expected_score(graph, score_distribution(graph, target_probabilities(graph, beta, g, epsilon, phi)))
             for g in gammas]
    return means[0] - means[1]


def check(units):
    worst_ratio = 0.0
    worst = None
    count = 0
    for graph, beta, gammas, epsilon, phi in units:
        if epsilon == 0 and phi == 0:
            continue
        shift = abs(gap(graph, beta, gammas, epsilon, phi) - gap(graph, beta, gammas, 0.0, 0.0))
        a_sum = len(graph.edges) * sum(2 * g for g in gammas)
        m_count = 2 * len(graph.edges)
        half_b = (abs(epsilon) * a_sum + abs(phi) * m_count) / 2
        ratio = shift / half_b
        count += 1
        if ratio > worst_ratio:
            worst_ratio, worst = ratio, {"graph": graph.name, "beta": beta, "gammas": list(gammas),
                                         "epsilon": epsilon, "phi": phi, "shift": shift, "half_B": half_b}
    return {"units_checked": count, "max_ratio_shift_to_half_B": worst_ratio, "worst_case": worst,
            "bound_holds_everywhere": worst_ratio <= 1 + 1e-12}


def main():
    gate2 = [(g, BETA_VALUES[b], (GAMMA_VALUES[i], GAMMA_VALUES[j]), e, p)
             for g in GRAPHS for b in range(len(BETA_VALUES)) for i, j in GAMMA_PAIRS
             for e in EPSILON_VALUES for p in PHI_VALUES]
    gate34 = [(g, BETA_VALUES[b], (GAMMA_VALUES[i], GAMMA_VALUES[j]), e, p)
              for g in split99_graphs() for b in range(len(BETA_VALUES)) for i, j in GAMMA_PAIR_INDICES
              for e, p in ERROR_POINTS]
    result = {
        "schema": "erratum_E006_gap_shift_bound_v1",
        "status": "deterministic numerical check of an analytically proved bound; not a proof",
        "gate2_population": check(gate2),
        "gate34_population": check(gate34),
    }
    out = ROOT / "results" / "errata"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gap_shift_bound_check.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                                    encoding="utf-8")
    for key in ("gate2_population", "gate34_population"):
        r = result[key]
        print(key, r["units_checked"], "max ratio", round(r["max_ratio_shift_to_half_B"], 4),
              "holds:", r["bound_holds_everywhere"])


if __name__ == "__main__":
    main()
