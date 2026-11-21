import math
import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sense_correct_abstain.gate2 import (  # noqa: E402
    GRAPHS,
    cut_sizes,
    estimate_from_xy,
    nearest_clifford,
    partition,
    score_distribution,
    target_probabilities,
)
from sense_correct_abstain.pamp import M_VALUES, THETA_VALUES  # noqa: E402


class Gate2Tests(unittest.TestCase):
    def test_probabilities_and_score_distribution_are_normalized(self):
        for graph in GRAPHS:
            probs = target_probabilities(graph, math.pi / 8, math.pi / 4, 0.02, 0.01)
            self.assertAlmostEqual(sum(probs), 1.0)
            self.assertAlmostEqual(sum(score_distribution(graph, probs)), 1.0)
            self.assertEqual(len(cut_sizes(graph)), 1 << graph.n_qubits)

    def test_partition_is_deterministic(self):
        self.assertEqual(partition("fixed-key"), partition("fixed-key"))
        self.assertIn(partition("fixed-key"), ("rule-development", "evaluation"))

    def test_nearest_clifford_ties_round_toward_zero(self):
        self.assertEqual(nearest_clifford(math.pi / 4), 0.0)
        self.assertEqual(nearest_clifford(3 * math.pi / 4), math.pi / 2)
        self.assertEqual(nearest_clifford(-math.pi / 4), -0.0)

    def test_xy_estimator_recovers_noiseless_parameters(self):
        epsilon, phi = 0.02, -0.01
        repetitions = []
        for theta in THETA_VALUES:
            for m in M_VALUES:
                phase = m * theta + m * (epsilon * theta + phi)
                repetitions.append((math.cos(phase), math.sin(phase)))
        echoes = [(math.cos(2 * m * phi), math.sin(2 * m * phi)) for m in M_VALUES]
        estimate = estimate_from_xy(repetitions, echoes)
        self.assertAlmostEqual(estimate[0], epsilon)
        self.assertAlmostEqual(estimate[1], phi)


if __name__ == "__main__":
    unittest.main()
