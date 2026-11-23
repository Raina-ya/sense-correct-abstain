"""Local-only checks for the unexecuted HW-P1 Stage A follow-up."""

from __future__ import annotations

import math
import unittest

import hwp1


class HWP1Tests(unittest.TestCase):
    def test_frozen_design_has_18_settings(self) -> None:
        self.assertEqual(len(hwp1.settings()), 18)

    def test_noiseless_circuits_match_phase_model(self) -> None:
        worst = 0.0
        for epsilon, phi in hwp1.INJECTED_POINTS:
            for setting, _ in hwp1.iter_point_circuits(epsilon, phi):
                observed = hwp1.ideal_xy(setting, epsilon, phi)
                expected = hwp1.expected_xy(setting, epsilon, phi)
                worst = max(worst, *(abs(a - b) for a, b in zip(observed, expected, strict=True)))
        self.assertLessEqual(worst, 1e-12)

    def test_usage_ledger_matches_protocol(self) -> None:
        ledger = hwp1.usage_ledger()
        self.assertEqual(ledger["pamp_shots"], 97_200)
        self.assertEqual(ledger["control_shots"], 5_400)
        self.assertEqual(ledger["calibration_shots"], 32_000)
        self.assertEqual(ledger["executions"], 134_600)
        self.assertTrue(math.isclose(ledger["quick_seconds"], 63.11))

    def test_z_control_has_a_measurement_bit(self) -> None:
        circuit = hwp1.z_control_circuit(0.02, 0.0)
        self.assertEqual(circuit.num_clbits, 1)
        self.assertEqual(circuit.count_ops().get("measure"), 1)


if __name__ == "__main__":
    unittest.main()
