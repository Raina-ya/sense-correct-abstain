"""Post-lock audit (erratum E004): selection-conditioning defect in the frozen
Gate 3 policy loss, and a corrected-estimand reanalysis. POST-HOC: this
reanalysis was specified after the frozen Gate 3 result was known. It cannot
change, rescue, or replace the frozen Gate 3 verdict, and it cannot authorize M7.

Defect. The frozen policy chooses N only when the realized initial gap satisfies
|g0_hat| > 1.96 * SE_g0, and on path N it issues delta_0 = sign(g0_hat) from those
same initial shots. `tools/run_gate34.py` nevertheless scored the policy's N loss
as 1 - sensor_correct_probability, an unconditional probability estimated from
256 independent replicate redraws. That is the expected loss of always issuing,
not the conditional loss of issuing on the selected event, so
E[1{N} * loss_used] != E[1{N} * 1{delta_0 wrong}] in general. The correct
per-unit loss on path N, conditional on the stage-1 data that the policy saw,
is the realized indicator 1{delta_0 wrong} (theory note, Theorem T1, l_N).

Corrected estimand. Same units, comparator (selected once on the policy-lock
partition, unchanged), C and A losses as frozen (the C loss is a conditional
expectation of the future rerun given the stage-1 data, which is correct up to
Monte Carlo error), and the realized indicator on path N. Uncertainty uses the
frozen procedure: per-cluster means, 10,000 cluster-bootstrap samples with the
frozen PCG64 seed, linear-interpolation 5th percentile.

The script first reproduces the frozen Delta_V and lower bound from the stored
per-unit fields as a fidelity check, then computes the corrected values.

Usage: python tools/audit_gate34_estimand.py
Writes: results/errata/gate34_estimand.json
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate34 import global_seed, quantile_linear  # noqa: E402


def cluster_bootstrap(rows, delta):
    by_cluster = {}
    for row in rows:
        by_cluster.setdefault(row["cluster_id"], []).append(delta(row))
    means = {c: sum(v) / len(v) for c, v in by_cluster.items()}
    values = np.array(list(means.values()))
    rng = np.random.Generator(np.random.PCG64(global_seed("cluster-bootstrap")))
    idx = rng.integers(0, len(values), size=(10000, len(values)))
    lower = quantile_linear(values[idx].mean(axis=1).tolist(), 0.05)
    return sum(delta(r) for r in rows) / len(rows), lower, len(values)


def main():
    frozen = json.loads((ROOT / "results" / "gate34" / "gate34_results.json").read_text(encoding="utf-8"))
    selected = frozen["selected_comparator"]
    E = [u for u in frozen["units"] if u["evaluable"] and u["partition"] == "evaluation"]

    def realized_wrong(u):
        selected_a = u["initial_gap_observed"] >= 0  # frozen sampled tie rule: equality selects A
        return float(selected_a != (u["ideal_gap"] > 0))

    def corrected_policy_loss(u):
        return realized_wrong(u) if u["action"] == "N" else u["policy_loss"]

    frozen_dv, frozen_lb, k = cluster_bootstrap(E, lambda u: u["fixed_losses"][selected] - u["policy_loss"])
    reproduced = (abs(frozen_dv - frozen["gate3"]["delta_v"]) < 1e-12
                  and abs(frozen_lb - frozen["gate3"]["lower_bound"]) < 1e-12)
    corr_dv, corr_lb, _ = cluster_bootstrap(E, lambda u: u["fixed_losses"][selected] - corrected_policy_loss(u))

    n_rows = [u for u in E if u["action"] == "N"]
    used = sum(1 - u["sensor_correct_probability"] for u in n_rows) / len(n_rows)
    realized = sum(realized_wrong(u) for u in n_rows) / len(n_rows)
    c_rows = [u for u in E if u["action"] == "C"]
    a_rows = [u for u in E if u["action"] == "A"]
    contrib = {
        "N": sum(u["fixed_losses"][selected] - realized_wrong(u) for u in n_rows) / len(E),
        "C": sum(u["fixed_losses"][selected] - u["policy_loss"] for u in c_rows) / len(E),
        "A": sum(u["fixed_losses"][selected] - u["policy_loss"] for u in a_rows) / len(E),
    }
    result = {
        "schema": "erratum_E004_gate34_estimand_v1",
        "status": ("POST-HOC corrected-estimand reanalysis of stored fields; the frozen Gate 3 verdict "
                   "(FAIL) stands and this analysis cannot rescue it or authorize M7"),
        "selected_comparator": selected,
        "evaluation_units": len(E),
        "graph_clusters": k,
        "frozen_reproduction": {"delta_v": frozen_dv, "lower_bound": frozen_lb, "matches_artifact": reproduced},
        "corrected_estimand": {"delta_v": corr_dv, "lower_bound": corr_lb},
        "path_N": {
            "units": len(n_rows),
            "mean_loss_used_in_frozen_run_unconditional": used,
            "mean_realized_conditional_loss": realized,
        },
        "corrected_delta_v_contribution_by_action": contrib,
        "note_on_C_units": ("on C units the policy loss equals the selected C-always comparator loss "
                            "exactly (same corrected-rerun probability), so they contribute zero"),
    }
    out = ROOT / "results" / "errata"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gate34_estimand.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                              encoding="utf-8")
    print(json.dumps({k2: v for k2, v in result.items() if k2 != "status"}, indent=1))


if __name__ == "__main__":
    main()
