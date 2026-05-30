# Document Processing Tools — Setup & Reference

All tools are installed under `/Users/j/APX/`, each in its own directory with an isolated Python 3.14 virtual environment.

**Base requirement:** Python 3.14 via Homebrew — `/opt/homebrew/bin/python3.14`

---

## Quick Status

| # | Tool | Directory | Status | API Key? |
|---|------|-----------|--------|----------|
| 1 | LangChain Text Splitters | `langchain-text-splitters/` | ✅ Working | No |
| 2 | LlamaIndex | `llama-index/` | ✅ Working | No |
| 3 | Unstructured.io | `unstructured-io/` | ✅ Working | No (local mode) |
| 4 | Docling | `docling/` | ✅ Working | No |
| 5 | Marker | `marker/` | ✅ Working | No |
| 6 | MinerU | `mineru/` | ✅ Working | No |
| 7 | DocStrange | `docstrange/` | ✅ Working (local) | Optional (cloud) |
| 8 | Extend Document Toolkit | `extend-document-toolkit/` | 🔑 Needs API key | Yes — extend.ai |
| 9 | Taskade | `taskade/` | 🔑 Needs API key | Yes — taskade.com |

---

## 1. LangChain Text Splitters

**Directory:** `langchain-text-splitters/`
**Package:** `langchain-text-splitters 1.1.2`

### Install
```bash
cd /Users/j/APX/langchain-text-splitters
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install langchain-text-splitters
```

### Test
```bash
source venv/bin/activate
python test.py
```

### Capabilities tested
- `CharacterTextSplitter` — split on character boundaries
- `RecursiveCharacterTextSplitter` — smart recursive splitting
- `TokenTextSplitter` — split by token count (via tiktoken)
- `MarkdownHeaderTextSplitter` — split markdown by heading levels

### Notes
Fully local. No API key or network access required.

---

## 2. LlamaIndex Ingestion & Node Parsers

**Directory:** `llama-index/`
**Package:** `llama-index 0.14.22`, `llama-index-core 0.14.22`

### Install
```bash
cd /Users/j/APX/llama-index
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install llama-index llama-index-core
```

### Test
```bash
source venv/bin/activate
python test.py
```

### Capabilities tested
- `SimpleDirectoryReader` — load documents from a folder
- `IngestionPipeline` + `SentenceSplitter` — split docs into nodes
- Node inspection (text, IDs, metadata)

### Notes
Fully local for ingestion/parsing. LLM-based features (query, summarise) require an OpenAI or other LLM API key — not needed for pure chunking/ingestion.

---

## 3. Unstructured.io (Local Pipeline)

**Directory:** `unstructured-io/`
**Package:** `unstructured 0.18.32`

### Install
```bash
cd /Users/j/APX/unstructured-io
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install unstructured
# For PDF support, also run:
pip install "unstructured[pdf]"
```

### Test
```bash
source venv/bin/activate
python test.py
```

### Capabilities tested
- `partition_text` — partition plain text into typed elements
- `partition_auto` — auto-detect file type and partition
- Element types: `Title`, `NarrativeText`, `ListItem`, `Table`, etc.

### Notes
Local pipeline mode requires no API key. The Unstructured cloud API (`unstructured-client`) is also installed but optional — it requires `UNSTRUCTURED_API_KEY` from unstructured.io. A non-fatal `libmagic` warning may appear on macOS; install with `brew install libmagic` to suppress it.

---

## 4. Docling

**Directory:** `docling/`
**Package:** `docling 2.96.0`, `docling-core 2.78.0`

### Install
```bash
cd /Users/j/APX/docling
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install docling
```

### Test
```bash
source venv/bin/activate
python test.py
```

### Capabilities tested
- `DocumentConverter` — convert HTML/DOCX/PDF to `DoclingDocument`
- Markdown export
- Element inspection (headings, paragraphs, tables, lists)

### Notes
Fully local. HTML and DOCX conversion uses lightweight parsers. **PDF conversion downloads ML model weights on first run** (EasyOCR/layout models, ~1–2 GB) — allow time for the initial download. Subsequent runs use the cached models.

---

## 5. Marker (PDF → Markdown)

**Directory:** `marker/`
**Package:** `marker-pdf 1.10.2`, `surya-ocr 0.17.1`

### Prerequisites (macOS)
```bash
brew install jpeg   # required to build Pillow 10.x from source on Python 3.14
```

### Install
```bash
cd /Users/j/APX/marker
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install marker-pdf fpdf2
```

### Test
```bash
source venv/bin/activate
TORCHDYNAMO_DISABLE=1 python test.py
```

### Python 3.14 workarounds (applied automatically in `test.py`)
| Issue | Fix |
|-------|-----|
| Pillow <11 requires `libjpeg` to build | `brew install jpeg` before pip install |
| `torch._dynamo` crashes on Python 3.14's `inspect` module | Set env var `TORCHDYNAMO_DISABLE=1` |
| `ConfigParser` requires explicit `output_format` | Pass `{"output_format": "markdown"}` |

