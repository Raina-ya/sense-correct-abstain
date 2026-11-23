"""HW-P1 Stage A: locked artifacts unchanged and the post-lock correction reproduces."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HWP1PostLockTests(unittest.TestCase):
    def test_postlock_record(self) -> None:
        path = ROOT / "tools" / "check_hwp1_postlock.py"
        spec = importlib.util.spec_from_file_location("check_hwp1_postlock", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()
