"""Compile the research paper from its authoritative LaTeX source.

`paper/technical_report_v1.tex` is the single source of the paper. This script
runs latexmk (pdflatex + BibTeX) in `paper/` and fails with a clear message if
no TeX engine is installed. It builds two layouts of the same text: the
single-column `technical_report_v1.pdf` and the two-column
`technical_report_v1_twocolumn.pdf` (from a wrapper that only switches the
layout). It reads no research data and writes only LaTeX build products and
those two PDFs.

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
TEX_FILES = (PAPER / "technical_report_v1.tex", PAPER / "technical_report_v1_twocolumn.tex")
AUX_SUFFIXES = (".aux", ".bbl", ".blg", ".fdb_latexmk", ".fls", ".log", ".out")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--clean", action="store_true", help="remove LaTeX build products afterwards")
    args = parser.parse_args()

    latexmk = shutil.which("latexmk")
    if latexmk is None:
        print("latexmk not found: install a TeX distribution (TeX Live or MiKTeX) to build the paper", file=sys.stderr)
        return 2
    for tex in TEX_FILES:
        cmd = [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name]
        result = subprocess.run(cmd, cwd=PAPER)
        if result.returncode != 0:
            print(f"LaTeX build failed; see {tex.with_suffix('.log').relative_to(ROOT)}", file=sys.stderr)
            return result.returncode
        if args.clean:
            for suffix in AUX_SUFFIXES:
                tex.with_suffix(suffix).unlink(missing_ok=True)
        print(f"wrote {tex.with_suffix('.pdf').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
