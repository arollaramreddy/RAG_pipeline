"""
main.py  —  Pipeline entry point

Runs the full ingestion pipeline in order:
    Step 1 : clean_docs              — strip boilerplate from raw discussion files
    Step 2 : data_ingestion_chunking — concatenate + chunk the cleaned files
"""

import clean_docs
from data_ingestion_chunking import ingest_and_chunk, CHUNK_SIZE, CHUNK_OVERLAP


def main() -> None:
    # ── Step 1: Clean raw discussion files ───────────────────────────────────
    print("=" * 60)
    print("STEP 1: Cleaning documents")
    print("=" * 60)
    clean_docs.main()

    # ── Step 2: Ingest and chunk ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 2: Ingestion & Chunking")
    print(f"  Chunk size : {CHUNK_SIZE} tokens")
    print(f"  Overlap    : {CHUNK_OVERLAP} tokens")
    print("=" * 60)

    chunks = ingest_and_chunk()

    print(f"\nTotal chunks: {len(chunks)}\n")

    # ── Print first 5 chunks for inspection ──────────────────────────────────
    print("-" * 60)
    print("FIRST 5 CHUNKS")
    print("-" * 60)
    for chunk in chunks[:5]:
        print(
            f"\n── {chunk['chunk_id']}"
            f"  |  source: {chunk['source']}"
            f"  |  {chunk['token_count']} tokens ──"
        )
        print(chunk["text"])
        print()


if __name__ == "__main__":
    main()
