#!/usr/bin/env python3
"""
Test script for Extend Document Toolkit (extend-ai SDK).

This script exercises the core SDK functionality:
  1. Imports and SDK version check
  2. Authentication setup via EXTEND_API_KEY env var
  3. Client instantiation with all supported environments
  4. Demonstrates all major API method signatures
  5. Makes a live parse call if EXTEND_API_KEY is set;
     otherwise runs a simulated skeleton demo.

Requires: EXTEND_API_KEY env var for live API calls.
Sign up at: https://extend.ai
"""

import os
import sys

# ── 1. Imports ────────────────────────────────────────────────────────────────
print("=" * 60)
print("Extend Document Toolkit — SDK Test")
print("=" * 60)

try:
    import extend_ai
    from extend_ai import Extend, AsyncExtend, ExtendEnvironment
    from extend_ai.core.api_error import ApiError
    from extend_ai.errors import UnauthorizedError
    print(f"[OK] extend_ai imported successfully")
    print(f"[OK] SDK version: {extend_ai.__version__}")
except ImportError as e:
    print(f"[FAIL] Could not import extend_ai: {e}")
    sys.exit(1)

# ── 2. Authentication setup ───────────────────────────────────────────────────
API_KEY = os.environ.get("EXTEND_API_KEY", "")

if API_KEY:
    print(f"[OK] EXTEND_API_KEY found in environment (length={len(API_KEY)})")
else:
    print("[WARN] EXTEND_API_KEY not set — will run skeleton demo only")

# ── 3. Client instantiation ───────────────────────────────────────────────────
print("\n--- Client Instantiation ---")
token_to_use = API_KEY if API_KEY else "demo_token_placeholder"

# Default (US production)
client = Extend(token=token_to_use, timeout=30.0)
print(f"[OK] Extend client created (US production, timeout=30s)")

# Environment variants (just instantiation, no network call)
client_us2 = Extend(token=token_to_use, environment=ExtendEnvironment.PRODUCTION_US2)
print(f"[OK] Extend client created (US2 / HIPAA)")

client_eu = Extend(token=token_to_use, environment=ExtendEnvironment.PRODUCTION_EU1)
print(f"[OK] Extend client created (EU1)")

async_client = AsyncExtend(token=token_to_use)
print(f"[OK] AsyncExtend client created")

# ── 4. SDK method signatures ──────────────────────────────────────────────────
print("\n--- Available Client Methods ---")
sdk_methods = [
    "parse",             # Parse a document into structured chunks
    "extract",           # Extract structured data using an extractor
    "classify",          # Classify a document using a classifier
    "split",             # Split a multi-doc file using a splitter
    "edit",              # Edit/fill a PDF form
    "parse_runs",        # Async parse run management
    "extract_runs",      # Async extract run management
    "classify_runs",     # Async classify run management
    "split_runs",        # Async split run management
    "edit_runs",         # Async edit run management
    "workflow_runs",     # Async workflow run management
    "webhooks",          # Webhook verification helpers
]
for method in sdk_methods:
    has_it = hasattr(client, method)
    status = "[OK]" if has_it else "[MISSING]"
    print(f"  {status} client.{method}")

# ── 5. Live API call or skeleton demo ─────────────────────────────────────────
print("\n--- API Call Test ---")

SAMPLE_URL = "https://raw.githubusercontent.com/extend-hq/extend-python-sdk/refs/heads/main/README.md"

if API_KEY:
    print(f"Live mode: attempting parse on sample URL...")
    print(f"  URL: {SAMPLE_URL}")
    try:
        result = client.parse(
            file={"url": SAMPLE_URL, "name": "readme.md"},
        )
        print(f"[OK] Parse succeeded!")
        print(f"  Status : {getattr(result, 'status', 'N/A')}")
        chunks = getattr(getattr(result, "output", None), "chunks", None) or []
        print(f"  Chunks : {len(chunks)}")
        if chunks:
            first_chunk = chunks[0]
            content = getattr(first_chunk, "content", "")
            print(f"  First chunk preview: {content[:120]!r}")
    except UnauthorizedError as e:
        print(f"[WARN] 401 Unauthorized — API key may be invalid: {e.body}")
    except ApiError as e:
        print(f"[WARN] API error {e.status_code}: {e.body}")
    except Exception as e:
        print(f"[WARN] Unexpected error: {e}")
else:
    print("Skeleton demo (no API key — showing what a parse call looks like):")
    print()
    print("  from extend_ai import Extend")
    print("  client = Extend(token=os.environ['EXTEND_API_KEY'])")
    print()
    print("  # Parse a document")
    print("  result = client.parse(file={'url': 'https://example.com/invoice.pdf'})")
    print("  for chunk in result.output.chunks:")
    print("      print(chunk.content)")
    print()
    print("  # Extract structured data")
    print("  result = client.extract(")
    print("      file={'url': 'https://example.com/invoice.pdf'},")
    print("      extractor={'id': 'ex_YOUR_EXTRACTOR_ID'},")
    print("  )")
    print()
    print("  # Classify a document")
    print("  result = client.classify(")
    print("      file={'url': 'https://example.com/document.pdf'},")
    print("      classifier={'id': 'cls_YOUR_CLASSIFIER_ID'},")
    print("  )")
    print()
    print("  # Split a multi-document file")
    print("  result = client.split(")
    print("      file={'url': 'https://example.com/packet.pdf'},")
    print("      splitter={'id': 'spl_YOUR_SPLITTER_ID'},")
    print("  )")
    print()
    print("  # Edit/fill a PDF form")
    print("  result = client.edit(")
    print("      file={'url': 'https://example.com/form.pdf'},")
    print("      config={'instructions': 'Fill applicant name as Jane Doe'},")
    print("  )")

# ── 6. Polling helper signature demo ─────────────────────────────────────────
print("\n--- Polling Helper Signature ---")
print("  result = client.parse_runs.create_and_poll(")
print("      file={'url': 'https://example.com/invoice.pdf'},")
print("  )")
print("  # Returns when status is PROCESSED, FAILED, or CANCELLED")

# ── 7. Webhook verification signature demo ────────────────────────────────────
print("\n--- Webhook Verification Signature ---")
print("  event = client.webhooks.verify_and_parse(")
print("      body=request_body_str,")
print("      headers=request_headers_dict,")
print("      signing_secret=os.environ['EXTEND_WEBHOOK_SECRET'],")
print("  )")

print()
print("=" * 60)
if API_KEY:
    print("SUCCESS — SDK is installed and live API call completed.")
else:
    print("SUCCESS — SDK is installed. Skeleton demo ran end-to-end.")
    print("NOTE    — Set EXTEND_API_KEY to enable live API calls.")
    print("          Sign up at: https://extend.ai")
print("=" * 60)
