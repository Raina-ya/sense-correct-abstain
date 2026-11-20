"""Deterministic semantic check for the frozen MT2 RC cost block.

This is a circuit-identity check, not a research simulation.  It enumerates all
16 two-qubit Pauli labels and checks noiseless equivalence of the dressed
CX-RZ-CX block at several angles.
"""

from __future__ import annotations

import itertools
import cmath
import math

I = ((1, 0), (0, 1))
X = ((0, 1), (1, 0))
Y = ((0, -1j), (1j, 0))
Z = ((1, 0), (0, -1))
PAULIS = {"I": I, "X": X, "Y": Y, "Z": Z}


def matmul(*matrices):
    result = matrices[0]
    for right in matrices[1:]:
        result = tuple(
            tuple(sum(result[row][k] * right[k][col] for k in range(len(right)))
                  for col in range(len(right[0])))
            for row in range(len(result))
        )
    return result


def kron(left, right):
    return tuple(
        tuple(left[i][j] * right[k][ell]
              for j in range(len(left[0])) for ell in range(len(right[0])))
        for i in range(len(left)) for k in range(len(right))
    )


def rz(angle: float):
    return (
        (cmath.exp(-0.5j * angle), 0),
        (0, cmath.exp(0.5j * angle)),
    )


def on_target(operation):
    return kron(I, operation)


def close(left, right) -> bool:
    return all(
        abs(left[row][col] - right[row][col]) <= 1e-12
        for row in range(len(left)) for col in range(len(left[0]))
    )


def equal_up_to_global_phase(left, right) -> bool:
    for row in range(len(left)):
        for col in range(len(left[0])):
            if abs(right[row][col]) > 1e-12:
                phase = left[row][col] / right[row][col]
                return close(left, tuple(
                    tuple(phase * value for value in target_row) for target_row in right
                ))
    return close(left, right)


def main() -> None:
    hard = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0))
    angles = (0.0, 0.37, -0.91, math.pi)
    checked = 0
    for control_label, target_label in itertools.product(PAULIS, repeat=2):
        twirl = kron(PAULIS[control_label], PAULIS[target_label])
        correction = matmul(hard, twirl, hard)
        sign = 1 if close(matmul(correction, on_target(Z)), matmul(on_target(Z), correction)) else -1
        for angle in angles:
            bare = matmul(hard, on_target(rz(angle)), hard)
            dressed = matmul(hard, correction, on_target(rz(sign * angle)), hard, twirl)
            if not equal_up_to_global_phase(dressed, bare):
                raise AssertionError(
                    f"failed label {control_label}{target_label}, angle {angle}"
                )
            checked += 1
    print(f"RC semantic check passed: {checked} label-angle cases")


if __name__ == "__main__":
    main()
