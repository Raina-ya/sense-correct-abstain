"""Circuit and analysis helpers for the unexecuted HW-P1 Stage A pilot."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import sys
from typing import Iterable

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from sense_correct_abstain.gate2 import estimate_from_xy  # noqa: E402

M_VALUES = (1, 4, 16)
THETA_VALUES = (math.pi / 8, math.pi / 4)
INJECTED_POINTS = (
    (0.0, 0.0),
    (0.02, 0.0),
    (-0.02, 0.0),
    (0.04, 0.01),
    (-0.04, -0.01),
)
SHOTS = 135
CALIBRATION_SHOTS = 1000
BLOCKS = 8


@dataclass(frozen=True)
class Setting:
    family: str
    theta: float
    repetitions: int
    basis: str


def settings() -> tuple[Setting, ...]:
    result = []
    for theta in THETA_VALUES:
        for repetitions in M_VALUES:
            for basis in ("x", "y"):
                result.append(Setting("repetition", theta, repetitions, basis))
    for repetitions in M_VALUES:
        for basis in ("x", "y"):
            result.append(Setting("echo", math.pi / 4, repetitions, basis))
    return tuple(result)


def seed_for(*parts: object) -> int:
    key = "|".join(str(part) for part in parts)
    return int.from_bytes(hashlib.sha256(f"hwp1|{key}".encode()).digest()[:4], "big")


def _block(circuit: QuantumCircuit, angle: float, epsilon: float, phi: float) -> None:
    circuit.barrier(0, 1)
    circuit.cx(1, 0)
    circuit.rz((1 + epsilon) * angle + phi, 0)
    circuit.cx(1, 0)
    circuit.barrier(0, 1)


def pamp_circuit(setting: Setting, epsilon: float, phi: float, *, measure: bool = True) -> QuantumCircuit:
    circuit = QuantumCircuit(2, 1 if measure else 0)
    circuit.h(0)
    if setting.family == "repetition":
        for _ in range(setting.repetitions):
            _block(circuit, setting.theta, epsilon, phi)
    elif setting.family == "echo":
        for _ in range(setting.repetitions):
            _block(circuit, -setting.theta, epsilon, phi)
            _block(circuit, setting.theta, epsilon, phi)
    else:
        raise ValueError(f"unknown family: {setting.family}")
    if measure:
        if setting.basis == "x":
            circuit.h(0)
        elif setting.basis == "y":
            circuit.sdg(0)
            circuit.h(0)
        elif setting.basis == "z":
            pass
        else:
            raise ValueError(f"unknown basis: {setting.basis}")
        circuit.measure(0, 0)
    return circuit


def z_control_circuit(epsilon: float, phi: float) -> QuantumCircuit:
    setting = Setting("repetition", math.pi / 4, 16, "z")
    return pamp_circuit(setting, epsilon, phi, measure=True)


def calibration_circuits() -> tuple[QuantumCircuit, ...]:
    result = []
    for value in range(4):
        circuit = QuantumCircuit(2, 2, name=f"cal_{value:02b}")
        if value & 1:
            circuit.x(0)
        if value & 2:
            circuit.x(1)
        circuit.measure((0, 1), (0, 1))
        result.append(circuit)
    return tuple(result)


def ideal_xy(setting: Setting, epsilon: float, phi: float) -> tuple[float, float]:
    circuit = pamp_circuit(setting, epsilon, phi, measure=False)
    state = Statevector.from_instruction(circuit)
    x = float(state.expectation_value([[0, 1], [1, 0]], (0,)).real)
    y = float(state.expectation_value([[0, -1j], [1j, 0]], (0,)).real)
    return x, y


def expected_xy(setting: Setting, epsilon: float, phi: float) -> tuple[float, float]:
    if setting.family == "repetition":
        phase = setting.repetitions * setting.theta + setting.repetitions * (
            epsilon * setting.theta + phi
        )
    else:
        phase = 2 * setting.repetitions * phi
    return math.cos(phase), math.sin(phase)


def expectation(counts: dict[str, int]) -> float:
    total = sum(counts.values())
    return (counts.get("0", 0) - counts.get("1", 0)) / total


def estimate_point(values: dict[tuple[str, float, int, str], float]) -> tuple[float, float, float]:
    repetitions = []
    echoes = []
    amplitudes = []
    for theta in THETA_VALUES:
        for m in M_VALUES:
            x = values[("repetition", theta, m, "x")]
            y = values[("repetition", theta, m, "y")]
            repetitions.append((x, y))
            amplitudes.append(math.hypot(x, y))
    for m in M_VALUES:
        x = values[("echo", math.pi / 4, m, "x")]
        y = values[("echo", math.pi / 4, m, "y")]
        echoes.append((x, y))
        amplitudes.append(math.hypot(x, y))
    epsilon_hat, phi_hat = estimate_from_xy(repetitions, echoes)
    return epsilon_hat, phi_hat, sum(amplitudes) / len(amplitudes)


def usage_ledger(blocks: int = BLOCKS) -> dict[str, int | float]:
    pamp_circuits = blocks * len(INJECTED_POINTS) * len(settings())
    control_circuits = blocks * len(INJECTED_POINTS)
    calibration_count = blocks * 4
    pamp_shots = pamp_circuits * SHOTS
    control_shots = control_circuits * SHOTS
    calibration_shots = calibration_count * CALIBRATION_SHOTS
    executions = pamp_shots + control_shots + calibration_shots
    quick_seconds = blocks * 2 + 0.00035 * executions
    return {
        "blocks": blocks,
        "pamp_circuits": pamp_circuits,
        "control_circuits": control_circuits,
        "calibration_circuits": calibration_count,
        "pamp_shots": pamp_shots,
        "control_shots": control_shots,
        "calibration_shots": calibration_shots,
        "executions": executions,
        "quick_seconds": quick_seconds,
        "quick_minutes": quick_seconds / 60,
    }


def circuit_key(setting: Setting) -> tuple[str, float, int, str]:
    return setting.family, setting.theta, setting.repetitions, setting.basis


def iter_point_circuits(epsilon: float, phi: float) -> Iterable[tuple[Setting, QuantumCircuit]]:
    for setting in settings():
        yield setting, pamp_circuit(setting, epsilon, phi)
