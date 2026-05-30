#!/usr/bin/env python3
"""
MinerU test script: creates a minimal PDF and extracts structured content.
Uses the `pipeline` backend (CPU-only, no GPU required).
"""
import os
import sys
import subprocess
import json
from pathlib import Path

# ── 1. Create a simple test PDF with reportlab ────────────────────────────────
print("=" * 60)
print("MinerU PDF Extraction Test")
print("=" * 60)

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    print("ERROR: reportlab not installed")
    sys.exit(1)

work_dir = Path(__file__).parent
pdf_path = work_dir / "sample.pdf"
output_dir = work_dir / "output"
output_dir.mkdir(exist_ok=True)

print(f"\n[1] Creating sample PDF: {pdf_path}")
c = canvas.Canvas(str(pdf_path), pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica-Bold", 18)
c.drawString(72, height - 72, "MinerU Test Document")

# Body paragraphs
c.setFont("Helvetica", 12)
c.drawString(72, height - 110, "This is a test document for MinerU PDF extraction.")
c.drawString(72, height - 130, "MinerU is an open-source tool by OpenDataLab that converts")
c.drawString(72, height - 150, "PDF and Office documents into structured Markdown or JSON.")

# Section heading
c.setFont("Helvetica-Bold", 14)
c.drawString(72, height - 190, "Key Features")

# Bullet points
c.setFont("Helvetica", 12)
items = [
    "• Converts PDF → Markdown / JSON",
    "• Supports formulas (LaTeX) and tables (HTML)",
    "• 109-language OCR support",
    "• Runs on CPU (pipeline backend)",
]
y = height - 215
for item in items:
    c.drawString(90, y, item)
    y -= 20

c.save()
print(f"   PDF created: {pdf_path.stat().st_size} bytes")

# ── 2. Run MinerU CLI ─────────────────────────────────────────────────────────
print(f"\n[2] Running MinerU (pipeline backend, txt method)...")
mineru_bin = work_dir / "venv" / "bin" / "mineru"
cmd = [
    str(mineru_bin),
    "-p", str(pdf_path),
    "-o", str(output_dir),
    "-b", "pipeline",
    "-m", "txt",
]
print(f"   Command: {' '.join(cmd)}")

result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
print(f"   Exit code: {result.returncode}")
if result.stdout:
    # Print last 20 lines of stdout
    lines = result.stdout.strip().splitlines()
    for line in lines[-20:]:
        print(f"   [stdout] {line}")
if result.stderr:
    lines = result.stderr.strip().splitlines()
    for line in lines[-20:]:
        print(f"   [stderr] {line}")

if result.returncode != 0:
    print("\nERROR: mineru returned non-zero exit code")
    sys.exit(1)

# ── 3. Find and display output ────────────────────────────────────────────────
print(f"\n[3] Looking for output in {output_dir}...")
md_files = list(output_dir.rglob("*.md"))
json_files = list(output_dir.rglob("*.json"))

print(f"   Found {len(md_files)} markdown file(s), {len(json_files)} JSON file(s)")

if md_files:
    md_file = md_files[0]
    content = md_file.read_text(encoding="utf-8")
    print(f"\n--- Extracted Markdown ({md_file.name}) ---")
    print(content[:1500])  # Print up to 1500 chars
    print("---")

if json_files:
    for jf in json_files:
        if "middle" not in jf.name and "model" not in jf.name:
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                print(f"\n--- JSON output ({jf.name}) ---")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
                print("---")
                break
            except Exception:
                pass

if not md_files and not json_files:
    print("WARNING: No output files found")
    # List what's in the output dir
    for p in output_dir.rglob("*"):
        print(f"   {p}")

# ── 4. Verify success ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
if md_files or json_files:
    print("SUCCESS: MinerU extracted content from PDF")
    print(f"  - Input:  {pdf_path}")
    print(f"  - Output: {output_dir}")
    print(f"  - Files:  {len(md_files)} .md, {len(json_files)} .json")
    print("=" * 60)
else:
    print("PARTIAL: MinerU ran but produced no recognized output files")
    print("=" * 60)
    sys.exit(1)