### Capabilities tested
- Python API: `convert_single_pdf()` → Markdown string
- CLI: `marker_single <pdf>` → Markdown file
- Surya OCR model inference (CPU)

### Notes
Models download on first run (~1–2 GB). Subsequent runs are fast. No API key required.

---

## 6. MinerU (PDF → Structured Chunks)

**Directory:** `mineru/`
**Package:** `mineru 3.2.1`

### Install
```bash
cd /Users/j/APX/mineru
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
# MinerU officially supports Python 3.10–3.13; use --ignore-requires-python on 3.14
pip install --ignore-requires-python "mineru[pipeline]" six
```

### Test
```bash
source venv/bin/activate
python test.py
# or via CLI:
mineru -p sample.pdf -o output/ -b pipeline -m txt
```

### Capabilities tested
- CLI conversion: PDF → Markdown + JSON
- Output formats: `.md` (readable text), `middle.json` (structured), `content_list.json`, `model.json`

### Notes
- `six` must be installed explicitly (not pulled in as a dependency but required at runtime by OCR internals).
- `--ignore-requires-python` is required because MinerU's metadata declares `python<3.14` but works in practice on 3.14.
- CPU-only (`-b pipeline`) mode used; GPU mode available with `cuda` extras.

---

## 7. DocStrange (PDF/Images → Markdown)

**Directory:** `docstrange/`
**Package:** `docstrange 1.1.8`

### Install
```bash
cd /Users/j/APX/docstrange
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install docstrange
```

### Test
```bash
source venv/bin/activate
python test.py
```

### Capabilities tested
- `DOCXProcessor` — local DOCX → Markdown (no login needed)
- Cloud extraction via Nanonets API (optional, see below)

### Cloud mode (optional free tier)
DocStrange's cloud backend is powered by [Nanonets](https://nanonets.com). To enable:
```bash
docstrange login          # opens browser for OAuth sign-in
# or set env var:
export NANONETS_API_KEY=your_key_here
```
Free tier: 10,000 pages/month. Sign up at [docstrange.nanonets.com](https://docstrange.nanonets.com).

---

## 8. Extend Document Toolkit

**Directory:** `extend-document-toolkit/`
**Package:** `extend-ai 1.12.0`

### Install
```bash
cd /Users/j/APX/extend-document-toolkit
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install extend-ai
```

### Test
```bash
source venv/bin/activate
python test.py   # runs in demo/skeleton mode if EXTEND_API_KEY is not set
```

### Live mode (requires API key)
```bash
export EXTEND_API_KEY=your_key_here
python test.py
```

### Available client operations
`parse` · `extract` · `classify` · `split` · `edit` · `*_runs` (async batch) · `workflow_runs` · `webhooks`

### Environments supported
| Env | Description |
|-----|-------------|
| US (default) | `Extend()` |
| US2 / HIPAA | `Extend(environment="US2")` |
| EU1 | `Extend(environment="EU1")` |

Sign up and get an API key at [extend.ai](https://extend.ai). No free tier — requires a subscription.

---

## 9. Taskade (PDF → Notes/Chunks)

**Directory:** `taskade/`
**Packages:** `requests 2.34.2`, `python-dotenv 1.2.2`

> **Note:** There is no official Python SDK for Taskade. The `taskade` package on PyPI is an unrelated DAG executor. This setup uses Taskade's REST API directly.

### Install
```bash
cd /Users/j/APX/taskade
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
```

### Test
```bash
source venv/bin/activate
python test.py   # runs in mock/demo mode if TASKADE_API_KEY is not set
```

### Live mode (requires API key)
```bash
# Option 1: environment variable
export TASKADE_API_KEY=your_personal_access_token

# Option 2: .env file (copy from template)
cp .env.example .env
# edit .env and set TASKADE_API_KEY=...

python test.py
```

### PDF upload workflow
1. Authenticate → `GET /workspaces`
2. List folders → `GET /workspaces/{id}/folders`
3. List agents → `GET /folders/{id}/agents`
4. Upload PDF → `POST /agents/{id}/knowledge/bulk` (multipart)
5. Query agent → `GET /agents/{id}/convos/`

Get a Personal Access Token at [taskade.com](https://taskade.com) (Settings → API). Generous free plan available.

---

## Environment Variables Reference

| Variable | Tool | Where to get it |
|----------|------|-----------------|
| `EXTEND_API_KEY` | Extend Document Toolkit | [extend.ai](https://extend.ai) |
| `TASKADE_API_KEY` | Taskade | [taskade.com](https://taskade.com) → Settings → API |
| `NANONETS_API_KEY` | DocStrange (cloud) | [nanonets.com](https://nanonets.com) or `docstrange login` |
| `UNSTRUCTURED_API_KEY` | Unstructured.io (cloud) | [unstructured.io](https://unstructured.io) (optional) |

---

## Re-running Any Tool

```bash
cd /Users/j/APX/<tool-directory>
source venv/bin/activate
python test.py
```

Each directory contains:
- `venv/` — isolated Python 3.14 virtual environment
- `test.py` — self-contained test script
- `README.md` — tool-specific notes and API docs
- `requirements.txt` — pinned dependencies
