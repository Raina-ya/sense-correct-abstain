"""Verify the frozen Gate-3/4 design manifest before M6 execution."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "freeze" / "gate3_gate4_design_manifest.sha256"


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
    if checked != 1:
        raise SystemExit(f"expected 1 locked file, found {checked}")
    print("Gate-3/4 design lock passed: 1 file")


if __name__ == "__main__":
    main()
