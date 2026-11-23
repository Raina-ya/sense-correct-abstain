"""Create the environment-bound HW-P1 Stage A protocol-lock candidate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "freeze" / "hwp1_stage_a_lock_v2.json"
SNAPSHOT = ROOT / "followup" / "ibm-hardware-pilot" / "environment_snapshot.json"

DESIGN_FILES = (
    "followup/ibm-hardware-pilot/PROTOCOL_DRAFT.md",
    "followup/ibm-hardware-pilot/LOCK_REVIEW.md",
    "followup/ibm-hardware-pilot/cloud_preflight_report_fez.json",
    "followup/ibm-hardware-pilot/cloud_preflight_report_marrakesh.json",
    "followup/ibm-hardware-pilot/dry_run_report.json",
)
CODE_FILES = (
    "followup/ibm-hardware-pilot/prepare_lock.py",
    "followup/ibm-hardware-pilot/cloud_preflight.py",
    "followup/ibm-hardware-pilot/dry_run.py",
    "followup/ibm-hardware-pilot/run_stage_a.py",
    "followup/ibm-hardware-pilot/analyze_stage_a.py",
    "followup/ibm-hardware-pilot/hwp1.py",
    "followup/ibm-hardware-pilot/test_hwp1.py",
    "src/sense_correct_abstain/__init__.py",
    "src/sense_correct_abstain/gate2.py",
)
ENVIRONMENT_FILES = (
    "requirements.txt",
    "followup/ibm-hardware-pilot/requirements.txt",
    "followup/ibm-hardware-pilot/environment_snapshot.json",
)


def sha256(relative: str) -> str:
    data = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "scipy", "qiskit", "qiskit-ibm-runtime")
        },
    }
    SNAPSHOT.write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lock = {
        "schema": "protocol_lock_v2",
        "lock_id": "hwp1_stage_a",
        "design_files": {path: sha256(path) for path in DESIGN_FILES},
        "code_files": {path: sha256(path) for path in CODE_FILES},
        "environment_files": {path: sha256(path) for path in ENVIRONMENT_FILES},
        "environment": environment,
        "seeds": {
            "root": "hwp1",
            "derivation": "SHA256('hwp1|' + '|'.join(parts))[:4], big-endian",
        },
        "command": [
            "python",
            "followup/ibm-hardware-pilot/run_stage_a.py",
            "--submit",
        ],
        "analysis_command": [
            "python",
            "followup/ibm-hardware-pilot/analyze_stage_a.py",
        ],
        "runner": "followup/ibm-hardware-pilot/run_stage_a.py",
        "outputs": ["followup/ibm-hardware-pilot/results/stage_a/"],
        "artifacts": {},
    }
    OUTPUT.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
