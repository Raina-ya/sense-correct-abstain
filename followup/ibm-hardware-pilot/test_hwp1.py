"""Local-only checks for the unexecuted HW-P1 Stage A follow-up."""

from __future__ import annotations

import math
from pathlib import Path
import tempfile
import unittest

import analyze_stage_a
import hwp1
import run_stage_a


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

    def test_stage_a_block_has_locked_circuit_and_shot_counts(self) -> None:
        class IdentityPassManager:
            @staticmethod
            def run(circuits):
                return circuits

        pubs, labels = run_stage_a.build_block(0, IdentityPassManager())
        self.assertEqual(len(pubs), 99)
        self.assertEqual(len(labels), 99)
        self.assertEqual(sum(pub[2] for pub in pubs), 16_825)
        self.assertEqual(sum(label["kind"] == "pamp" for label in labels), 90)
        self.assertEqual(sum(label["kind"] == "z_control" for label in labels), 5)
        self.assertEqual(sum(label["kind"] == "readout_calibration" for label in labels), 4)

    def test_lock_hash_is_canonical_across_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lock.json"
            path.write_bytes(b"a\r\nb\r\n")
            first = run_stage_a.canonical_sha256(path)
            path.write_bytes(b"a\nb\n")
            self.assertEqual(first, run_stage_a.canonical_sha256(path))

    def test_calibration_error_uses_per_qubit_marginals(self) -> None:
        records = []
        for prepared in ("00", "01", "10", "11"):
            records.append({
                "label": {"kind": "readout_calibration", "prepared": prepared},
                "counts": {prepared: 950, "00" if prepared != "00" else "11": 50},
            })
        self.assertAlmostEqual(analyze_stage_a.calibration_error(records), 0.05)


if __name__ == "__main__":
    unittest.main()
