"""Tests for the public archive manifest."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ArchiveManifestTests(unittest.TestCase):
    def test_archive_manifest(self) -> None:
        path = ROOT / "tools" / "check_archive_manifest.py"
        spec = importlib.util.spec_from_file_location("check_archive_manifest", path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()


if __name__ == "__main__":
    unittest.main()
