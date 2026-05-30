# Marker — PDF → Markdown (local OCR)

**Directory:** `/Users/j/APX/marker`
**Status:** ✅ WORKING — No API key required

## What it does
Marker converts PDFs (and other documents) to clean Markdown using locally-downloaded
Surya OCR models. It handles layout recognition, text extraction, tables, and images
entirely on-device.

## Setup

```bash
# 1. Pre-requisite: libjpeg (needed to build Pillow 10.x from source)
brew install jpeg

# 2. Create venv with Python 3.14
/opt/homebrew/bin/python3.14 -m venv venv
source venv/bin/activate

# 3. Build Pillow 10.4.0 from source (marker-pdf requires Pillow<11)
CFLAGS="-I/opt/homebrew/Cellar/jpeg/10/include" \
LDFLAGS="-L/opt/homebrew/Cellar/jpeg/10/lib" \
pip install "Pillow>=10.1.0,<11.0.0" --no-binary Pillow

# 4. Install marker-pdf and fpdf2
pip install marker-pdf fpdf2
```

## Run the test

```bash
TORCHDYNAMO_DISABLE=1 PYTORCH_ENABLE_MPS_FALLBACK=1 \
  python test.py
```

Models (~1 GB) are downloaded automatically on first run from Hugging Face.

## Notes

- **Python 3.14 workaround:** `torch._dynamo` is incompatible with Python 3.14's
  `inspect` module. Set `TORCHDYNAMO_DISABLE=1` to bypass this. Inference still
  works correctly; only JIT tracing/compilation is disabled.
- **Pillow constraint:** `marker-pdf` requires `Pillow>=10.1.0,<11.0.0`. No
  pre-built wheel exists for Python 3.14, so it must be compiled from source
  using Homebrew's `jpeg` library.
- **API key:** None required. All models run locally.

## Python API (v1.x)

```python
import os
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

from marker.models import create_model_dict
from marker.converters.pdf import PdfConverter
from marker.config.parser import ConfigParser

models = create_model_dict()
config_parser = ConfigParser({"output_format": "markdown"})
converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=models,
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
)
rendered = converter("/path/to/document.pdf")
print(rendered.markdown)
```

## CLI

```bash
TORCHDYNAMO_DISABLE=1 marker_single sample.pdf --output_dir ./output
```

## Packages installed
- marker-pdf 1.10.2
- surya-ocr 0.17.1
- torch 2.12.0
- transformers 4.57.6
- Pillow 10.4.0 (built from source)
- fpdf2 2.8.7
- (see `pip list` for full dependency tree)
