"""Check a v2 protocol lock record (E005 §5, E006 §7).

Usage:
    python tools/check_protocol_lock.py <lock.json> --phase pre
    python tools/check_protocol_lock.py <lock.json> --phase post

A v2 lock is a JSON file (see docs/protocols/lock_template_v2.md) with:

    schema            "protocol_lock_v2"
    lock_id           short identifier
    design_files      {path: sha256}      protocol / specification documents
    code_files        {path: sha256}      runner + every local module it imports + tests
    environment_files {path: sha256}      must include requirements.txt
    environment       {"python": "3.x.y", "platform": "...", "packages": {"numpy": "x.y.z", ...}}
    seeds             {"root": int-or-str, "derivation": "..."}  (non-empty)
    command           [argv list]         exact execution command
    runner            path of the entry script (must be in code_files)
    outputs           [paths]             must NOT exist at phase "pre"
    artifacts         {path: sha256}      required at phase "post" (results + logs)

Phase "pre" checks hashes of design, code and environment files, that every
local import of the runner (recursively, within this repository) is hashed,
that the running interpreter and package versions equal the recorded
environment, that seeds and command are present, and that no output exists.
Phase "post" additionally checks every artifact hash and that every declared
output is covered by an artifact entry. SHA-256 is computed after CRLF-to-LF
canonicalization, as in the existing manifests. Unknown environment fields
must be written as the string "unknown" and make phase "pre" fail: a lock
cannot be taken without a known environment.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("schema", "lock_id", "design_files", "code_files", "environment_files", "environment",
            "seeds", "command", "runner", "outputs")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def local_imports(path: Path, root: Path, seen: set[Path]) -> set[Path]:
    """Return repository files imported (recursively) by `path`."""
    if path in seen or not path.exists():
        return seen
    seen.add(path)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level:  # relative import inside a package
                base = path.parent
                for _ in range(node.level - 1):
                    base = base.parent
                names.append(str((base / node.module.replace(".", "/")).relative_to(root)).replace("/", "."))
            else:
                names.append(node.module)
    for name in names:
        rel = Path(*name.split("."))
        for candidate in (root / "src" / rel.with_suffix(".py"), root / "src" / rel / "__init__.py",
                          root / rel.with_suffix(".py"), root / "tools" / rel.with_suffix(".py")):
            if candidate.exists():
                local_imports(candidate, root, seen)
                break
    package_init = path.parent / "__init__.py"
    if path.parent != root and package_init.exists() and package_init not in seen:
        local_imports(package_init, root, seen)
    return seen


def check(lock: dict, root: Path, phase: str, check_environment: bool = True) -> list[str]:
    problems = [f"missing field: {k}" for k in REQUIRED if k not in lock]
    if problems:
        return problems
    if lock["schema"] != "protocol_lock_v2":
        problems.append("schema must be protocol_lock_v2")
    for group in ("design_files", "code_files", "environment_files"):
        if not lock[group]:
            problems.append(f"{group} is empty")
        for rel, expected in lock[group].items():
            path = root / rel
            if not path.exists():
                problems.append(f"{group}: missing file {rel}")
            elif sha256(path) != expected:
                problems.append(f"{group}: hash mismatch {rel}")
    if "requirements.txt" not in lock["environment_files"]:
        problems.append("environment_files must include requirements.txt")
    runner = root / lock["runner"]
    if lock["runner"] not in lock["code_files"]:
        problems.append("runner is not hashed in code_files")
    elif runner.exists():
        for imported in local_imports(runner, root, set()):
            rel = str(imported.relative_to(root)).replace("\\", "/")
            if rel not in lock["code_files"]:
                problems.append(f"local import not hashed in code_files: {rel}")
    env = lock["environment"]
    for key in ("python", "platform", "packages"):
        if key not in env:
            problems.append(f"environment.{key} missing")
    if "python" in env and env["python"] == "unknown":
        problems.append("environment.python is unknown; a lock requires a known environment")
    if check_environment and "python" in env and env["python"] != platform.python_version():
        problems.append(f"python {platform.python_version()} != locked {env['python']}")
    for name, version in env.get("packages", {}).items():
        if version == "unknown":
            problems.append(f"package {name} version unknown")
        elif check_environment:
            try:
                installed = importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:
                installed = None
            if installed != version:
                problems.append(f"package {name} {installed} != locked {version}")
    if not lock["seeds"]:
        problems.append("seeds empty")
    if not lock["command"] or not isinstance(lock["command"], list):
        problems.append("command must be a non-empty argv list")
    if phase == "pre":
        for rel in lock["outputs"]:
            if (root / rel).exists():
                problems.append(f"output already exists before run: {rel}")
    else:
        artifacts = lock.get("artifacts") or {}
        if not artifacts:
            problems.append("artifacts required at phase post")
        for rel, expected in artifacts.items():
            path = root / rel
            if not path.exists():
                problems.append(f"artifact missing: {rel}")
            elif sha256(path) != expected:
                problems.append(f"artifact hash mismatch: {rel}")
        for rel in lock["outputs"]:
            if not any(a == rel or a.startswith(rel.rstrip("/") + "/") for a in artifacts):
                problems.append(f"declared output not covered by artifacts: {rel}")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lock")
    parser.add_argument("--phase", choices=("pre", "post"), required=True)
    args = parser.parse_args()
    lock = json.loads(Path(args.lock).read_text(encoding="utf-8"))
    problems = check(lock, ROOT, args.phase)
    for p in problems:
        print(p)
    if problems:
        raise SystemExit(f"protocol lock check FAILED ({len(problems)} problems)")
    print(f"protocol lock {lock['lock_id']} passed at phase {args.phase}")


if __name__ == "__main__":
    main()
