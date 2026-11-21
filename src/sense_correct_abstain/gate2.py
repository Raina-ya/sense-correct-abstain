"""Frozen Gate-2 QAOA target model and auditable transfer helpers."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Sequence

from .gate1 import Context, probabilities
from .pamp import M_VALUES, THETA_VALUES, design_rows, phase_from_xy, wrap


@dataclass(frozen=True)
class Graph:
    name: str
    n_qubits: int
    edges: tuple[tuple[int, int], ...]


GRAPHS = (
    Graph("edge-2", 2, ((0, 1),)),
    Graph("path-3", 3, ((0, 1), (1, 2))),
    Graph("triangle-3", 3, ((0, 1), (1, 2), (0, 2))),
    Graph("path-4", 4, ((0, 1), (1, 2), (2, 3))),
    Graph("cycle-4", 4, ((0, 1), (1, 2), (2, 3), (3, 0))),
    Graph("star-4", 4, ((0, 1), (0, 2), (0, 3))),
    Graph("complete-4", 4, tuple((i, j) for i in range(4) for j in range(i + 1, 4))),
    Graph("path-5", 5, ((0, 1), (1, 2), (2, 3), (3, 4))),
    Graph("cycle-5", 5, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))),
    Graph("star-5", 5, ((0, 1), (0, 2), (0, 3), (0, 4))),
)
BETA_VALUES = (math.pi / 16, math.pi / 8, 3 * math.pi / 16, math.pi / 4)
GAMMA_VALUES = tuple(k * math.pi / 16 for k in range(1, 8))
GAMMA_PAIRS = tuple((i, j) for i in range(7) for j in range(i + 1, 7) if j - i in (1, 2))
EPSILON_VALUES = (-0.04, -0.02, 0.0, 0.02, 0.04)
PHI_VALUES = (-0.01, 0.0, 0.01)


def unit_key(graph: Graph, beta_i: int, gamma_i: int, gamma_j: int, epsilon_i: int, phi_i: int) -> str:
    return f"{graph.name}|{beta_i}|{gamma_i}|{gamma_j}|{epsilon_i}|{phi_i}"


def partition(key: str) -> str:
    return "rule-development" if hashlib.sha256(key.encode()).digest()[0] <= 63 else "evaluation"


def seed_for(key: str, stream: str) -> int:
    digest = hashlib.sha256(f"gate2-v1|{key}|{stream}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def target_probabilities(graph: Graph, beta: float, gamma: float, epsilon: float, phi: float) -> tuple[float, ...]:
    context = Context(graph.name, graph.n_qubits, graph.edges, beta)
    return probabilities(context, 2 * gamma, ("II",) * len(graph.edges), epsilon, phi)


def cut_sizes(graph: Graph) -> tuple[int, ...]:
    return tuple(sum(((basis >> i) & 1) != ((basis >> j) & 1) for i, j in graph.edges)
                 for basis in range(1 << graph.n_qubits))


def score_distribution(graph: Graph, probs: Sequence[float]) -> tuple[float, ...]:
    result = [0.0] * (len(graph.edges) + 1)
    for score, probability in zip(cut_sizes(graph), probs, strict=True):
        result[score] += probability
    return tuple(result)


def expected_score(graph: Graph, distribution: Sequence[float]) -> float:
    return sum(score * probability for score, probability in enumerate(distribution)) / len(graph.edges)


def score_variance(graph: Graph, distribution: Sequence[float]) -> float:
    mean = expected_score(graph, distribution)
    return sum(((score / len(graph.edges) - mean) ** 2) * probability
               for score, probability in enumerate(distribution))


def nearest_clifford(angle: float) -> float:
    scaled = angle / (math.pi / 2)
    magnitude = math.floor(abs(scaled) + 0.5 - 1e-15)
    return math.copysign(magnitude * math.pi / 2, scaled)


def estimate_from_xy(repetition_xy: Sequence[tuple[float, float]], echo_xy: Sequence[tuple[float, float]]) -> tuple[float, float]:
    residuals: list[float] = []
    offset = 0
    for theta in THETA_VALUES:
        previous = None
        for m in M_VALUES:
            measured = phase_from_xy(*repetition_xy[offset])
            residual = wrap(measured - wrap(m * theta))
            per_block = residual / m
            if previous is not None:
                candidates = [per_block + 2 * math.pi * k / m for k in range(-m, m + 1)]
                per_block = min(candidates, key=lambda value: abs(value - previous))
                residual = m * per_block
            previous = per_block
            residuals.append(residual)
            offset += 1
    previous = None
    for (x_value, y_value), m in zip(echo_xy, M_VALUES, strict=True):
        residual = wrap(phase_from_xy(x_value, y_value))
        per_block = residual / (2 * m)
        if previous is not None:
            candidates = [per_block + math.pi * k / m for k in range(-m, m + 1)]
            per_block = min(candidates, key=lambda value: abs(value - previous))
            residual = 2 * m * per_block
        previous = per_block
        residuals.append(residual)
    rows = design_rows()
    a = sum(x * x for x, _ in rows)
    b = sum(x * y for x, y in rows)
    c = sum(y * y for _, y in rows)
    u = sum(x * value for (x, _), value in zip(rows, residuals, strict=True))
    v = sum(y * value for (_, y), value in zip(rows, residuals, strict=True))
    determinant = a * c - b * b
    return (c * u - b * v) / determinant, (a * v - b * u) / determinant
