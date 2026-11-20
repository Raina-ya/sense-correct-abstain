"""Check arithmetic invariants in the frozen M3 Gate-1 design lock.

This validates protocol arithmetic only. It does not evaluate Gate 1A or 1B.
"""

from __future__ import annotations

import math
import hashlib
from pathlib import Path


TOTAL_SHOTS = 24_300
SENSING_FRACTION = 0.10
SETTINGS = 18
SHOTS_PER_SETTING = 135
EPSILON_MIN = 0.02
GRID = (-0.04, -0.02, -0.01, -0.005, 0.0, 0.005, 0.01, 0.02, 0.04)
M_VALUES = (1, 4, 16)
THETA_VALUES = (math.pi / 8, math.pi / 4)
REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "docs" / "freeze" / "gate1_design_lock_manifest.sha256"


def epsilon_standard_error() -> float:
    rows = [(m * theta, m) for theta in THETA_VALUES for m in M_VALUES]
    rows.extend((0.0, 2 * m) for m in M_VALUES)
    a = sum(x * x for x, _ in rows)
    b = sum(x * y for x, y in rows)
    c = sum(y * y for _, y in rows)
    inverse_00 = c / (a * c - b * b)
    return math.sqrt(inverse_00 / SHOTS_PER_SETTING)


def check_manifest() -> int:
    checked = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        expected, relative_path = line.split(maxsplit=1)
        data = (REPO_ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
        actual = hashlib.sha256(data).hexdigest()
        assert actual == expected, f"hash mismatch: {relative_path}"
        checked += 1
    return checked


def main() -> None:
    sensing_shots = round(TOTAL_SHOTS * SENSING_FRACTION)
    assert sensing_shots == 2_430
    assert SETTINGS * SHOTS_PER_SETTING == sensing_shots

    for epsilon in GRID:
        for phi in GRID:
            assert 32 * abs(phi) < math.pi / 2
            for theta in THETA_VALUES:
                assert 16 * abs(epsilon * theta + phi) < math.pi / 2

    standard_error = epsilon_standard_error()
    threshold = EPSILON_MIN / 2.8
    assert standard_error <= threshold
    manifest_files = check_manifest()
    print(
        "Gate-1 lock arithmetic passed: "
        f"sensing_shots={sensing_shots}, shots_per_setting={SHOTS_PER_SETTING}, "
        f"SE(epsilon)={standard_error:.8f}, threshold={threshold:.8f}, "
        f"grid_points={len(GRID) ** 2}, manifest_files={manifest_files}"
    )


if __name__ == "__main__":
    main()
