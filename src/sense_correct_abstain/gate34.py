"""Frozen split-99 graph generator and Gate-3/4 policy helpers."""

from __future__ import annotations

import hashlib
import math

from .gate2 import Graph


ERROR_POINTS = ((0.0, 0.0), (-0.02, 0.0), (0.02, 0.0), (-0.04, -0.01), (0.04, 0.01))
GAMMA_PAIR_INDICES = ((0, 1), (2, 4), (4, 6))
SE_EPSILON = 0.007090190179103527
SE_PHI = 0.002541716727064875


def _connected(n_qubits: int, edges: tuple[tuple[int, int], ...]) -> bool:
    if not edges:
        return False
    seen = {0}
    changed = True
    while changed:
        changed = False
        for left, right in edges:
            if left in seen and right not in seen:
                seen.add(right)
                changed = True
            elif right in seen and left not in seen:
                seen.add(left)
                changed = True
    return len(seen) == n_qubits


def _graphs_for_size(n_qubits: int) -> list[tuple[tuple[int, int], ...]]:
    possible = tuple((i, j) for i in range(n_qubits) for j in range(i + 1, n_qubits))
    accepted: list[tuple[tuple[int, int], ...]] = []
    seen = set()
    candidate = 0
    while len(accepted) < 33:
        digest = hashlib.sha256(f"gate34-v1|{n_qubits}|{candidate}".encode()).digest()
        edges = tuple(edge for bit, edge in enumerate(possible)
                      if digest[bit // 8] & (1 << (7 - bit % 8)))
        if edges not in seen and _connected(n_qubits, edges):
            accepted.append(edges)
            seen.add(edges)
        candidate += 1
    return accepted


def split99_graphs() -> tuple[Graph, ...]:
    by_size = {n: _graphs_for_size(n) for n in (4, 5, 6)}
    graphs = []
    for accepted_index in range(33):
        for n_qubits in (4, 5, 6):
            cluster_id = len(graphs)
            graphs.append(Graph(f"split99-{cluster_id:02d}-n{n_qubits}", n_qubits,
                                by_size[n_qubits][accepted_index]))
    return tuple(graphs)


def unit_key(cluster_id: int, beta_i: int, gamma_i: int, gamma_j: int, error_i: int) -> str:
    return f"{cluster_id}|{beta_i}|{gamma_i}|{gamma_j}|{error_i}"


def seed_for(key: str, stream: str) -> int:
    digest = hashlib.sha256(f"gate34-v1|{key}|{stream}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def global_seed(name: str) -> int:
    return int.from_bytes(hashlib.sha256(f"gate34-v1|{name}".encode()).digest()[:8], "big")


def policy_action(
    *,
    estimate_defined: bool,
    unambiguous: bool,
    epsilon_hat: float,
    phi_hat: float,
    g0_hat: float,
    se_g0: float,
    instability_bound: float,
) -> str:
    significant = estimate_defined and (
        abs(epsilon_hat) > 1.96 * SE_EPSILON or abs(phi_hat) > 1.96 * SE_PHI)
    correction = (estimate_defined and unambiguous and significant and g0_hat != 0
                  and abs(g0_hat) <= instability_bound)
    if correction:
        return "C"
    if not estimate_defined or not unambiguous or abs(g0_hat) <= 1.96 * se_g0:
        return "A"
    return "N"


def quantile_linear(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction
