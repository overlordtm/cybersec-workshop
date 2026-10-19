#!/usr/bin/env python3
"""Print active participant claim codes as ten cut-out slips per A4 sheet.

The PDF contains private claim codes. Default input and output are in secrets/.
Requires reportlab (see requirements-credentials.txt).
"""
import argparse
import csv
import math
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

INFRA = Path(__file__).resolve().parent
DEFAULT_URL = "https://overlordtm.github.io/cybersec-workshop/cybersec-201/vaje/dostop/"
COLUMNS, ROWS = 2, 5


def read_codes(path, access="all"):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"user", "access", "claim_code", "active"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain user,access,claim_code,active columns")
        rows = []
        users, codes = set(), set()
        for row in reader:
            if row["active"] != "yes" or row["access"] not in ("kali", "wireguard"):
                continue
            if access != "all" and row["access"] != access:
                continue
            prefix = "1" if row["access"] == "kali" else "2"
            if not re.fullmatch(rf"udelezenec{prefix}[0-9]{{2}}", row["user"]):
                raise ValueError(f"Invalid participant identity on CSV line {reader.line_num}")
            if not re.fullmatch(r"[A-Z]{4}-[0-9]{4}", row["claim_code"]):
                raise ValueError(f"Invalid claim code on CSV line {reader.line_num}; rerun lab.sh credentials")
            if row["user"] in users or row["claim_code"] in codes:
                raise ValueError(f"Duplicate participant or claim code on CSV line {reader.line_num}")
            users.add(row["user"])
            codes.add(row["claim_code"])
            rows.append(row)
    if not rows:
        raise ValueError("No active participant claim codes match the requested access type")
    return sorted(rows, key=lambda r: r["user"])


def register_fonts():
    # ReportLab ships these fonts, so the printed layout needs no system fonts.
    import reportlab
    font_dir = Path(reportlab.__file__).parent / "fonts"
    for name, filename in (("Slip", "Vera.ttf"), ("SlipBold", "VeraBd.ttf")):
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))


def draw_slip(pdf, row, url, qr, x, y, width, height):
    left = x + 5 * mm
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("SlipBold", 10)
    pdf.drawString(left, y + height - 7 * mm, row["user"])
    pdf.setFont("Slip", 8)
    label = "Kali v brskalniku" if row["access"] == "kali" else "Lastna Kali VM / WireGuard"
    pdf.drawString(left, y + height - 12 * mm, label)
    pdf.setFont("Courier-Bold", 22)
    pdf.drawString(left, y + height - 23 * mm, row["claim_code"])
    pdf.setFont("Slip", 7.5)
    pdf.drawString(left, y + height - 29 * mm, "Odpri stran in vnesi kodo.")
    pdf.drawString(left, y + height - 33 * mm, "Osebna koda — ne deli je.")
    # The QR code contains only the public page URL, never the private claim code.
    renderPDF.draw(qr, pdf, x + width - 28 * mm, y + 3 * mm)
    style = ParagraphStyle("url", fontName="Slip", fontSize=6.5, leading=8,
                           splitLongWords=True, textColor="black")
    paragraph = Paragraph(escape(url), style)
    _, used_height = paragraph.wrap(width - 36 * mm, 18 * mm)
    if used_height > 15 * mm:
        raise ValueError("Page URL is too long for a slip; use a shorter public URL")
    paragraph.drawOn(pdf, left, y + 3 * mm)


def generate_pdf(input_path, output_path, url=DEFAULT_URL, access="all"):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Page URL must be a public HTTPS URL without credentials, query, or fragment")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("PDF output must differ from the input CSV")
    rows = read_codes(input_path, access)
    register_fonts()
    widget = QrCodeWidget(url)
    x0, y0, x1, y1 = widget.getBounds()
    size = 24 * mm
    qr = Drawing(size, size, transform=[size / (x1 - x0), 0, 0, size / (y1 - y0), 0, 0])
    qr.add(widget)
    width, height = A4
    margin = 10 * mm
    grid_top = height - 20 * mm
    grid_bottom = 12 * mm
    cell_width = (width - 2 * margin) / COLUMNS
    cell_height = (grid_top - grid_bottom) / ROWS
    page_count = math.ceil(len(rows) / (COLUMNS * ROWS))
    output_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(suffix=".pdf", dir=output_path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            pdf = canvas.Canvas(out, pagesize=A4)
            pdf.setTitle("Cybersec-201 — osebne kode za dostop")
            pdf.setAuthor("Cybersec-201")
            for page in range(page_count):
                pdf.setFillColorRGB(0, 0, 0)
                pdf.setFont("SlipBold", 10)
                pdf.drawString(margin, height - 10 * mm, "CYBERSEC–201 / Dostop do laboratorija")
                pdf.setFont("Slip", 7)
                pdf.drawRightString(width - margin, height - 10 * mm, f"{page + 1} / {page_count}")
                pdf.setStrokeColorRGB(.6, .6, .6)
                pdf.setLineWidth(.4)
                pdf.setDash(2, 3)
                for col in range(COLUMNS + 1):
                    x = margin + col * cell_width
                    pdf.line(x, grid_bottom, x, grid_top)
                for line in range(ROWS + 1):
                    y = grid_bottom + line * cell_height
                    pdf.line(margin, y, width - margin, y)
                pdf.setDash()
                start = page * COLUMNS * ROWS
                for index, row in enumerate(rows[start:start + COLUMNS * ROWS]):
                    x = margin + (index % COLUMNS) * cell_width
                    y = grid_top - (index // COLUMNS + 1) * cell_height
                    draw_slip(pdf, row, url, qr, x, y, cell_width, cell_height)
                pdf.setFillColorRGB(0, 0, 0)
                pdf.setFont("Slip", 7)
                pdf.drawString(margin, 6 * mm, "A4 · 100 % · izrezi po vodilih")
                pdf.showPage()
            pdf.save()
        os.replace(temporary, output_path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return len(rows), page_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INFRA / "secrets/claim-codes.csv")
    parser.add_argument("--output", type=Path, default=INFRA / "secrets/claim-slips.pdf")
    parser.add_argument("--url", default=DEFAULT_URL, help="Public URL of the credential pickup page")
    parser.add_argument("--access", choices=("all", "kali", "wireguard"), default="all")
    args = parser.parse_args()
    try:
        count, pages = generate_pdf(args.input, args.output, args.url, args.access)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Cannot generate claim slips: {error}\n")
    print(f"Generated {count} slips on {pages} A4 pages: {args.output}")
