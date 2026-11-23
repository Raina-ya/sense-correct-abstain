"""Inspect a real IBM backend and transpile HW-P1 without submitting a job."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService

from hwp1 import (
    BLOCKS,
    CALIBRATION_SHOTS,
    INJECTED_POINTS,
    SHOTS,
    calibration_circuits,
    iter_point_circuits,
    seed_for,
    settings,
    usage_ledger,
    z_control_circuit,
)

ROOT = Path(__file__).resolve().parent


def property_error(properties) -> float:
    return float("inf") if properties is None or properties.error is None else float(properties.error)


def choose_pair(backend) -> tuple[int, int, float]:
    target = backend.target
    if "cz" not in target:
        raise RuntimeError("selected backend target has no CZ instruction")
    candidates = []
    for pair, properties in target["cz"].items():
        if pair is None or len(pair) != 2:
            continue
        target_q, control_q = pair
        score = property_error(properties)
        if "measure" in target:
            score += property_error(target["measure"].get((target_q,)))
            score += property_error(target["measure"].get((control_q,)))
        candidates.append((score, target_q, control_q))
    if not candidates:
        raise RuntimeError("no connected CZ pair found")
    score, target_q, control_q = min(candidates)
    return target_q, control_q, score


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", required=True, help="Exact IBM backend name selected by the owner")
    parser.add_argument("--output", type=Path, default=ROOT / "cloud_preflight_report.json")
    args = parser.parse_args()

    service = QiskitRuntimeService()
    backend = service.backend(args.backend, use_fractional_gates=False)
    target_q, control_q, score = choose_pair(backend)
    pass_manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=1,
        initial_layout=[target_q, control_q],
        seed_transpiler=seed_for("cloud-preflight", args.backend),
    )

    unique = []
    for epsilon, phi in INJECTED_POINTS:
        unique.extend(circuit for _, circuit in iter_point_circuits(epsilon, phi))
    unique.extend(z_control_circuit(epsilon, phi) for epsilon, phi in INJECTED_POINTS)
    unique.extend(calibration_circuits())
    isa = pass_manager.run(unique)
    two_qubit_counts = [sum(circuit.count_ops().get(name, 0) for name in ("cz", "ecr", "cx")) for circuit in isa]
    pamp_count = len(INJECTED_POINTS) * len(settings())
    if any(count == 0 for count in two_qubit_counts[:pamp_count]):
        raise RuntimeError("ISA structure check failed: a P-amp circuit lost every two-qubit gate")

    durations = []
    for circuit in isa:
        try:
            durations.append(float(circuit.estimate_duration(backend.target)))
        except Exception:
            durations.append(None)
    ledger = usage_ledger(BLOCKS)
    report = {
        "status": "preflight only; no hardware job submitted",
        "backend": backend.name,
        "processor_type": getattr(backend, "processor_type", None),
        "selected_physical_qubits": {"target": target_q, "control": control_q},
        "selection_score": score,
        "use_fractional_gates": False,
        "unique_circuits_transpiled": len(isa),
        "pamp_circuits_with_two_qubit_gate": sum(count > 0 for count in two_qubit_counts[:pamp_count]),
        "depth": {"min": min(circuit.depth() for circuit in isa), "max": max(circuit.depth() for circuit in isa)},
        "duration_seconds": {
            "available": all(value is not None for value in durations),
            "unique_min": min(value for value in durations if value is not None) if any(value is not None for value in durations) else None,
            "unique_max": max(value for value in durations if value is not None) if any(value is not None for value in durations) else None,
        },
        "design_ledger": ledger,
        "shots": {"pamp": SHOTS, "calibration": CALIBRATION_SHOTS},
        "seed_transpiler": seed_for("cloud-preflight", args.backend),
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
