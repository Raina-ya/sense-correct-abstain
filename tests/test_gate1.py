from __future__ import annotations

import math
import os
import sys
import unittest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sense_correct_abstain.gate1 import (  # noqa: E402
    G2_PRIMARY,
    G2_SCORE_ZERO,
    G3_PRIMARY,
    LABELS,
    information_matrices,
    label_patterns,
    probabilities,
)
from sense_correct_abstain.pamp import design_eigenvalues, estimate  # noqa: E402


class Gate1ExactTests(unittest.TestCase):
    def test_probabilities_are_normalized(self) -> None:
        for context in (G2_PRIMARY, G3_PRIMARY):
            labels = tuple("II" for _ in context.edges)
            probs = probabilities(context, math.pi / 4, labels, 0.02, -0.01)
            self.assertAlmostEqual(sum(probs), 1.0, places=12)
            self.assertTrue(all(value >= 0 for value in probs))

    def test_phi_zero_is_label_invariant(self) -> None:
        for context in (G2_PRIMARY, G3_PRIMARY):
            reference = probabilities(
                context, math.pi / 4, tuple("II" for _ in context.edges), 0.02, 0.0
            )
            for labels in label_patterns(context):
                actual = probabilities(context, math.pi / 4, labels, 0.02, 0.0)
                self.assertLess(max(abs(a - b) for a, b in zip(actual, reference)), 1e-12)

    def test_logical_angle_control_is_label_blind(self) -> None:
        reference = probabilities(G2_PRIMARY, math.pi / 4, ("II",), 0.02, 0.01,
                                  logical_angle_control=True)
        for label in LABELS:
            actual = probabilities(G2_PRIMARY, math.pi / 4, (label,), 0.02, 0.01,
                                   logical_angle_control=True)
            self.assertLess(max(abs(a - b) for a, b in zip(actual, reference)), 1e-12)

    def test_score_zero_context_has_zero_oracle_information(self) -> None:
        matrices = information_matrices(G2_SCORE_ZERO, (math.pi / 4,), 0.0, 0.0)
        self.assertLess(max(abs(value) for row in matrices["I2"] for value in row), 1e-10)

    def test_i1_epsilon_is_zero_at_phi_zero(self) -> None:
        for context in (G2_PRIMARY, G3_PRIMARY):
            i1 = information_matrices(context, (math.pi / 8, math.pi / 4), 0.02, 0.0)["I1"]
            self.assertLess(abs(i1[0][0]), 1e-9)
            self.assertLess(abs(i1[0][1]), 1e-9)

    def test_pamp_design_has_rank_two(self) -> None:
        eigenvalues = design_eigenvalues()
        self.assertGreater(eigenvalues[0], 0)

    def test_pamp_recovers_frozen_grid(self) -> None:
        grid = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)
        for epsilon in grid:
            for phi in grid:
                epsilon_hat, phi_hat = estimate(epsilon, phi)
                self.assertLessEqual(abs(epsilon_hat - epsilon), 1e-8)
                self.assertLessEqual(abs(phi_hat - phi), 1e-8)


if __name__ == "__main__":
    unittest.main()
