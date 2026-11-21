"""Post-lock audit (erratum E005): deterministic recomputation spot check.

Recomputes a fixed, outcome-independent sample of units of the frozen Gate 2
and Gate 3/4 development runs with the frozen per-unit functions
(`tools/run_gate2.py:simulate_unit`, `tools/run_gate34.py:simulate_unit`) and
compares every stored field exactly (floats to 1e-12). The sample is every
`STRIDE`-th unit in the frozen generation order, so it does not depend on
outcomes. This is an independent recomputation check of provenance, not new
research data; the recomputed rows are not saved.

Usage: python tools/audit_reproducibility.py [stride]
Prints a JSON summary including the running NumPy and Python versions.
"""

from __future__ import annotations

import importlib.util
import json
import math
import platform
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def same(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, float) or isinstance(b, float):
        if a is None or b is None:
            return a is b
        if isinstance(a, float) and math.isnan(a):
            return isinstance(b, float) and math.isnan(b)
        return abs(a - b) <= 1e-12
    return a == b


VERDICT_FIELDS = ("pamp_prediction", "benefit_positive", "p2_prediction", "evaluable", "partition",
                  "action", "policy_loss", "fixed_losses", "correction_failed")


def check(stored_rows, recompute):
    checked = mismatched = 0
    first = None
    by_field = {}
    for row, new in recompute(stored_rows):
        checked += 1
        if not same(row, new):
            mismatched += 1
            fields = [k for k in set(row) | set(new) if not same(row.get(k), new.get(k))]
            for k in fields:
                by_field[k] = by_field.get(k, 0) + 1
            if first is None:
                first = {"key": row.get("key"), "fields": {k: (row.get(k), new.get(k)) for k in fields}}
    return {"checked": checked, "mismatched_units": mismatched, "mismatch_count_by_field": by_field,
            "verdict_relevant_fields_changed": sorted(k for k in by_field if k in VERDICT_FIELDS),
            "first_mismatch": first}


def main():
    stride = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    g2 = load("run_gate2")
    from sense_correct_abstain.gate2 import GRAPHS, BETA_VALUES, GAMMA_PAIRS, EPSILON_VALUES, PHI_VALUES
    order2 = [(g, b, gi, gj, e, p) for g in GRAPHS for b in range(len(BETA_VALUES)) for gi, gj in GAMMA_PAIRS
              for e in range(len(EPSILON_VALUES)) for p in range(len(PHI_VALUES))]
    stored2 = json.loads((ROOT / "results" / "dev" / "gate2_results.json").read_text(encoding="utf-8"))["units"]

    def recompute2(rows):
        for i in range(0, len(order2), stride):
            yield rows[i], g2.simulate_unit(*order2[i])

    g34 = load("run_gate34")
    from sense_correct_abstain.gate34 import split99_graphs, ERROR_POINTS, GAMMA_PAIR_INDICES
    graphs = split99_graphs()
    order34 = [(c, graph, b, gi, gj, e) for c, graph in enumerate(graphs) for b in range(len(BETA_VALUES))
               for gi, gj in GAMMA_PAIR_INDICES for e in range(len(ERROR_POINTS))]
    stored34 = json.loads((ROOT / "results" / "gate34" / "gate34_results.json").read_text(encoding="utf-8"))["units"]

    def strip(row):
        return {k: v for k, v in row.items() if k not in ("selected_fixed_loss", "delta")}

    recomputed34 = []

    def recompute34(rows):
        for i in range(0, len(order34), stride):
            new = g34.simulate_unit(*order34[i])
            recomputed34.append(new)
            yield strip(rows[i]), new

    summary = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "stride": stride,
        "gate2": check(stored2, recompute2),
        "gate34": check(stored34, recompute34),
    }
    if stride == 1:
        # Gate 3 statistic from the recomputed rows, with the frozen comparator and procedure.
        estimand = load("audit_gate34_estimand")
        frozen = json.loads((ROOT / "results" / "gate34" / "gate34_results.json").read_text(encoding="utf-8"))
        selected = frozen["selected_comparator"]
        evaluation = [r for r in recomputed34 if r["evaluable"] and r["partition"] == "evaluation"]
        dv, lb, _ = estimand.cluster_bootstrap(evaluation, lambda r: r["fixed_losses"][selected] - r["policy_loss"])
        summary["gate3_from_recomputed_rows"] = {
            "selected_comparator_frozen": selected, "delta_v": dv, "lower_bound": lb,
            "verdict_same_as_frozen": (dv > 0 and lb > 0) == (frozen["gate3"]["verdict"] == "pass"),
        }
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main()
