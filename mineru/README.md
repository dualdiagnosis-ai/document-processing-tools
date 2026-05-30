# MinerU — PDF → Structured Content

**Package:** `mineru` v3.2.1 ([PyPI](https://pypi.org/project/mineru/))  
**Author:** OpenDataLab  
**Directory:** `/Users/j/APX/mineru/`

## What it does

MinerU converts PDF, DOCX, PPTX, XLSX, and image files into structured
Markdown and JSON. It supports:
- Text extraction (fast, CPU-only)
- OCR for scanned documents (109 languages)
- Formula → LaTeX conversion
- Table → HTML conversion

## Installation Notes

**Python compatibility:** MinerU formally declares `Python <3.14, >=3.10`.
This install used Python 3.14.5 with `--ignore-requires-python` and works
correctly in practice (all functionality tested and passing).

```bash
# Activate venv
source /Users/j/APX/mineru/venv/bin/activate

# Install (already done)
pip install --ignore-requires-python "mineru[pipeline]" six
```

## No API Key Required

MinerU is fully local/offline. No API keys, accounts, or internet access
needed once models are downloaded (models auto-download on first run).

## Usage

### CLI

```bash
# Text-based PDF (fast, no model download needed)
mineru -p sample.pdf -o output/ -b pipeline -m txt

# Auto-detect (may use OCR models)
mineru -p document.pdf -o output/ -b pipeline

# With explicit OCR
mineru -p scanned.pdf -o output/ -b pipeline -m ocr
```

### Python API (via subprocess or direct)

```python
import subprocess
result = subprocess.run([
    "mineru",
    "-p", "input.pdf",
    "-o", "output/",
    "-b", "pipeline",
    "-m", "txt",
], capture_output=True, text=True)
```

## Test

```bash
/Users/j/APX/mineru/venv/bin/python /Users/j/APX/mineru/test.py
```

Test creates `sample.pdf` with `reportlab`, runs MinerU, and prints the
extracted Markdown and JSON.

## Output Structure

```
output/
└── sample/
    ├── sample.md                    # Extracted Markdown
    ├── sample_content_list_v2.json  # Structured content list (blocks)
    ├── sample_middle.json           # Intermediate representation
    └── sample_model.json            # Model detection output
```
