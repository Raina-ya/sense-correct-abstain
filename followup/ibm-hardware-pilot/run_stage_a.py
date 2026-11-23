"""Submit the locked HW-P1 Stage A workload, one block at a time.

The runner is inert unless both ``--submit`` and the exact lock-file SHA-256
are supplied.  It never retries a failed block and never starts Stage B.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
from typing import Any

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from hwp1 import (
    BLOCKS,
    CALIBRATION_SHOTS,
    INJECTED_POINTS,
    SHOTS,
    calibration_circuits,
    iter_point_circuits,
    seed_for,
    z_control_circuit,
)

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "docs" / "freeze" / "hwp1_stage_a_lock_v2.json"
OUTPUT = ROOT / "followup" / "ibm-hardware-pilot" / "results" / "stage_a"
BACKEND = "ibm_marrakesh"
TARGET_QUBIT = 53
CONTROL_QUBIT = 54
MAX_EXECUTION_SECONDS = 22


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def backend_snapshot(backend) -> dict[str, Any]:
    properties = backend.properties()
    status = backend.status()
    return {
        "backend": backend.name,
        "status": {
            "operational": status.operational,
            "pending_jobs": status.pending_jobs,
            "status_msg": status.status_msg,
        },
        "properties": jsonable(properties.to_dict() if properties is not None else None),
    }


def build_block(block: int, pass_manager) -> tuple[list[tuple[Any, None, int]], list[dict[str, Any]]]:
    points = list(INJECTED_POINTS)
    random.Random(seed_for("block-order", block)).shuffle(points)
    circuits = []
    labels = []
    shots = []
    for epsilon, phi in points:
        for setting, circuit in iter_point_circuits(epsilon, phi):
            circuits.append(circuit)
            labels.append({
                "kind": "pamp",
                "epsilon": epsilon,
                "phi": phi,
                "family": setting.family,
                "theta": setting.theta,
                "repetitions": setting.repetitions,
                "basis": setting.basis,
            })
            shots.append(SHOTS)
        circuits.append(z_control_circuit(epsilon, phi))
        labels.append({"kind": "z_control", "epsilon": epsilon, "phi": phi})
        shots.append(SHOTS)
    for value, circuit in enumerate(calibration_circuits()):
        circuits.append(circuit)
        labels.append({"kind": "readout_calibration", "prepared": f"{value:02b}"})
        shots.append(CALIBRATION_SHOTS)
    isa = pass_manager.run(circuits)
    for circuit, label in zip(isa, labels, strict=True):
        if label["kind"] == "pamp":
            two_qubit = sum(circuit.count_ops().get(name, 0) for name in ("cz", "ecr", "cx"))
            if two_qubit == 0:
                raise RuntimeError("ISA structure check failed: a P-amp circuit lost every two-qubit gate")
    pubs = [(circuit, None, count) for circuit, count in zip(isa, shots, strict=True)]
    return pubs, labels


def extract_counts(result, labels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for pub_result, label in zip(result, labels, strict=True):
        registers = list(pub_result.data.keys())
        if len(registers) != 1:
            raise RuntimeError(f"expected one classical register, found {registers}")
        counts = getattr(pub_result.data, registers[0]).get_counts()
        records.append({"label": label, "counts": {str(k): int(v) for k, v in counts.items()}})
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submit", action="store_true", help="Required to submit QPU jobs")
    args = parser.parse_args()

    if not args.submit:
        raise SystemExit("inert by default: pass --submit only after owner approval")
    if not LOCK.exists():
        raise SystemExit(f"missing lock: {LOCK}")
    actual_lock_hash = canonical_sha256(LOCK)
    if os.environ.get("HWP1_APPROVED_LOCK_SHA256") != actual_lock_hash:
        raise SystemExit("lock approval hash does not match the current lock file")
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing output: {OUTPUT}")

    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

    service = QiskitRuntimeService(instance="open-instance")
    backend = service.backend(BACKEND, use_fractional_gates=False)
    if not backend.status().operational:
        raise SystemExit(f"backend is not operational: {BACKEND}")
    pass_manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
        initial_layout=[TARGET_QUBIT, CONTROL_QUBIT],
        seed_transpiler=seed_for("cloud-preflight", BACKEND),
    )
    sampler = SamplerV2(mode=backend)
    sampler.options.max_execution_time = MAX_EXECUTION_SECONDS
    sampler.options.dynamical_decoupling.enable = False
    sampler.options.twirling.enable_gates = False
    sampler.options.twirling.enable_measure = False

    OUTPUT.mkdir(parents=True)
    previous_after = None
    for block in range(BLOCKS):
        before = backend_snapshot(backend)
        if previous_after is not None:
            previous_date = previous_after.get("properties", {}).get("last_update_date")
            current_date = before.get("properties", {}).get("last_update_date")
            if previous_date != current_date:
                raise RuntimeError("backend recalibrated between blocks; stopping without retry")
        pubs, labels = build_block(block, pass_manager)
        job = sampler.run(pubs)
        receipt = {
            "study": "HW-P1 Stage A",
            "block": block,
            "backend": BACKEND,
            "job_id": job.job_id(),
            "lock_sha256": actual_lock_hash,
            "snapshot_before": before,
        }
        receipt_path = OUTPUT / f"block_{block:02d}_submission.json"
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"submitted block {block}: job {job.job_id()} -> {receipt_path}")
        result = job.result()
        after = backend_snapshot(backend)
        payload = {
            "study": "HW-P1 Stage A",
            "block": block,
            "backend": BACKEND,
            "physical_qubits": {"target": TARGET_QUBIT, "control": CONTROL_QUBIT},
            "lock_sha256": actual_lock_hash,
            "job_id": job.job_id(),
            "job_metrics": jsonable(job.metrics()),
            "snapshot_before": before,
            "snapshot_after": after,
            "records": extract_counts(result, labels),
        }
        output = OUTPUT / f"block_{block:02d}_result.json"
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"completed block {block}: job {job.job_id()} -> {output}")
        if before.get("properties", {}).get("last_update_date") != after.get("properties", {}).get(
            "last_update_date"
        ):
            raise RuntimeError("backend recalibrated during the block; output retained and stage stopped")
        previous_after = after


if __name__ == "__main__":
    main()
