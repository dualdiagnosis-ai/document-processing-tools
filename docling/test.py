#!/usr/bin/env python3
"""
Docling test script — converts a sample HTML file to DoclingDocument,
exports Markdown, and reports page/element counts.
"""

import os
import tempfile
from pathlib import Path

# ── 1. Create a small sample HTML file ─────────────────────────────────────
sample_html = """\
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Docling Sample Document</title></head>
<body>
  <h1>Introduction to Docling</h1>
  <p>Docling is an open-source document-parsing library that converts various
  document formats (PDF, DOCX, HTML, …) into a structured
  <code>DoclingDocument</code> representation.</p>

  <h2>Key Features</h2>
  <ul>
    <li>Supports PDF, DOCX, HTML, PPTX, and more</li>
    <li>Exports to Markdown, JSON, and other formats</li>
    <li>Layout-aware: understands headings, tables, lists</li>
    <li>Fully local — no API key required</li>
  </ul>

  <h2>Example Table</h2>
  <table border="1">
    <thead>
      <tr><th>Format</th><th>Supported</th><th>Notes</th></tr>
    </thead>
    <tbody>
      <tr><td>PDF</td><td>Yes</td><td>Layout + OCR</td></tr>
      <tr><td>DOCX</td><td>Yes</td><td>Native parsing</td></tr>
      <tr><td>HTML</td><td>Yes</td><td>DOM-based</td></tr>
      <tr><td>CSV</td><td>Partial</td><td>Via pandas</td></tr>
    </tbody>
  </table>

  <h2>Conclusion</h2>
  <p>Docling makes it easy to build document-intelligence pipelines entirely
  on-premise, without relying on external services.</p>
</body>
</html>
"""

# Write the HTML to a temp file in the same directory
script_dir = Path(__file__).parent
sample_path = script_dir / "sample.html"
sample_path.write_text(sample_html, encoding="utf-8")
print(f"Sample file written to: {sample_path}")

# ── 2. Convert with DocumentConverter ──────────────────────────────────────
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
print("\nConverting document (this may download ML models on first run)…")
result = converter.convert(str(sample_path))

doc = result.document  # DoclingDocument

# ── 3. Export as Markdown ───────────────────────────────────────────────────
md_output = doc.export_to_markdown()
print("\n" + "=" * 60)
print("MARKDOWN OUTPUT")
print("=" * 60)
print(md_output)

# ── 4. Show element/page stats ──────────────────────────────────────────────
print("=" * 60)
print("DOCUMENT STATS")
print("=" * 60)

# Pages
num_pages = len(doc.pages) if hasattr(doc, "pages") and doc.pages else "N/A"
print(f"  Pages detected : {num_pages}")

# Top-level body elements (texts, tables, lists, …)
body_items = list(doc.iterate_items()) if hasattr(doc, "iterate_items") else []
print(f"  Body elements  : {len(body_items)}")

# Count by label/type
from collections import Counter
label_counts: Counter = Counter()
for item, _ in body_items:
    label = getattr(item, "label", None) or type(item).__name__
    label_counts[label] += 1

if label_counts:
    print("  Element types  :")
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        print(f"    {label}: {count}")

print("\n✅  SUCCESS — Docling converted the document end-to-end.")
