"""Build the MT7 report's LaTeX source and a deterministic review PDF.

The LaTeX file is the publication source.  The PDF is generated with ReportLab
because the archived development environment does not include a TeX engine.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = ROOT / "paper" / "technical_report_v1.md"
TEX = ROOT / "paper" / "technical_report_v1.tex"
PDF = ROOT / "paper" / "technical_report_v1.pdf"
rl_config.invariant = 1


def blocks(text: str):
    paragraph: list[str] = []

    def flush():
        nonlocal paragraph
        if paragraph:
            yield ("p", " ".join(line.strip() for line in paragraph))
            paragraph = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            yield from flush()
        elif line.startswith("### "):
            yield from flush()
            yield ("h3", line[4:])
        elif line.startswith("## "):
            yield from flush()
            yield ("h2", line[3:])
        elif line.startswith("# "):
            yield from flush()
            yield ("title", line[2:])
        elif line.startswith("- ") or re.match(r"^\d+\. ", line):
            yield from flush()
            yield ("li", re.sub(r"^(?:- |\d+\. )", "", line))
        elif line.startswith("> "):
            yield from flush()
            yield ("quote", line[2:])
        else:
            paragraph.append(line)
    yield from flush()


def latex_escape(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    code: list[str] = []

    def save_code(match):
        code.append(match.group(1))
        return f"@@CODE{len(code) - 1}@@"

    value = re.sub(r"`([^`]+)`", save_code, value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", value)
    for old, new in [
        ("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
        ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
        ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
    ]:
        value = value.replace(old, new)
    value = value.replace(r"\textbackslash{}textbf\{", r"\textbf{")
    for index, item in enumerate(code):
        escaped = item.replace("\\", r"\textbackslash{}").replace("_", r"\_")
        value = value.replace(f"@@CODE{index}@@", rf"\texttt{{{escaped}}}")
    return value


def build_tex(text: str) -> None:
    output = [r"""\documentclass[10pt,twocolumn]{article}
\usepackage[letterpaper,margin=0.68in,columnsep=0.24in]{geometry}
\usepackage{microtype}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
\usepackage{enumitem}
\setlist{nosep,leftmargin=*}
\title{Sense, Correct, or Abstain:\\A Fixed-Budget Decision Study of Angle-Proportional Coherent Error in QAOA}
\author{Zhen-Jun Liu}
\date{Final MT7 technical report, 23 November 2026\\\href{https://doi.org/10.5281/zenodo.24443391}{doi:10.5281/zenodo.24443391}}
\begin{document}
\maketitle
"""]
    in_abstract = False
    in_list = False
    skip_refs = False
    for kind, value in blocks(text):
        if kind == "title" or value.startswith("**Author:") or value.startswith("**Status:") or value.startswith("**Version DOI:"):
            continue
        if kind == "h2" and value == "Abstract":
            output.append(r"\begin{abstract}")
            in_abstract = True
            continue
        if in_abstract and kind == "h2":
            output.append(r"\end{abstract}")
            in_abstract = False
        if kind == "h2" and value == "References":
            skip_refs = True
            break
        if kind != "li" and in_list:
            output.append(r"\end{itemize}")
            in_list = False
        clean = latex_escape(value)
        if kind == "h2":
            output.append(rf"\section{{{clean}}}")
        elif kind == "h3":
            output.append(rf"\subsection{{{clean}}}")
        elif kind == "li":
            if not in_list:
                output.append(r"\begin{itemize}")
                in_list = True
            output.append(rf"\item {clean}")
        elif kind == "quote":
            output.append(rf"\begin{{quote}}{clean}\end{{quote}}")
        elif kind == "p":
            output.append(clean + "\n")
    if in_list:
        output.append(r"\end{itemize}")
    if in_abstract:
        output.append(r"\end{abstract}")
    if not skip_refs:
        output.append(r"\section{References}")
    output.extend([
        r"\nocite{*}",
        r"\bibliographystyle{abbrv}",
        r"\bibliography{references}",
        r"\end{document}",
    ])
    TEX.write_text("\n".join(output) + "\n", encoding="utf-8")


def pdf_markup(value: str) -> str:
    value = html.escape(value)
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", value)
    return value


def build_pdf(text: str) -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.3, leading=10.2, spaceAfter=4)
    h2 = ParagraphStyle("H2", parent=body, fontName="Helvetica-Bold", fontSize=11, leading=12.5, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle("H3", parent=body, fontName="Helvetica-Bold", fontSize=9, leading=10.5, spaceBefore=6, spaceAfter=3)
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15, leading=17, alignment=TA_CENTER, spaceAfter=8)
    meta = ParagraphStyle("Meta", parent=body, fontName="Helvetica", fontSize=8, leading=10, alignment=TA_CENTER, spaceAfter=3)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=10, firstLineIndent=-7, bulletIndent=2)
    quote = ParagraphStyle("Quote", parent=body, leftIndent=10, rightIndent=8, borderColor=colors.HexColor("#777777"), borderWidth=0.6, borderPadding=5)

    story = []
    for kind, value in blocks(text):
        markup = pdf_markup(value)
        if kind == "title":
            story.append(Paragraph(markup, title))
        elif kind == "h2":
            story.append(Paragraph(markup, h2))
        elif kind == "h3":
            story.append(Paragraph(markup, h3))
        elif kind == "li":
            story.append(KeepTogether([Paragraph("&#8226; " + markup, bullet)]))
        elif kind == "quote":
            story.append(Paragraph(markup, quote))
        elif kind == "p":
            style = meta if value.startswith("**Author:") or value.startswith("**Status:") or value.startswith("**Version DOI:") or value.startswith("**Evidence boundary:") else body
            story.append(Paragraph(markup, style))
    story.insert(1, Spacer(1, 3))

    page_w, page_h = letter
    margin = 0.58 * inch
    gap = 0.22 * inch
    frame_w = (page_w - 2 * margin - gap) / 2
    frames = [
        Frame(margin, margin, frame_w, page_h - 2 * margin, id="left", leftPadding=0, rightPadding=4),
        Frame(margin + frame_w + gap, margin, frame_w, page_h - 2 * margin, id="right", leftPadding=4, rightPadding=0),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(margin, 0.34 * inch, "Sense, Correct, or Abstain - analytic and synthetic evidence only")
        canvas.drawRightString(page_w - margin, 0.34 * inch, f"{doc.page}")
        canvas.restoreState()

    doc = BaseDocTemplate(str(PDF), pagesize=letter, leftMargin=margin, rightMargin=margin, topMargin=margin, bottomMargin=margin, title="Sense, Correct, or Abstain", author="Zhen-Jun Liu")
    doc.addPageTemplates(PageTemplate(id="two-column", frames=frames, onPage=footer))
    doc.build(story)


def main() -> None:
    text = MARKDOWN.read_text(encoding="utf-8")
    build_tex(text)
    build_pdf(text)
    print(f"wrote {TEX.relative_to(ROOT)}")
    print(f"wrote {PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
