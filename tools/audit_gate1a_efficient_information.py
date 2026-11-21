"""Post-lock audit (erratum E001): compute the Gate-1A I3 quantity that the
frozen specification required but `tools/run_gate1a.py` hard-coded.

What this computes
------------------
For every frozen primary context (G2-primary, G3-primary), candidate design
(single, same, distinct) and grid point of the M3 9-by-9 grid, the efficient
(nuisance-projected) Fisher information for psi = (epsilon, phi) under the
frozen saturated local nuisance class of `gate1_math_spec_v1.md` §5.3:

* per candidate circuit, an unknown outcome distribution q (normalization only);
* per candidate circuit and tagged location ell, an unknown local response
  direction D_ell (sum-zero vector), entering through the first-order logical
  phase shift epsilon*theta_ell + s_ell(t)*phi.

In p-derivative coordinates the nuisance tangent space at the true point is
spanned, per candidate, by
    (a) label-independent sum-zero vectors (delta q), and
    (b) for each ell and outcome b: the vector over (t, b') equal to
        (epsilon*theta_ell + s_ell(t)*phi) * (e_b - e_0).
The epsilon and phi scores are exact-model derivatives (central differences,
step 1e-6, as in the frozen code). Each score is projected onto the
orthocomplement of the nuisance tangent space in the Fisher metric
<h, g> = sum_t w_t sum_b h_tb g_tb / p_tb, and the efficient information
matrix is formed from the projected scores.

Status: deterministic post-lock audit computation. It does not rerun Gate 1A,
does not change its verdict, and cannot contribute to any pass. Label patterns
with equal sign vectors give identical distributions (frame cancellation), so
the computation groups the 16^L patterns by sign vector with equal weight.

Usage: python tools/audit_gate1a_efficient_information.py
Writes: results/errata/gate1a_efficient_information.json
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate1 import G2_PRIMARY, G3_PRIMARY, LABELS, label_sign, probabilities  # noqa: E402

GRID = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)
DESIGNS = {
    "single": (math.pi / 4,),
    "same": (math.pi / 4, math.pi / 4),
    "distinct": (math.pi / 8, math.pi / 4),
}
STEP = 1e-6
# one representative Pauli label for each sign
REP = {+1: next(l for l in LABELS if label_sign(l) == +1), -1: next(l for l in LABELS if label_sign(l) == -1)}


def candidate_blocks(context, theta, epsilon, phi):
    """Return per-sign-vector probabilities, eps-derivs, phi-derivs, shifts."""
    L = len(context.edges)
    rows = []
    for signs in itertools.product((+1, -1), repeat=L):
        labels = tuple(REP[s] for s in signs)
        p = np.array(probabilities(context, theta, labels, epsilon, phi))
        de = (np.array(probabilities(context, theta, labels, epsilon + STEP, phi))
              - np.array(probabilities(context, theta, labels, epsilon - STEP, phi))) / (2 * STEP)
        dp = (np.array(probabilities(context, theta, labels, epsilon, phi + STEP))
              - np.array(probabilities(context, theta, labels, epsilon, phi - STEP))) / (2 * STEP)
        shifts = [epsilon * theta + s * phi for s in signs]
        rows.append((p, de, dp, shifts))
    return rows


def efficient_information(context, thetas, epsilon, phi):
    blocks = [candidate_blocks(context, theta, epsilon, phi) for theta in thetas]
    n_out = 1 << context.n_qubits
    L = len(context.edges)
    n_sign = 2 ** L
    dim = len(thetas) * n_sign * n_out
    weights = np.zeros(dim)
    pvec = np.zeros(dim)
    se = np.zeros(dim)
    sp = np.zeros(dim)
    nuisance = []
    for ci, rows in enumerate(blocks):
        base = ci * n_sign * n_out
        for ti, (p, de, dp, _shifts) in enumerate(rows):
            sl = slice(base + ti * n_out, base + (ti + 1) * n_out)
            weights[sl] = 1.0 / (len(thetas) * n_sign)
            pvec[sl] = p
            se[sl] = de
            sp[sl] = dp
        for b in range(1, n_out):
            v = np.zeros(dim)
            for ti in range(n_sign):
                v[base + ti * n_out + b] = 1.0
                v[base + ti * n_out + 0] = -1.0
            nuisance.append(v)
            for ell in range(L):
                w = np.zeros(dim)
                for ti, (_p, _de, _dp, shifts) in enumerate(rows):
                    w[base + ti * n_out + b] = shifts[ell]
                    w[base + ti * n_out + 0] = -shifts[ell]
                if np.any(w):
                    nuisance.append(w)
    mask = pvec > 1e-14
    metric = np.where(mask, weights / np.where(mask, pvec, 1.0), 0.0)
    sq = np.sqrt(metric)
    N = np.array(nuisance).T * sq[:, None]
    S = np.stack([se * sq, sp * sq], axis=1)
    # orthogonal projection onto the orthocomplement of span(N) (SVD basis)
    U, sing, _ = np.linalg.svd(N, full_matrices=False)
    keep = sing > 1e-10 * sing.max()
    Qm = U[:, keep]
    S_eff = S - Qm @ (Qm.T @ S)
    full = S.T @ S
    eff = S_eff.T @ S_eff
    return full, eff


def rank_of(matrix):
    values = np.linalg.eigvalsh(matrix)
    values = np.clip(values, 0.0, None)
    largest = values.max()
    tol = max(1e-12, 1e-10 * largest)
    # finite-difference noise floor: treat entries below 1e-9 as numerical zero
    tol = max(tol, 1e-9)
    return int((values > tol).sum()), values.tolist()


def main():
    records = []
    for context in (G2_PRIMARY, G3_PRIMARY):
        for name, thetas in DESIGNS.items():
            counts = {"0": 0, "1": 0, "2": 0}
            max_eps = 0.0
            phi_zero_phi_info = []
            phi_nonzero_max = 0.0
            eps_at_phi_zero = 0.0
            oracle_eps_at_phi_zero = []
            for epsilon, phi in itertools.product(GRID, repeat=2):
                full, eff = efficient_information(context, thetas, epsilon, phi)
                r, vals = rank_of(eff)
                counts[str(r)] += 1
                max_eps = max(max_eps, abs(eff[0, 0]))
                if phi == 0.0:
                    phi_zero_phi_info.append(eff[1, 1])
                    eps_at_phi_zero = max(eps_at_phi_zero, abs(eff[0, 0]))
                    oracle_eps_at_phi_zero.append(full[0, 0])
                else:
                    phi_nonzero_max = max(phi_nonzero_max, abs(eff[1, 1]))
            records.append({
                "context": context.name,
                "design": name,
                "thetas": list(thetas),
                "efficient_rank_counts_literal_first_order_reading": counts,
                "max_abs_efficient_info_epsilon_at_phi_zero": eps_at_phi_zero,
                "oracle_full_info_epsilon_at_phi_zero_range": [min(oracle_eps_at_phi_zero),
                                                               max(oracle_eps_at_phi_zero)],
                "max_abs_efficient_info_epsilon_epsilon": max_eps,
                "max_abs_efficient_info_phi_phi_at_phi_nonzero": phi_nonzero_max,
                "efficient_info_phi_phi_at_phi_zero_range": [min(phi_zero_phi_info), max(phi_zero_phi_info)],
            })
            print(context.name, name, counts, f"max|I_ee|={max_eps:.2e}",
                  f"max|I_pp|(phi!=0)={phi_nonzero_max:.2e}",
                  f"I_pp(phi=0) in [{min(phi_zero_phi_info):.4f},{max(phi_zero_phi_info):.4f}]")
    out = ROOT / "results" / "errata"
    out.mkdir(parents=True, exist_ok=True)
    (out / "gate1a_efficient_information.json").write_text(json.dumps({
        "schema": "erratum_E001_efficient_information_v1",
        "status": "post-lock deterministic audit; does not change the frozen Gate 1A verdict",
        "nuisance_class": ("literal first-order reading of gate1_math_spec_v1 section 5.3: per-candidate "
                           "unknown distribution q and first-order directions D_ell; second-order response "
                           "terms are NOT nuisance under this reading. Under the fully saturated reading "
                           "(every label-sign-class distribution free whenever phi != 0) the efficient "
                           "information is zero at every phi != 0 point by construction (erratum E001)."),
        "numerical_zero_threshold": 1e-9,
        "records": records,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
