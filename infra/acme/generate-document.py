#!/usr/bin/env python3
"""Rebuild the deterministic training PDF for HTTP and SMB (no dependencies)."""

from pathlib import Path


def build_pdf():
    # ASCII is intentional: the metadata name can be compared with Maja Kovač
    # on the company website without needing embedded PDF fonts.
    stream = (
        b"BT /F1 22 Tf 60 760 Td (ACME - cenik 2026) Tj "
        b"/F1 12 Tf 0 -40 Td (Ucni dokument za delavnico Cybersec-201.) Tj "
        b"0 -28 Td (Termostat: 79 EUR) Tj "
        b"0 -20 Td (Kamera: 129 EUR) Tj "
        b"0 -20 Td (Tiskalnik: 249 EUR) Tj "
        b"0 -40 Td (Podatki in cene so izmisljeni.) Tj ET\n"
    )
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"endstream",
        b"<< /Title (Interni cenik 2026) /Author (Maja Kovac) "
        b"/Creator (LibreOffice 7.0) /Producer (LibreOffice 7.0) "
        b"/CreationDate (D:20260914090000+02'00') >>",
    ]
    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R /Info 6 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n".encode()
    )
    return pdf


if __name__ == "__main__":
    base = Path(__file__).resolve().parent / "files"
    for relative in ["www/htdocs/dokumenti/cenik-2026.pdf", "files/javno/cenik-2026.pdf"]:
        destination = base / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(build_pdf())
        print(destination)
