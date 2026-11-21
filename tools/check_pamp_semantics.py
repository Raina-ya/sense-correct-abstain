"""Post-lock semantic check (erratum E002): P-amp circuits versus the phase model.

The frozen Gate 1B "noiseless recovery" (`tools/run_gate1b.py`) generated the
P-amp phases from the same linear phase model that the estimator inverts, so it
did not test the circuit semantics. This deterministic check simulates the
frozen P-amp circuits at state-vector level with the frozen gate primitives:

* block B(a) = CX(c,t) - RZ_t((1+epsilon)*a + phi) - CX(c,t), control in |0>,
  target in |+>  (primary synthetic E2 law applied to every commanded angle);
* repetitions R(m, theta) = B(theta)^m, m in {1,4,16}, theta in {pi/8, pi/4};
* echoes E(m) = [B(pi/4) B(-pi/4)]^m, m in {1,4,16};
* target <X> and <Y>.

It compares them with the phase model used by the estimator
(<X>, <Y>) = (cos u, sin u), u = m*theta + m*(epsilon*theta + phi) for
repetitions and u = 2*m*phi for echoes, at every point of the frozen 9-by-9
grid. It is a semantic check, not a recovery or robustness result; it cannot
test visibility loss, context mismatch, or any physical carrier.

Usage: python tools/check_pamp_semantics.py
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate1 import _apply_cx, _apply_single, _single_matrix  # noqa: E402

GRID = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)
CONTROL, TARGET = 1, 0  # qubit 0 is the least-significant bit in gate1.py
TOL = 1e-12


def block(state, angle, epsilon, phi):
    _apply_cx(state, CONTROL, TARGET)
    _apply_single(state, _single_matrix("RZ", (1 + epsilon) * angle + phi), TARGET)
    _apply_cx(state, CONTROL, TARGET)


def target_xy(state):
    # control |0>: amplitudes of |c=0,t=0> and |c=0,t=1> are indices 0 and 1
    a0, a1 = state[0], state[1]
    leak = abs(state[2]) ** 2 + abs(state[3]) ** 2
    x = 2 * (a0.conjugate() * a1).real
    y = 2 * (a0.conjugate() * a1).imag
    return x, y, leak


def initial():
    r = 1 / math.sqrt(2)
    return [complex(r), complex(r), 0j, 0j]  # control |0>, target |+>


def main():
    worst = 0.0
    worst_leak = 0.0
    cases = 0
    for epsilon, phi in itertools.product(GRID, repeat=2):
        for theta in (math.pi / 8, math.pi / 4):
            for m in (1, 4, 16):
                state = initial()
                for _ in range(m):
                    block(state, theta, epsilon, phi)
                x, y, leak = target_xy(state)
                u = m * theta + m * (epsilon * theta + phi)
                worst = max(worst, abs(x - math.cos(u)), abs(y - math.sin(u)))
                worst_leak = max(worst_leak, leak)
                cases += 1
        for m in (1, 4, 16):
            state = initial()
            for _ in range(m):
                block(state, -math.pi / 4, epsilon, phi)
                block(state, math.pi / 4, epsilon, phi)
            x, y, leak = target_xy(state)
            u = 2 * m * phi
            worst = max(worst, abs(x - math.cos(u)), abs(y - math.sin(u)))
            worst_leak = max(worst_leak, leak)
            cases += 1
    if worst > TOL or worst_leak > TOL:
        raise SystemExit(f"P-amp semantic check FAILED: max deviation {worst:.3e}, control leak {worst_leak:.3e}")
    print(f"P-amp semantic check passed: {cases} circuit-grid cases, max deviation {worst:.2e}, "
          f"control leak {worst_leak:.2e}")


if __name__ == "__main__":
    main()
