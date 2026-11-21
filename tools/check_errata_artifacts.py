"""Verify the post-lock errata manifests (append-only).

Usage: python tools/check_errata_artifacts.py

* Checks SHA-256 (after CRLF-to-LF canonicalization) of every file listed in
  every `results/errata/errata_manifest*.sha256` (v1 from 9201ba9, v2 from E006).
* Living documents (E006 §6) are verified against their blob in the commit
  that created the manifest entry, not against the working tree, so status can
  be updated without weakening the record.
* Re-runs every frozen lock and artifact checker (errata must never modify
  frozen files).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "results" / "errata"
LIVING = {"docs/results/project_status.md": "9201ba9"}  # path -> commit holding the hashed snapshot
FROZEN_CHECKERS = (
    "check_gate1_lock.py", "check_gate1_artifacts.py", "check_gate2_lock.py",
    "check_gate2_artifacts.py", "check_gate34_lock.py", "check_gate34_artifacts.py",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    checked = 0
    manifests = sorted(MANIFEST_DIR.glob("errata_manifest*.sha256"))
    if not manifests:
        raise SystemExit("no errata manifest found")
    for manifest in manifests:
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            expected, relative_path = line.split(maxsplit=1)
            if relative_path in LIVING:
                data = subprocess.run(["git", "show", f"{LIVING[relative_path]}:{relative_path}"],
                                      cwd=ROOT, check=True, capture_output=True).stdout
            else:
                data = (ROOT / relative_path).read_bytes()
            if digest(data) != expected:
                raise SystemExit(f"errata hash mismatch: {relative_path} ({manifest.name})")
            checked += 1
    for checker in FROZEN_CHECKERS:
        subprocess.run([sys.executable, str(ROOT / "tools" / checker)], check=True,
                       stdout=subprocess.DEVNULL)
    print(f"Errata manifests passed: {len(manifests)} manifests, {checked} entries "
          f"({len(LIVING)} living document checked against its commit); "
          f"all {len(FROZEN_CHECKERS)} frozen checks intact")


if __name__ == "__main__":
    main()
