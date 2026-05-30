# LangChain Text Splitters

Splits documents into chunks using LangChain's text-splitting utilities.

## Install

```bash
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate
pip install langchain-text-splitters
# or restore pinned deps:
pip install -r requirements.txt
```

## Test

```bash
source venv/bin/activate
python test.py
```

## Splitters covered

| Splitter | Description |
|----------|-------------|
| `CharacterTextSplitter` | Split on a fixed character (default: `\n\n`) |
| `RecursiveCharacterTextSplitter` | Recursively tries `\n\n`, `\n`, ` ` until chunk_size is met |
| `TokenTextSplitter` | Split by token count via tiktoken |
| `MarkdownHeaderTextSplitter` | Split by markdown heading level, adding heading metadata |

## Key packages

- `langchain-text-splitters 1.1.2`
- `langchain-core 1.4.0`
- `tiktoken 0.13.0`

## Notes

Fully local — no API key or internet access required.
