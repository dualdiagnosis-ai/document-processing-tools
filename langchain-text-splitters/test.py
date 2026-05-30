"""
Test script for LangChain Text Splitters
Exercises: CharacterTextSplitter, RecursiveCharacterTextSplitter,
           TokenTextSplitter, MarkdownHeaderTextSplitter
"""

from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
)

# ---------------------------------------------------------------------------
# Sample ~500-word paragraph
# ---------------------------------------------------------------------------
SAMPLE_TEXT = (
    "Artificial intelligence has rapidly transformed the way humans interact with technology. "
    "From virtual assistants that understand natural language to recommendation engines that "
    "predict what you want to watch next, AI is embedded in daily life in ways that were "
    "unimaginable just two decades ago. The field draws on mathematics, statistics, computer "
    "science, and cognitive science to build systems capable of learning, reasoning, and "
    "problem-solving.\n\n"
    "Machine learning, a subset of AI, enables computers to improve their performance on tasks "
    "through experience rather than explicit programming. Deep learning, in turn, is a subset "
    "of machine learning that uses neural networks with many layers to model complex patterns "
    "in data. These techniques have driven breakthroughs in image recognition, speech synthesis, "
    "and natural language processing.\n\n"
    "Large language models such as GPT and Claude are trained on vast corpora of text data and "
    "can generate coherent, contextually appropriate text across a wide range of topics. They "
    "power everything from customer-service chatbots to code-completion tools used by millions "
    "of software engineers every day. Despite their impressive capabilities, these models also "
    "have well-documented limitations, including hallucination, bias, and sensitivity to prompt "
    "phrasing.\n\n"
    "The ethical implications of AI are significant and still being actively debated. Questions "
    "around data privacy, algorithmic fairness, job displacement, and the long-term risks of "
    "advanced AI systems occupy researchers, policymakers, and philosophers alike. Responsible "
    "development practices, transparency, and inclusive governance are widely seen as essential "
    "to ensuring that AI benefits humanity as a whole rather than a privileged few.\n\n"
    "Looking ahead, the next frontier likely involves multimodal AI systems that can reason "
    "across text, images, audio, and video simultaneously. Autonomous agents that can plan and "
    "execute multi-step tasks are already emerging from research labs. The pace of progress "
    "shows no signs of slowing, making AI literacy an increasingly important skill for people "
    "in every profession."
)

CHUNK_SIZE = 100
OVERLAP = 20

SEPARATOR = "\n" + "=" * 60 + "\n"


def print_chunks(label, chunks):
    print(f"\n{'=' * 60}")
    print(f"  {label}  ({len(chunks)} chunks)")
    print("=" * 60)
    for i, chunk in enumerate(chunks):
        preview = chunk.replace("\n", " ")[:60]
        print(f"  [{i:02d}] len={len(chunk):4d}  │  {preview!r}")
    print()


# ---------------------------------------------------------------------------
# 1. CharacterTextSplitter
# ---------------------------------------------------------------------------
char_splitter = CharacterTextSplitter(
    separator=" ",
    chunk_size=CHUNK_SIZE,
    chunk_overlap=OVERLAP,
    length_function=len,
)
char_chunks = char_splitter.split_text(SAMPLE_TEXT)
print_chunks("CharacterTextSplitter (separator=' ')", char_chunks)

# ---------------------------------------------------------------------------
# 2. RecursiveCharacterTextSplitter
# ---------------------------------------------------------------------------
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=OVERLAP,
    length_function=len,
)
recursive_chunks = recursive_splitter.split_text(SAMPLE_TEXT)
print_chunks("RecursiveCharacterTextSplitter", recursive_chunks)

# ---------------------------------------------------------------------------
# 3. TokenTextSplitter
# ---------------------------------------------------------------------------
token_splitter = TokenTextSplitter(
    chunk_size=30,   # tokens (smaller unit than chars)
    chunk_overlap=5,
)
token_chunks = token_splitter.split_text(SAMPLE_TEXT)
print_chunks("TokenTextSplitter (chunk_size=30 tokens, overlap=5)", token_chunks)

# ---------------------------------------------------------------------------
# 4. MarkdownHeaderTextSplitter
# ---------------------------------------------------------------------------
MARKDOWN_SAMPLE = """# Introduction

Artificial intelligence is reshaping society in profound ways.

## History

The term *artificial intelligence* was coined in 1956 at the Dartmouth Conference.
Early AI research focused on symbolic reasoning and rule-based systems.

## Modern Techniques

### Deep Learning

Deep learning uses multi-layer neural networks to learn representations from data.
It has achieved state-of-the-art results in vision, speech, and language tasks.

### Transformers

The transformer architecture, introduced in 2017, underpins most large language models.
Self-attention mechanisms allow it to capture long-range dependencies in sequences.

## Ethical Considerations

Bias, fairness, and accountability are central concerns in modern AI deployment.
"""

headers_to_split_on = [
    ("#", "Header1"),
    ("##", "Header2"),
    ("###", "Header3"),
]

md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_chunks = md_splitter.split_text(MARKDOWN_SAMPLE)

print("=" * 60)
print("  MarkdownHeaderTextSplitter")
print("=" * 60)
for i, doc in enumerate(md_chunks):
    preview = doc.page_content.replace("\n", " ")[:60]
    print(f"  [{i:02d}] metadata={doc.metadata}  │  {preview!r}")
print()

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("=" * 60)
print("  SUMMARY")
print("=" * 60)
print(f"  CharacterTextSplitter      : {len(char_chunks):3d} chunks")
print(f"  RecursiveCharacterSplitter : {len(recursive_chunks):3d} chunks")
print(f"  TokenTextSplitter          : {len(token_chunks):3d} chunks")
print(f"  MarkdownHeaderSplitter     : {len(md_chunks):3d} chunks")
print()
print("  ✅  SUCCESS — all four splitters executed without errors.")
print("=" * 60)
