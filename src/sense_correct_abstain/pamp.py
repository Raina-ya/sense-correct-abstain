"""Frozen P-amp estimator used only after the Gate-1A failure."""

from __future__ import annotations

import math


M_VALUES = (1, 4, 16)
THETA_VALUES = (math.pi / 8, math.pi / 4)


def wrap(angle: float) -> float:
    return (angle + math.pi) % (2 * math.pi) - math.pi


def phase_from_xy(x_expectation: float, y_expectation: float) -> float:
    if abs(x_expectation) < 1e-15 and abs(y_expectation) < 1e-15:
        raise ValueError("undefined atan2 phase")
    return math.atan2(y_expectation, x_expectation)


def design_rows() -> list[tuple[float, float]]:
    rows = [(m * theta, m) for theta in THETA_VALUES for m in M_VALUES]
    rows.extend((0.0, 2 * m) for m in M_VALUES)
    return rows


def exact_residuals(epsilon: float, phi: float) -> list[float]:
    residuals = []
    for theta in THETA_VALUES:
        previous_per_block = None
        for m in M_VALUES:
            total = m * theta + m * (epsilon * theta + phi)
            measured = phase_from_xy(math.cos(total), math.sin(total))
            residual = wrap(measured - wrap(m * theta))
            per_block = residual / m
            if previous_per_block is not None:
                candidates = [per_block + 2 * math.pi * k / m for k in range(-m, m + 1)]
                per_block = min(candidates, key=lambda value: abs(value - previous_per_block))
                residual = m * per_block
            previous_per_block = per_block
            residuals.append(residual)
    previous_per_block = None
    for m in M_VALUES:
        total = 2 * m * phi
        measured = phase_from_xy(math.cos(total), math.sin(total))
        residual = wrap(measured)
        per_block = residual / (2 * m)
        if previous_per_block is not None:
            candidates = [per_block + math.pi * k / m for k in range(-m, m + 1)]
            per_block = min(candidates, key=lambda value: abs(value - previous_per_block))
            residual = 2 * m * per_block
        previous_per_block = per_block
        residuals.append(residual)
    return residuals


def estimate(epsilon: float, phi: float) -> tuple[float, float]:
    rows = design_rows()
    residuals = exact_residuals(epsilon, phi)
    a = sum(x * x for x, _ in rows)
    b = sum(x * y for x, y in rows)
    c = sum(y * y for _, y in rows)
    u = sum(x * value for (x, _), value in zip(rows, residuals, strict=True))
    v = sum(y * value for (_, y), value in zip(rows, residuals, strict=True))
    determinant = a * c - b * b
    if determinant <= 0:
        raise ValueError("nonunique least-squares design")
    return (c * u - b * v) / determinant, (a * v - b * u) / determinant


def design_eigenvalues() -> tuple[float, float]:
    rows = design_rows()
    a = sum(x * x for x, _ in rows)
    b = sum(x * y for x, y in rows)
    c = sum(y * y for _, y in rows)
    center = (a + c) / 2
    radius = math.sqrt(((a - c) / 2) ** 2 + b * b)
    return center - radius, center + radius
