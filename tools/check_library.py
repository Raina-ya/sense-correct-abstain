"""Check structural agreement between library.csv and library_notes.md.

Usage: python tools/check_library.py

Checks: every CSV key has exactly one note heading (#### `key`) and vice
versa, and each note sits under the top-level section (## A, ## B, ...) whose
letter matches the first letter of the key's `theme` column.

This script does not validate bibliographic metadata, evidence levels, or
scientific claims.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "docs" / "literature" / "library.csv"
NOTES_PATH = ROOT / "docs" / "literature" / "library_notes.md"


def main() -> int:
    with CSV_PATH.open(encoding="utf-8") as f:
        themes = {row["key"]: row["theme"] for row in csv.DictReader(f)}

    section = None
    found: dict[str, list[str]] = {}
    for line in NOTES_PATH.read_text(encoding="utf-8").splitlines():
        top = re.match(r"^## ([A-Z]) ", line)
        if top:
            section = top.group(1)
            continue
        note = re.match(r"^#### `([^`]+)`", line)
        if note and section is not None:
            found.setdefault(note.group(1), []).append(section)

    problems = []
    for key in sorted(set(themes) - set(found)):
        problems.append(f"missing note for CSV key: {key}")
    for key in sorted(set(found) - set(themes)):
        problems.append(f"note has no CSV row: {key}")
    for key, sections in sorted(found.items()):
        if len(sections) > 1:
            problems.append(f"duplicate note: {key}")
        if key in themes and sections[0] != themes[key][0]:
            problems.append(
                f"{key}: note under section {sections[0]}, CSV theme {themes[key]}"
            )

    for message in problems:
        print(message)
    print(
        f"{len(themes)} CSV entries, {len(found)} notes, "
        f"{len(problems)} structural problems"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
