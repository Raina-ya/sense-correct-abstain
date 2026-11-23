"""Check the HW-P1 Stage A record: locked artifacts unchanged, post-lock files intact.

1. The execution-time lock (`docs/freeze/hwp1_stage_a_lock_v2.json` as committed
   in `ead7168`) still has canonical SHA-256 f4b60e02...; every submission and
   result receipt records that hash.
2. Every artifact hash in the current lock (post-run entries) matches, so the
   raw QPU results and `analysis_primary.json` are unchanged.
3. The append-only HW-P1 errata manifest matches.
4. The post-lock corrected analysis reproduces its stored output from raw counts.

SHA-256 is computed after CRLF-to-LF normalisation, as in the other checks.
Usage: python tools/check_hwp1_postlock.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "docs" / "freeze" / "hwp1_stage_a_lock_v2.json"
EXECUTION_LOCK_COMMIT = "ead7168"
EXECUTION_LOCK_SHA256 = "f4b60e026386769918327196883a74c406179c0356e348262f5ece5ec76f1a56"
PILOT = ROOT / "followup" / "ibm-hardware-pilot"
MANIFEST = PILOT / "errata" / "hwp1_errata_manifest.sha256"


def canonical(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def main() -> int:
    problems: list[str] = []

    committed = subprocess.run(
        ["git", "show", f"{EXECUTION_LOCK_COMMIT}:docs/freeze/hwp1_stage_a_lock_v2.json"],
        cwd=ROOT, capture_output=True,
    )
    if committed.returncode != 0:
        problems.append(f"cannot read the execution-time lock from {EXECUTION_LOCK_COMMIT}")
    elif canonical(committed.stdout) != EXECUTION_LOCK_SHA256:
        problems.append("execution-time lock hash changed")

    receipts = sorted((PILOT / "results" / "stage_a").glob("block_*_*.json"))
    if len(receipts) != 16:
        problems.append(f"expected 16 submission/result receipts, found {len(receipts)}")
    for path in receipts:
        if json.loads(path.read_text(encoding="utf-8")).get("lock_sha256") != EXECUTION_LOCK_SHA256:
            problems.append(f"{path.name} does not record the execution-time lock hash")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    artifacts = lock.get("artifacts", {})
    if len(artifacts) != 17:
        problems.append(f"expected 17 post-run artifact hashes, found {len(artifacts)}")
    for rel, digest in artifacts.items():
        if canonical((ROOT / rel).read_bytes()) != digest:
            problems.append(f"locked artifact changed: {rel}")

    entries = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64})\s+(\S.*)", line.strip())
        if not match:
            problems.append(f"malformed manifest line: {line}")
            continue
        entries += 1
        if canonical((ROOT / match.group(2)).read_bytes()) != match.group(1):
            problems.append(f"post-lock file changed: {match.group(2)}")

    check = subprocess.run(
        [sys.executable, str(PILOT / "analyze_stage_a_postlock.py"), "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if check.returncode != 0:
        problems.append("corrected analysis: " + (check.stderr or check.stdout).strip().splitlines()[-1])

    if problems:
        for problem in problems:
            print(problem)
        print(f"HW-P1 post-lock check FAILED ({len(problems)} problems)")
        return 1
    print(f"HW-P1 post-lock check passed: execution lock {EXECUTION_LOCK_SHA256[:12]} intact, "
          f"16 receipts, 17 locked artifacts, {entries} post-lock files, corrected analysis reproduces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
