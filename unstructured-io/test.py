#!/usr/bin/env python3
"""
Test script for Unstructured.io local pipeline mode.
Tests partition_text and partition_auto on a sample .txt file.
"""

import sys
import os

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample.txt")

def test_partition_text():
    print("=" * 60)
    print("TEST 1: partition_text")
    print("=" * 60)
    from unstructured.partition.text import partition_text

    elements = partition_text(filename=SAMPLE_FILE)
    print(f"  Total elements found: {len(elements)}\n")
    for i, el in enumerate(elements, 1):
        print(f"  [{i}] Type: {type(el).__name__}")
        print(f"       Text: {el.text[:120]!r}")
    print()
    assert len(elements) > 0, "partition_text returned no elements!"
    return elements

def test_partition_auto():
    print("=" * 60)
    print("TEST 2: partition_auto")
    print("=" * 60)
    from unstructured.partition.auto import partition

    elements = partition(filename=SAMPLE_FILE)
    print(f"  Total elements found: {len(elements)}\n")
    for i, el in enumerate(elements, 1):
        print(f"  [{i}] Type: {type(el).__name__}")
        print(f"       Text: {el.text[:120]!r}")
    print()
    assert len(elements) > 0, "partition_auto returned no elements!"
    return elements

def main():
    print(f"\nUnstructured.io Test Suite")
    print(f"Python: {sys.version}")
    from importlib.metadata import version
    print(f"Unstructured version: {version('unstructured')}")
    print(f"Sample file: {SAMPLE_FILE}\n")

    try:
        elements_text = test_partition_text()
        elements_auto = test_partition_auto()

        # Summarise element type distribution
        from collections import Counter
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        type_counts = Counter(type(el).__name__ for el in elements_auto)
        for etype, count in sorted(type_counts.items()):
            print(f"  {etype}: {count}")

        print("\n✅  SUCCESS — Unstructured.io local pipeline is working correctly.")
    except Exception as exc:
        print(f"\n❌  FAILED: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
