import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sense_correct_abstain.gate34 import policy_action, quantile_linear, split99_graphs  # noqa: E402


class Gate34Tests(unittest.TestCase):
    def test_split99_is_unique_connected_and_deterministic(self):
        graphs = split99_graphs()
        self.assertEqual(len(graphs), 99)
        self.assertEqual(graphs, split99_graphs())
        signatures = {(graph.n_qubits, graph.edges) for graph in graphs}
        self.assertEqual(len(signatures), 99)
        for graph in graphs:
            reached = {0}
            while True:
                expanded = reached | {v for edge in graph.edges if edge[0] in reached or edge[1] in reached for v in edge}
                if expanded == reached:
                    break
                reached = expanded
            self.assertEqual(len(reached), graph.n_qubits)

    def test_policy_order(self):
        common = dict(estimate_defined=True, unambiguous=True, epsilon_hat=0.04,
                      phi_hat=0.0, g0_hat=0.01, se_g0=0.001, instability_bound=0.02)
        self.assertEqual(policy_action(**common), "C")
        common.update(g0_hat=0.001, instability_bound=0.0001)
        self.assertEqual(policy_action(**common), "A")
        common.update(g0_hat=0.1)
        self.assertEqual(policy_action(**common), "N")
        common.update(estimate_defined=False)
        self.assertEqual(policy_action(**common), "A")

    def test_linear_quantile(self):
        self.assertEqual(quantile_linear([0.0, 10.0], 0.25), 2.5)


if __name__ == "__main__":
    unittest.main()
