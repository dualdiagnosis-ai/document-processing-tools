#!/usr/bin/env python3
"""
Test script for marker-pdf: PDF -> Markdown conversion
marker-pdf v1.x API
"""
import os
import sys

# Disable torch dynamo (required for Python 3.14 compatibility)
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# ── Step 1: Create a sample PDF ──────────────────────────────────────────────
print("Step 1: Creating sample PDF with fpdf2...")
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=16)
pdf.cell(0, 10, "Marker PDF Test Document", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(5)
pdf.set_font("Helvetica", size=12)
pdf.cell(0, 8, "Introduction", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(
    0, 6,
    "This is a test PDF created to verify that Marker can convert PDFs to Markdown. "
    "Marker uses Surya OCR models to extract text, tables, and other content. "
    "This sentence contains simple Latin text to exercise the OCR pipeline.",
)
pdf.ln(4)
pdf.set_font("Helvetica", size=12)
pdf.cell(0, 8, "Key Features", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
for item in [
    "- Converts PDFs to clean Markdown",
    "- Handles OCR via Surya models",
    "- Preserves document structure",
    "- Open-source and runs locally",
]:
    pdf.cell(0, 6, item, new_x="LMARGIN", new_y="NEXT")

sample_pdf = "/Users/j/APX/marker/sample.pdf"
pdf.output(sample_pdf)
print(f"  Created: {sample_pdf}")

# ── Step 2: Load models ───────────────────────────────────────────────────────
print("\nStep 2: Loading Marker models (downloading on first run — may take a while)...")
from marker.models import create_model_dict

models = create_model_dict()
print("  Models loaded OK")

# ── Step 3: Convert PDF ───────────────────────────────────────────────────────
print("\nStep 3: Converting PDF to Markdown...")
from marker.converters.pdf import PdfConverter
from marker.config.parser import ConfigParser

config_parser = ConfigParser({"output_format": "markdown"})
converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=models,
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
)

rendered = converter(sample_pdf)
markdown_text = rendered.markdown

# ── Step 4: Report result ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUCCESS — First 500 chars of Markdown output:")
print("=" * 60)
print(markdown_text[:500])
print("=" * 60)
print(f"\nTotal markdown length: {len(markdown_text)} characters")
