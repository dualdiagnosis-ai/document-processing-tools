# Unstructured.io — Local Pipeline Setup

## Directory
`/Users/j/APX/unstructured-io/`

## Python
`/opt/homebrew/bin/python3.14` → venv at `./venv/`

## Installation
```bash
source venv/bin/activate
pip install unstructured   # version 0.18.32 installed
```

For PDF support (optional, requires extra deps):
```bash
pip install "unstructured[pdf]"
```

## Test
```bash
./venv/bin/python test.py
```

The test script (`test.py`):
1. Creates no files — uses `sample.txt` (already present)
2. Runs `partition_text` → prints each element's type and text
3. Runs `partition_auto` → same output via auto-detection
4. Prints a SUMMARY of element type counts
5. Exits 0 on success, 1 on failure

## API Key Notes
**No API key is required** for the local pipeline mode.

The `unstructured-client` package is installed as a transitive dependency. It enables the **Unstructured API** (cloud-hosted pipeline) if you want to process documents remotely. To use the API:
- Sign up at https://unstructured.io and obtain an API key
- Set `UNSTRUCTURED_API_KEY=<your_key>` in your environment
- Use `UnstructuredClient` from `unstructured_client` SDK

For all local text, HTML, and basic document processing tasks, **no API key is needed**.

## Notes
- `libmagic` is not installed; `partition_auto` falls back to extension-based detection (works fine for `.txt`).
  Install via `brew install libmagic` for better MIME-type detection.
- PDF partitioning requires `pip install "unstructured[pdf]"` and system libraries (`poppler`, `tesseract` for OCR).
