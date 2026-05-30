"""
Helper: create a minimal valid PDF for testing.
No external PDF library required — pure Python bytes.
"""
import struct

def create_minimal_pdf(path: str, text: str = "Hello DocStrange World!\n\nThis is a test document.\nIt contains:\n- Some text\n- A list\n- A sample title\n\nDocStrange converts this to clean Markdown."):
    """Write a minimal but valid PDF-1.4 with one page of text."""
    lines = text.split("\n")

    # Build content stream (BT ... ET block per line)
    ops = ["BT", "/F1 12 Tf", "72 720 Td", "14 TL"]
    for line in lines:
        # Escape parentheses and backslash for PDF string literals
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        ops.append(f"({safe}) Tj")
        ops.append("T*")
    ops.append("ET")
    content = "\n".join(ops).encode()

    offsets = []
    body = b"%PDF-1.4\n"

    # obj 1 - Catalog
    offsets.append(len(body))
    body += b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"

    # obj 2 - Pages
    offsets.append(len(body))
    body += b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"

    # obj 3 - Page
    offsets.append(len(body))
    body += (
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R\n"
        b"   /MediaBox [0 0 612 792]\n"
        b"   /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>\n"
        b"   /Contents 4 0 R >>\n"
        b"endobj\n"
    )

    # obj 4 - Content stream
    offsets.append(len(body))
    stream_len = len(content)
    body += f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode()
    body += content
    body += b"\nendstream\nendobj\n"

    # xref table
    xref_offset = len(body)
    n_objs = len(offsets) + 1
    xref = f"xref\n0 {n_objs}\n"
    xref += "0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n"
    body += xref.encode()

    # trailer
    body += (
        f"trailer\n<< /Size {n_objs} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode()

    with open(path, "wb") as f:
        f.write(body)

    print(f"Created sample PDF: {path} ({len(body)} bytes)")

if __name__ == "__main__":
    create_minimal_pdf("sample.pdf")
