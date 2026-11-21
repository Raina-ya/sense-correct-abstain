"""Verify canonical SHA-256 hashes of the M6 Gate-3/4 artifacts."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results" / "gate34_artifact_manifest.sha256"


def main() -> None:
    checked = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        expected, relative_path = line.split(maxsplit=1)
        data = (ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(data).hexdigest() != expected:
            raise SystemExit(f"hash mismatch: {relative_path}")
        checked += 1
    print(f"Gate-3/4 artifact manifest passed: {checked} files")


if __name__ == "__main__":
    main()
