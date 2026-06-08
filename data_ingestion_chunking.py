"""
data_ingestion_chunking.py  —  Milestone 3: Ingestion & Chunking

Loads every cleaned discussion file from documents/cleanedTextFiles/,
concatenates them in order (discussion_1 → discussion_2 → … → discussion_13),
then applies a single sliding window across the combined stream so chunks
can span document boundaries — e.g. the last 20 tokens of discussion_1
plus the first 230 tokens of discussion_2 form one chunk.

Chunking parameters (from planning.md):
    Chunk size : 300 tokens
    Overlap    :  50 tokens

Token counting uses the same WordPiece tokenizer as the downstream
all-MiniLM-L6-v2 embedding model, so chunk boundaries are exact.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

from transformers import AutoTokenizer, logging as hf_logging

# Suppress the "sequence longer than model max length" warning — we only
# use the tokenizer for splitting, never for model inference.
hf_logging.set_verbosity_error()

# ── Paths & hyper-parameters (mirrors planning.md Chunking Strategy) ─────────
CLEANED_DIR    = Path(__file__).parent / "documents" / "cleanedTextFiles"
CHUNK_SIZE     = 200   # tokens per chunk
CHUNK_OVERLAP  = 30    # tokens shared between consecutive chunks
TOKENIZER_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ── Tokenizer (loaded once at import time) ────────────────────────────────────
_tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
_tokenizer.model_max_length = int(1e9)   # suppress length warnings


def _tokenize(text: str) -> tuple[list[int], list[tuple[int, int]]]:
    """
    Return (token_ids, char_offsets) for `text`.

    char_offsets[i] = (char_start, char_end) lets us slice the *original*
    string instead of decoding token IDs (which adds WordPiece spacing
    artifacts like "it ' s").
    """
    enc = _tokenizer(
        text,
        add_special_tokens=False,
        return_offsets_mapping=True,
    )
    return enc["input_ids"], enc["offset_mapping"]


def _natural_key(path: Path) -> int:
    """Sort discussion files numerically: discussion_1 < discussion_2 … < discussion_13."""
    match = re.search(r"(\d+)", path.stem)
    return int(match.group(1)) if match else 0


# ── Stage 1: Ingestion ────────────────────────────────────────────────────────
def load_documents(directory: Path = CLEANED_DIR) -> list[dict]:
    """
    Read every .txt file in `directory` in natural numeric order.

    Returns a list of dicts:
        source (str) : filename, e.g. "discussion_1.txt"
        text   (str) : full file content, whitespace-stripped
    """
    docs: list[dict] = []
    for path in sorted(directory.glob("*.txt"), key=_natural_key):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            docs.append({"source": path.name, "text": text})
    if not docs:
        raise FileNotFoundError(
            f"No .txt files found in {directory}. "
            "Run clean_docs.py first to generate the cleaned files."
        )
    return docs


# ── Stage 2: Chunking ─────────────────────────────────────────────────────────
def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> Generator[tuple[str, int, int, int], None, None]:
    """
    Slide a fixed-token window over `text`.

    Uses char offset mapping so each chunk is sliced directly from the
    original string — no WordPiece decode artifacts.

    Yields:
        (chunk_string, token_count, char_start, char_end)
    """
    if overlap >= chunk_size:
        raise ValueError(
            f"overlap ({overlap}) must be smaller than chunk_size ({chunk_size})"
        )

    token_ids, offsets = _tokenize(text)
    total_tokens = len(token_ids)
    step = chunk_size - overlap
    start = 0

    while start < total_tokens:
        end = min(start + chunk_size, total_tokens)
        char_start = offsets[start][0]
        char_end   = offsets[end - 1][1]
        yield text[char_start:char_end].strip(), end - start, char_start, char_end
        if end == total_tokens:
            break
        start += step


# ── Combined pipeline ─────────────────────────────────────────────────────────
def ingest_and_chunk(
    directory: Path = CLEANED_DIR,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """
    Concatenate all documents in order, then chunk the combined stream.

    Chunks can span document boundaries (e.g. the tail of discussion_1
    and the head of discussion_2 can share a chunk), matching the example
    in the project spec.

    Each returned dict contains:
        chunk_id    (str)       : "chunk_0", "chunk_1", …
        source      (str)       : document(s) contributing to this chunk,
                                  e.g. "discussion_1.txt" or
                                  "discussion_1.txt + discussion_2.txt"
        chunk_index (int)       : global position of this chunk
        text        (str)       : chunk content (exact original characters)
        token_count (int)       : exact token count
    """
    documents = load_documents(directory)

    # Build one combined string and record each document's char span
    combined   = ""
    doc_spans: list[tuple[str, int, int]] = []   # (source, char_start, char_end)

    for doc in documents:
        if combined:
            combined += "\n\n"
        char_start = len(combined)
        combined  += doc["text"]
        char_end   = len(combined)
        doc_spans.append((doc["source"], char_start, char_end))

    # Slide the window over the full combined text
    chunks: list[dict] = []
    for idx, (chunk_str, token_count, chunk_start, chunk_end) in enumerate(
        chunk_text(combined, chunk_size, overlap)
    ):
        # Find every document whose char range overlaps this chunk's char range
        sources = [
            src
            for src, doc_start, doc_end in doc_spans
            if chunk_end > doc_start and chunk_start < doc_end
        ]
        chunks.append({
            "chunk_id":    f"chunk_{idx}",
            "source":      " + ".join(sources),
            "chunk_index": idx,
            "text":        chunk_str,
            "token_count": token_count,
        })

    return chunks


# ── Quick smoke-test when run directly ───────────────────────────────────────
if __name__ == "__main__":
    print(f"Tokenizer : {TOKENIZER_NAME}")
    print(f"Chunk size: {CHUNK_SIZE} tokens  |  Overlap: {CHUNK_OVERLAP} tokens")
    print(f"Source dir: {CLEANED_DIR}\n")

    chunks = ingest_and_chunk()

    print(f"Total chunks: {len(chunks)}\n")

    # Print first 5 chunks for inspection
    print("=" * 60)
    print("FIRST 5 CHUNKS")
    print("=" * 60)
    for chunk in chunks[:5]:
        print(f"\n── {chunk['chunk_id']}  |  source: {chunk['source']}  |  {chunk['token_count']} tokens ──")
        print(chunk["text"])
        print()
