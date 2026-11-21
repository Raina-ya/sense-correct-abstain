"""Deterministic tests for the post-lock audit tools (errata E001-E004)."""

from __future__ import annotations

import importlib.util
import itertools
import math
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ErrataTests(unittest.TestCase):
    def test_pamp_circuits_match_phase_model(self) -> None:
        load("check_pamp_semantics").main()  # raises SystemExit on any deviation > 1e-12

    def test_epsilon_efficient_information_is_zero_at_phi_zero(self) -> None:
        audit = load("audit_gate1a_efficient_information")
        from sense_correct_abstain.gate1 import G2_PRIMARY, G3_PRIMARY
        for context, (name, thetas) in itertools.product((G2_PRIMARY, G3_PRIMARY), audit.DESIGNS.items()):
            for epsilon in (-0.04, 0.0, 0.02):
                full, eff = audit.efficient_information(context, thetas, epsilon, 0.0)
                self.assertLess(abs(eff[0, 0]), 1e-12, (context.name, name, epsilon))
                self.assertGreater(full[0, 0], 0.1)  # oracle information is not zero

    def test_phi_efficient_information_positive_at_phi_zero(self) -> None:
        audit = load("audit_gate1a_efficient_information")
        from sense_correct_abstain.gate1 import G2_PRIMARY
        _, eff = audit.efficient_information(G2_PRIMARY, (math.pi / 4,), 0.02, 0.0)
        self.assertGreater(eff[1, 1], 0.5)

    def test_g2_efficient_information_zero_at_phi_nonzero(self) -> None:
        audit = load("audit_gate1a_efficient_information")
        from sense_correct_abstain.gate1 import G2_PRIMARY
        _, eff = audit.efficient_information(G2_PRIMARY, (math.pi / 8, math.pi / 4), 0.02, 0.01)
        self.assertLess(abs(eff).max(), 1e-12)


if __name__ == "__main__":
    unittest.main()
