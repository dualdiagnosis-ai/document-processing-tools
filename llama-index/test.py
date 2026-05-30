"""
LlamaIndex Ingestion Pipeline & Node Parsers Test
- Uses SimpleDirectoryReader to load a local .txt file
- Runs through IngestionPipeline with SentenceSplitter
- 100% local: no API keys or LLM calls required
"""

import os
import sys

print("=" * 60)
print("LlamaIndex Ingestion Pipeline & Node Parsers Test")
print("=" * 60)

# Step 1: Verify sample data exists
sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
sample_file = os.path.join(sample_dir, "sample.txt")

if not os.path.exists(sample_file):
    print(f"ERROR: Sample file not found at {sample_file}")
    sys.exit(1)

print(f"\n[1] Sample file: {sample_file}")
print(f"    Size: {os.path.getsize(sample_file)} bytes")

# Step 2: Load documents with SimpleDirectoryReader
print("\n[2] Loading documents with SimpleDirectoryReader...")
from llama_index.core import SimpleDirectoryReader

reader = SimpleDirectoryReader(input_dir=sample_dir)
documents = reader.load_data()
print(f"    Loaded {len(documents)} document(s)")
for i, doc in enumerate(documents):
    print(f"    Doc {i}: {len(doc.text)} chars, id={doc.doc_id[:16]}...")

# Step 3: Build and run IngestionPipeline with SentenceSplitter
print("\n[3] Running IngestionPipeline with SentenceSplitter...")
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=256, chunk_overlap=20),
    ]
)

nodes = pipeline.run(documents=documents)
print(f"    Produced {len(nodes)} node(s)")

# Step 4: Print first 2 nodes
print("\n[4] First 2 nodes:")
for i, node in enumerate(nodes[:2]):
    text_preview = node.text.strip().replace("\n", " ")
    print(f"\n  --- Node {i+1} ---")
    print(f"  ID:   {node.node_id[:32]}...")
    print(f"  Chars: {len(node.text)}")
    print(f"  Text: {text_preview[:300]}{'...' if len(text_preview) > 300 else ''}")

print("\n" + "=" * 60)
print("SUCCESS: LlamaIndex IngestionPipeline test passed!")
print(f"  Documents loaded : {len(documents)}")
print(f"  Nodes produced   : {len(nodes)}")
print("=" * 60)
