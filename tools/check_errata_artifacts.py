"""Verify the post-lock errata artifact manifest.

Usage: python tools/check_errata_artifacts.py

Checks SHA-256 (after CRLF-to-LF canonicalization) of every file listed in
`results/errata/errata_manifest.sha256`, and that every frozen lock and
artifact manifest is still intact (errata must never modify frozen files).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "errata" / "errata_manifest.sha256"
FROZEN_CHECKERS = (
    "check_gate1_lock.py", "check_gate1_artifacts.py", "check_gate2_lock.py",
    "check_gate2_artifacts.py", "check_gate34_lock.py", "check_gate34_artifacts.py",
)


def main() -> None:
    checked = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        expected, relative_path = line.split(maxsplit=1)
        data = (ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(data).hexdigest() != expected:
            raise SystemExit(f"errata hash mismatch: {relative_path}")
        checked += 1
    for checker in FROZEN_CHECKERS:
        subprocess.run([sys.executable, str(ROOT / "tools" / checker)], check=True,
                       stdout=subprocess.DEVNULL)
    print(f"Errata manifest passed: {checked} files; all {len(FROZEN_CHECKERS)} frozen checks intact")


if __name__ == "__main__":
    main()
