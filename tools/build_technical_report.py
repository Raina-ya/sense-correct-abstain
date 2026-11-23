"""Compile the research paper from its authoritative LaTeX source.

`paper/technical_report_v1.tex` is the single source of the paper. This script
runs latexmk (pdflatex + BibTeX) in `paper/` and fails with a clear message if
no TeX engine is installed. It reads no research data and writes only LaTeX
build products and `paper/technical_report_v1.pdf`.

Earlier versions generated the `.tex` from a Markdown summary and drew the PDF
with ReportLab; that path was retired when the paper was expanded (see
`docs/audits/rigor_review_2026-11-23.md`, item 15), so that the PDF is always a
rendering of the `.tex`.

Usage: python tools/build_technical_report.py [--clean]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
TEX = PAPER / "technical_report_v1.tex"
PDF = PAPER / "technical_report_v1.pdf"
AUX_SUFFIXES = (".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--clean", action="store_true", help="remove LaTeX build products afterwards")
    args = parser.parse_args()

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        print("latexmk not found: install a TeX distribution (TeX Live or MiKTeX) to build the paper", file=sys.stderr)
        return 2
    cmd = [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", TEX.name]
    result = subprocess.run(cmd, cwd=PAPER)
    if result.returncode != 0:
        print(f"LaTeX build failed; see {TEX.with_suffix('.log').relative_to(ROOT)}", file=sys.stderr)
        return result.returncode
    if args.clean:
        for suffix in AUX_SUFFIXES:
            TEX.with_suffix(suffix).unlink(missing_ok=True)
    print(f"wrote {PDF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
