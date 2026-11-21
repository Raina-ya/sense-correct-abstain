"""Post-lock audit (erratum E001): restate the Gate-1A finite-separation pairs
at the frozen sensing budget, as `gate1_math_spec_v1.md` §10 required.

The frozen run (`results/gate1a/gate1a_results.json`) reported single-shot
quantities only. This script reads those stored single-shot quantities and
applies exact product-measure identities for n = 2430 i.i.d. observations of
the full (label, bitstring) distribution:

* Bhattacharyya coefficient: BC_n = BC_1 ** n, where the frozen artifact stores
  hellinger_squared = 0.5 * sum (sqrt a - sqrt b)^2 = 1 - BC_1;
* KL_n = n * KL_1;
* upper bound   TV_n <= sqrt(1 - BC_n ** 2);
* lower bounds  1 - TV_n >= 0.5 * BC_n ** 2        (Le Cam's inequality),
                1 - TV_n >= 0.5 * exp(-KL_n)       (Bretagnolle-Huber).
The equal-prior two-point error lower bound is (1 - TV_n) / 2.

Status: deterministic post-lock restatement of stored quantities; no new
simulation, no change to any verdict. Action relevance remains nonevaluable
because M3 froze no action map for these reference contexts.

Usage: python tools/audit_gate1a_pairs_budget.py
Writes: results/errata/gate1a_pairs_at_budget.json
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N_SENSE = 2430


def main():
    frozen = json.loads((ROOT / "results" / "gate1a" / "gate1a_results.json").read_text(encoding="utf-8"))
    rows = []
    for pair in frozen["finite_pairs"]:
        d = pair["distances"]
        bc1 = 1.0 - d["hellinger_squared"]
        bcn = bc1 ** N_SENSE
        kln = N_SENSE * d["kl_z0_to_z1"]
        tv_upper = math.sqrt(max(0.0, 1.0 - bcn ** 2))
        overlap_lower = max(0.5 * bcn ** 2, 0.5 * math.exp(-kln))
        rows.append({
            "context": pair["context"],
            "theta_ref": pair["theta_ref"],
            "z1": pair["z1"],
            "single_shot": {"tv": d["tv"], "bc": bc1, "kl": d["kl_z0_to_z1"]},
            "budget_n": N_SENSE,
            "bc_n": bcn,
            "kl_n": kln,
            "tv_n_upper_bound": tv_upper,
            "one_minus_tv_n_lower_bound": overlap_lower,
            "two_point_error_lower_bound_equal_prior": overlap_lower / 2,
            "two_point_wrong_action_sum_lower_bound": overlap_lower,
            "action_relevance": "nonevaluable_no_frozen_action_map",
        })
        print(f"{pair['context']} theta={pair['theta_ref']:.4f} eps={pair['z1']['epsilon']:+.2f} "
              f"KL_n={kln:.3f} BC_n={bcn:.4f} TV_n<= {tv_upper:.4f} "
              f"two-point error >= {overlap_lower / 2:.4f}")
    out = ROOT / "results" / "errata"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gate1a_pairs_at_budget.json").write_text(json.dumps({
        "schema": "erratum_E001_pairs_at_budget_v1",
        "status": "post-lock restatement of stored single-shot quantities at the frozen sensing budget",
        "pairs": rows,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
