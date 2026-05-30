# DocStrange

**DocStrange** converts PDF, DOCX, PPTX, XLSX, images and URLs to Markdown, JSON,
CSV or HTML using OCR + layout detection.

- **PyPI**: `docstrange` (v1.1.8 as of setup)
- **GitHub**: https://github.com/NanoNets/docstrange
- **License**: MIT
- **Author**: Nanonets

---

## Directory

```
/Users/j/APX/docstrange/
├── venv/          # Python 3.14 virtual environment
├── sample.docx    # Auto-generated test DOCX
├── sample.pdf     # Auto-generated minimal PDF
├── test.py        # Test script (see below)
└── README.md      # This file
```

---

## Processing Modes

| Mode      | How it works                                  | Requirement                       |
|-----------|-----------------------------------------------|-----------------------------------|
| **Cloud** | Sends file to Nanonets API, returns Markdown  | Free account (10k docs/month)     |
| **Local** | Uses easyocr / python-docx / python-pptx etc. | No network, no API key needed     |

### Cloud API key (optional for higher quota)

The cloud mode has a **free tier** accessible via OAuth login:

```bash
venv/bin/docstrange login          # opens browser OAuth flow
```

Or pass an API key directly (from https://app.nanonets.com/#/keys):

```python
from docstrange import DocumentExtractor
extractor = DocumentExtractor(api_key="YOUR_KEY_HERE")
```

Set the key as an environment variable:

```bash
export NANONETS_API_KEY="YOUR_KEY_HERE"
```

> **Note**: The sandbox account used during setup had its 10k/month free quota
> exhausted. The unauthenticated endpoint also requires a valid API key (returns
> HTTP 401). To use the cloud path, sign up at https://docstrange.nanonets.com/
> and run `docstrange login` (free, no credit card).
>
> **The local extraction path works without any API key** — see `test.py`.

---

## Quick Start

```python
# Local mode — works with no API key or network
from docstrange.processors.docx_processor import DOCXProcessor
processor = DOCXProcessor()
result = processor.process("document.docx")
print(result.extract_markdown())
```

```python
# Cloud mode — requires free Nanonets account
from docstrange import DocumentExtractor
extractor = DocumentExtractor()  # run 'docstrange login' first
result = extractor.extract("document.pdf")
print(result.extract_markdown())
```

---

## Running the test

```bash
cd /Users/j/APX/docstrange
source venv/bin/activate
python test.py
```

**Expected output (local mode)**:
```
[1] Created sample DOCX: .../sample.docx (37192 bytes)
[2] Instantiating DOCXProcessor (local, no cloud API) ...
[3] Processing: .../sample.docx
[4] Extracting Markdown ...
...
SUCCESS — DocStrange DOCX → Markdown (local (DOCXProcessor))
  Characters extracted : 800
```

---

## Supported formats

| Input           | Output formats                   |
|-----------------|----------------------------------|
| PDF             | Markdown, JSON, HTML, CSV        |
| DOCX / DOC      | Markdown, JSON, HTML             |
| PPTX            | Markdown, JSON, HTML             |
| XLSX / XLS      | Markdown, CSV, JSON              |
| PNG / JPG / etc | Markdown, JSON, HTML             |
| URL             | Markdown, JSON, HTML (local only)|
