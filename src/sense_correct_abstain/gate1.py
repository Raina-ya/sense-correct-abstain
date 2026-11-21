"""Exact state-vector calculations for the M3-frozen Gate-1 design.

Qubit 0 is the least-significant computational-basis bit.  The implementation
uses only the Python standard library so the small two- and three-qubit study is
fully enumerable without an external numerical dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
from typing import Iterable, Sequence


PAULIS = ("I", "X", "Y", "Z")
LABELS = tuple(a + b for a in PAULIS for b in PAULIS)
CORRECTIONS = {
    "II": "II", "IX": "IX", "IY": "ZY", "IZ": "ZZ",
    "XI": "XX", "XX": "XI", "XY": "YZ", "XZ": "YY",
    "YI": "YX", "YX": "YI", "YY": "XZ", "YZ": "XY",
    "ZI": "ZI", "ZX": "ZX", "ZY": "IY", "ZZ": "IZ",
}


@dataclass(frozen=True)
class Context:
    name: str
    n_qubits: int
    edges: tuple[tuple[int, int], ...]
    beta: float


G2_PRIMARY = Context("G2-primary", 2, ((0, 1),), math.pi / 8)
G3_PRIMARY = Context("G3-primary", 3, ((0, 1), (1, 2)), math.pi / 8)
G2_SCORE_ZERO = Context("G2-score-zero", 2, ((0, 1),), 0.0)


def _apply_single(state: list[complex], matrix: tuple[tuple[complex, complex], ...], qubit: int) -> None:
    step = 1 << qubit
    for base in range(0, len(state), 2 * step):
        for offset in range(step):
            i = base + offset
            j = i + step
            a, b = state[i], state[j]
            state[i] = matrix[0][0] * a + matrix[0][1] * b
            state[j] = matrix[1][0] * a + matrix[1][1] * b


def _apply_cx(state: list[complex], control: int, target: int) -> None:
    for basis in range(len(state)):
        if ((basis >> control) & 1) and not ((basis >> target) & 1):
            partner = basis | (1 << target)
            state[basis], state[partner] = state[partner], state[basis]


def _single_matrix(name: str, angle: float = 0.0) -> tuple[tuple[complex, complex], ...]:
    if name == "I":
        return ((1, 0), (0, 1))
    if name == "X":
        return ((0, 1), (1, 0))
    if name == "Y":
        return ((0, -1j), (1j, 0))
    if name == "Z":
        return ((1, 0), (0, -1))
    if name == "RZ":
        return ((complex(math.cos(-angle / 2), math.sin(-angle / 2)), 0),
                (0, complex(math.cos(angle / 2), math.sin(angle / 2))))
    if name == "RX":
        c, s = math.cos(angle / 2), -1j * math.sin(angle / 2)
        return ((c, s), (s, c))
    raise ValueError(name)


def _apply_pauli_pair(state: list[complex], label: str, control: int, target: int) -> None:
    _apply_single(state, _single_matrix(label[0]), control)
    _apply_single(state, _single_matrix(label[1]), target)


def label_sign(label: str) -> int:
    return 1 if CORRECTIONS[label][1] in ("I", "Z") else -1


def initial_plus(n_qubits: int) -> list[complex]:
    amplitude = 1 / math.sqrt(1 << n_qubits)
    return [complex(amplitude) for _ in range(1 << n_qubits)]


def apply_dressed_cost_block(
    state: list[complex],
    edge: tuple[int, int],
    theta: float,
    label: str,
    epsilon: float,
    phi: float,
) -> None:
    """Apply the physical dressed block frozen in rc_construction_v1.md."""
    control, target = edge
    correction = CORRECTIONS[label]
    sign = label_sign(label)
    _apply_pauli_pair(state, label, control, target)
    _apply_cx(state, control, target)
    angle = (1 + epsilon) * sign * theta + phi
    _apply_single(state, _single_matrix("RZ", angle), target)
    _apply_pauli_pair(state, correction, control, target)
    _apply_cx(state, control, target)


def probabilities(
    context: Context,
    theta: float,
    labels: Sequence[str],
    epsilon: float,
    phi: float,
    *,
    logical_angle_control: bool = False,
) -> tuple[float, ...]:
    if len(labels) != len(context.edges):
        raise ValueError("one label is required for every tagged cost block")
    state = initial_plus(context.n_qubits)
    for edge, label in zip(context.edges, labels, strict=True):
        if logical_angle_control:
            # Labels do not act on the error in this negative control.
            apply_dressed_cost_block(state, edge, (1 + epsilon) * theta + phi, label, 0.0, 0.0)
        else:
            apply_dressed_cost_block(state, edge, theta, label, epsilon, phi)
    for qubit in range(context.n_qubits):
        _apply_single(state, _single_matrix("RX", 2 * context.beta), qubit)
    result = tuple(abs(amplitude) ** 2 for amplitude in state)
    total = sum(result)
    return tuple(value / total for value in result)


def label_patterns(context: Context) -> Iterable[tuple[str, ...]]:
    return itertools.product(LABELS, repeat=len(context.edges))


def _derivatives(
    context: Context,
    theta: float,
    labels: Sequence[str],
    epsilon: float,
    phi: float,
    step: float,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    center = probabilities(context, theta, labels, epsilon, phi)
    plus_e = probabilities(context, theta, labels, epsilon + step, phi)
    minus_e = probabilities(context, theta, labels, epsilon - step, phi)
    plus_p = probabilities(context, theta, labels, epsilon, phi + step)
    minus_p = probabilities(context, theta, labels, epsilon, phi - step)
    d_e = tuple((a - b) / (2 * step) for a, b in zip(plus_e, minus_e, strict=True))
    d_p = tuple((a - b) / (2 * step) for a, b in zip(plus_p, minus_p, strict=True))
    return center, d_e, d_p


def information_matrices(
    context: Context,
    thetas: Sequence[float],
    epsilon: float,
    phi: float,
    *,
    step: float = 1e-6,
) -> dict[str, tuple[tuple[float, float], tuple[float, float]]]:
    """Return I1 and oracle I2 per shot for one candidate design.

    I1 uses the conditional-minus-marginal chain-rule identity. I2 treats the
    exact target response as known and is diagnostic only.
    """
    conditional = [[0.0, 0.0], [0.0, 0.0]]
    marginal = [[0.0, 0.0], [0.0, 0.0]]
    candidates = len(thetas)
    for theta in thetas:
        rows = [_derivatives(context, theta, labels, epsilon, phi, step)
                for labels in label_patterns(context)]
        weight = 1 / (candidates * len(rows))
        for probs, d_e, d_p in rows:
            for probability, de, dp in zip(probs, d_e, d_p, strict=True):
                if probability > 1e-14:
                    conditional[0][0] += weight * de * de / probability
                    conditional[0][1] += weight * de * dp / probability
                    conditional[1][1] += weight * dp * dp / probability
        p_bar = [sum(row[0][b] for row in rows) / len(rows) for b in range(len(rows[0][0]))]
        de_bar = [sum(row[1][b] for row in rows) / len(rows) for b in range(len(rows[0][0]))]
        dp_bar = [sum(row[2][b] for row in rows) / len(rows) for b in range(len(rows[0][0]))]
        for probability, de, dp in zip(p_bar, de_bar, dp_bar, strict=True):
            if probability > 1e-14:
                marginal[0][0] += de * de / (candidates * probability)
                marginal[0][1] += de * dp / (candidates * probability)
                marginal[1][1] += dp * dp / (candidates * probability)
    conditional[1][0] = conditional[0][1]
    marginal[1][0] = marginal[0][1]
    i1 = tuple(tuple(conditional[i][j] - marginal[i][j] for j in range(2)) for i in range(2))
    i2 = tuple(tuple(conditional[i][j] for j in range(2)) for i in range(2))
    return {"I1": i1, "I2": i2}


def eigenvalues_2x2(matrix: Sequence[Sequence[float]]) -> tuple[float, float]:
    a, b, d = matrix[0][0], matrix[0][1], matrix[1][1]
    center = (a + d) / 2
    radius = math.sqrt(max(0.0, ((a - d) / 2) ** 2 + b * b))
    return center - radius, center + radius


def numerical_rank(matrix: Sequence[Sequence[float]]) -> int:
    values = tuple(max(0.0, value) for value in eigenvalues_2x2(matrix))
    largest = max(values)
    tolerance = max(1e-12, 1e-10 * largest)
    return sum(value > tolerance for value in values)
