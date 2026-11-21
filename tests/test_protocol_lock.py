"""Tests for the v2 protocol lock checker (tools/check_protocol_lock.py)."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import platform
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
SPEC = importlib.util.spec_from_file_location("cpl", os.path.join(ROOT, "tools", "check_protocol_lock.py"))
cpl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cpl)


def make_repo(tmp: Path) -> dict:
    (tmp / "src" / "pkg").mkdir(parents=True)
    (tmp / "tools").mkdir()
    (tmp / "docs").mkdir()
    (tmp / "src" / "pkg" / "__init__.py").write_text("")
    (tmp / "src" / "pkg" / "core.py").write_text("X = 1\n")
    (tmp / "src" / "pkg" / "helper.py").write_text("from .core import X\n")
    (tmp / "tools" / "run.py").write_text("from pkg.helper import X\nprint(X)\n")
    (tmp / "docs" / "design.md").write_text("design\n")
    (tmp / "requirements.txt").write_text("numpy\n")
    h = lambda rel: cpl.sha256(tmp / rel)  # noqa: E731
    return {
        "schema": "protocol_lock_v2",
        "lock_id": "test",
        "design_files": {"docs/design.md": h("docs/design.md")},
        "code_files": {r: h(r) for r in ("tools/run.py", "src/pkg/helper.py", "src/pkg/core.py",
                                         "src/pkg/__init__.py")},
        "environment_files": {"requirements.txt": h("requirements.txt")},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "packages": {}},
        "seeds": {"root": 1, "derivation": "fixed"},
        "command": ["python", "tools/run.py"],
        "runner": "tools/run.py",
        "outputs": ["results/out.json"],
    }


class ProtocolLockTests(unittest.TestCase):
    def test_complete_lock_passes_pre(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            lock = make_repo(Path(d))
            self.assertEqual(cpl.check(lock, Path(d), "pre"), [])

    def test_unhashed_local_import_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            lock = make_repo(Path(d))
            del lock["code_files"]["src/pkg/core.py"]
            problems = cpl.check(lock, Path(d), "pre")
            self.assertTrue(any("src/pkg/core.py" in p for p in problems), problems)

    def test_unknown_environment_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            lock = make_repo(Path(d))
            lock["environment"]["python"] = "unknown"
            self.assertTrue(cpl.check(lock, Path(d), "pre", check_environment=False))

    def test_modified_code_fails(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            lock = make_repo(Path(d))
            (Path(d) / "src" / "pkg" / "core.py").write_text("X = 2\n")
            self.assertTrue(any("hash mismatch" in p for p in cpl.check(lock, Path(d), "pre")))

    def test_existing_output_fails_pre_and_post_requires_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            lock = make_repo(Path(d))
            (Path(d) / "results").mkdir()
            (Path(d) / "results" / "out.json").write_text("{}")
            self.assertTrue(any("already exists" in p for p in cpl.check(lock, Path(d), "pre")))
            self.assertTrue(any("artifacts required" in p for p in cpl.check(lock, Path(d), "post")))
            lock["artifacts"] = {"results/out.json": cpl.sha256(Path(d) / "results" / "out.json")}
            self.assertEqual(cpl.check(lock, Path(d), "post"), [])


if __name__ == "__main__":
    unittest.main()
