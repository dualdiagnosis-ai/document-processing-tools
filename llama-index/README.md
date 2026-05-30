# LlamaIndex Ingestion Pipeline & Node Parsers

## Overview
Local document ingestion pipeline using LlamaIndex. No API keys required for ingestion/parsing.

## Setup

```bash
# Python 3.14 venv
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install llama-index llama-index-core
```

## Run Test

```bash
venv/bin/python test.py
```

## What the test does
1. Loads `sample_data/sample.txt` via `SimpleDirectoryReader`
2. Runs an `IngestionPipeline` with `SentenceSplitter(chunk_size=256, chunk_overlap=20)`
3. Prints node count and text of first 2 nodes

## API Key Notes
- **No API key required** for ingestion/parsing with local node parsers
- `llama-index-embeddings-openai` and `llama-index-llms-openai` are installed as transitive deps
- If you use OpenAI embeddings or LLM calls, set `OPENAI_API_KEY` in your environment

## Packages
- llama-index 0.14.22
- llama-index-core 0.14.22
- llama-index-workflows 2.20.0
- Python 3.14 (Apple Silicon)
