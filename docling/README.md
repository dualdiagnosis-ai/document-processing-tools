# Docling

Open-source document parsing library. Converts HTML, DOCX, PDF, and more to a structured `DoclingDocument`, then exports to Markdown, JSON, or other formats.

## Install

```bash
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install docling
# or restore pinned deps:
pip install -r requirements.txt
```

## Test

```bash
source venv/bin/activate
python test.py
```

The test converts `sample.html` → Markdown and prints element stats.

## Key packages

- `docling 2.96.0`
- `docling-core 2.78.0`
- `torch 2.12.0`, `transformers 5.9.0`

## Notes

- **HTML / DOCX**: lightweight parser, no model download required.
- **PDF**: downloads EasyOCR + layout model weights (~1–2 GB) on first run. Subsequent runs use cached models.
- Fully local — no API key required.
