# Extend Document Toolkit

AI-powered document processing using the [Extend](https://extend.ai) API.

## What it does

Extend provides cloud-based document intelligence:

- **Parse** — Convert PDFs, images, and Office docs into structured, LLM-ready markdown chunks
- **Extract** — Pull structured JSON data from documents using a schema/extractor you define
- **Classify** — Automatically categorize documents using a classifier you define
- **Split** — Separate multi-document files into individual components
- **Edit** — Detect and fill PDF form fields programmatically
- **Workflows** — Chain the above steps into reusable pipelines

## ⚠️ Requires EXTEND_API_KEY — sign up at [extend.ai](https://extend.ai)

There is **no free tier or local mode**. All API calls require a valid API key.

1. Create an account at https://extend.ai
2. Go to **Developer Settings** in the dashboard
3. Copy your API key
4. Set it in your environment:
   ```bash
   export EXTEND_API_KEY="your_api_key_here"
   ```

## Setup

```bash
# Create venv (Python 3.14)
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run the test

```bash
# Skeleton demo (no API key needed — shows code patterns)
python test.py

# Live API call (requires API key)
EXTEND_API_KEY=your_key_here python test.py
```

## Quick start (after obtaining an API key)

```python
import os
from extend_ai import Extend

client = Extend(token=os.environ["EXTEND_API_KEY"])

# Parse any document
result = client.parse(file={"url": "https://example.com/invoice.pdf"})
for chunk in result.output.chunks:
    print(chunk.content)

# Extract structured data (requires an Extractor ID from the dashboard)
result = client.extract(
    file={"url": "https://example.com/invoice.pdf"},
    extractor={"id": "ex_YOUR_EXTRACTOR_ID"},
)
print(result.output)
```

## SDK reference

- PyPI: https://pypi.org/project/extend-ai/
- GitHub: https://github.com/extend-hq/extend-python-sdk
- Docs: https://docs.extend.ai

## Installed packages

| Package     | Version |
|-------------|---------|
| extend-ai   | 1.12.0  |
| httpx       | 0.28.1  |
| pydantic    | 2.13.4  |
