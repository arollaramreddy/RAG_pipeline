"""
embed_retrieve.py  —  Milestone 4: Embedding + Vector Store + Retrieval

Pipeline:
    chunks (from data_ingestion_chunking)
        → all-MiniLM-L6-v2 (sentence-transformers)  [384-dim embeddings]
        → ChromaDB persistent collection             [cosine similarity index]
        → retrieve(query, top_k=5)                   [returns ranked chunks]

Embedding model : all-MiniLM-L6-v2   (planning.md — Retrieval Approach)
Top-k           : 5                   (planning.md — Retrieval Approach)
Vector store    : ChromaDB            (requirements.txt)
"""
from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from data_ingestion_chunking import ingest_and_chunk
# ── Config (mirrors planning.md Retrieval Approach) ───────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "asu_career_services"
CHROMA_PATH     = str(Path(__file__).parent / "chroma_db")
TOP_K           = 5

# ── Load embedding model once at import time ──────────────────────────────────
_model = SentenceTransformer(EMBEDDING_MODEL)


# ── Stage 3: Embed + Store ────────────────────────────────────────────────────
def embed_and_store(
    chunks: list[dict],
    reset: bool = False,
) -> chromadb.Collection:
    """
    Embed `chunks` with all-MiniLM-L6-v2 and upsert into a ChromaDB
    persistent collection.

    Args:
        chunks : list of chunk dicts from ingest_and_chunk()
        reset  : if True, drop and recreate the collection before inserting

    Returns:
        The ChromaDB Collection object (ready for querying).
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Dropped existing collection '{COLLECTION_NAME}'.")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},   # cosine similarity for sentence embeddings
    )

    # Skip embedding if vectors are already stored (idempotent re-runs)
    if collection.count() > 0 and not reset:
        print(
            f"Collection '{COLLECTION_NAME}' already has {collection.count()} vectors. "
            "Skipping embedding. Pass reset=True to rebuild."
        )
        return collection

    print(f"Embedding {len(chunks)} chunks with '{EMBEDDING_MODEL}' …")
    texts = [c["text"] for c in chunks]
    embeddings = _model.encode(texts, show_progress_bar=True, batch_size=32)

    collection.add(
        ids        = [c["chunk_id"]    for c in chunks],
        embeddings = embeddings.tolist(),
        documents  = texts,
        metadatas  = [
            {
                "source":      c["source"],
                "chunk_index": c["chunk_index"],
                "token_count": c["token_count"],
            }
            for c in chunks
        ],
    )

    print(f"Stored {collection.count()} vectors in ChromaDB at '{CHROMA_PATH}'.")
    return collection


# ── Helper: open the persisted collection without re-embedding ────────────────
def get_collection() -> chromadb.Collection:
    """
    Open the existing ChromaDB collection from disk.

    Raises RuntimeError if the collection has not been built yet
    (i.e. embed_and_store / build_index has not been run).
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    if collection.count() == 0:
        raise RuntimeError(
            "ChromaDB collection is empty. "
            "Run embed_and_store() or build_index() first to populate it."
        )
    return collection


# ── Stage 4: Retrieval ────────────────────────────────────────────────────────
def retrieve(
    query: str,
    top_k: int = TOP_K,
    collection: chromadb.Collection | None = None,
) -> list[dict]:
    """
    Embed `query` and return the top-k most relevant chunks from ChromaDB.

    Args:
        query      : natural-language question string
        top_k      : number of results to return (default: 5, from planning.md)
        collection : optional pre-loaded ChromaDB collection; if omitted the
                     persisted collection is opened automatically from disk

    Returns:
        List of result dicts ordered by relevance (most relevant first).
        Each dict contains:
            rank        (int)   : 1-based rank position
            chunk_id    (str)   : e.g. "chunk_14"
            source      (str)   : source file(s), e.g. "discussion_3.txt"
            chunk_index (int)   : position of chunk within the combined stream
            token_count (int)   : number of tokens in the chunk
            distance    (float) : raw cosine distance from ChromaDB
                                  (0.0 = identical, 2.0 = opposite)
            similarity  (float) : cosine similarity = 1 − distance
                                  (1.0 = identical, higher is more relevant)
            text        (str)   : full chunk text
    """
    if collection is None:
        collection = get_collection()

    query_embedding = _model.encode([query]).tolist()

    raw = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    results = []
    for rank, i in enumerate(range(len(raw["ids"][0])), start=1):
        meta     = raw["metadatas"][0][i]
        distance = raw["distances"][0][i]

        results.append({
            "rank":        rank,
            "chunk_id":    raw["ids"][0][i],
            "source":      meta["source"],
            "chunk_index": meta["chunk_index"],
            "token_count": meta["token_count"],
            "distance":    round(distance, 4),
            "similarity":  round(1 - distance, 4),
            "text":        raw["documents"][0][i],
        })

    return results


# ── Convenience: build the full index in one call ─────────────────────────────
def build_index(reset: bool = True) -> chromadb.Collection:
    """
    Run ingestion → chunking → embedding → storage end-to-end.

    Called by main.py so the embedding stage can be triggered with a
    single function call.
    """
    chunks = ingest_and_chunk()
    print(f"Total chunks to embed: {len(chunks)}")
    return embed_and_store(chunks, reset=reset)


# ── Smoke-test when run directly ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print(f"Embedding model : {EMBEDDING_MODEL}")
    print(f"Collection      : {COLLECTION_NAME}")
    print(f"ChromaDB path   : {CHROMA_PATH}")
    print(f"Top-k           : {TOP_K}")
    print("=" * 60 + "\n")

    # Build index from scratch
    build_index(reset=True)

    # Interactive query loop — keep asking until the user types 'exit'
    print("Type your question and press Enter to search.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Query: ").strip()

        if not query:
            continue
        if query.lower() == "exit":
            print("Goodbye!")
            break

        results = retrieve(query)

        print(f"\n{'=' * 60}")
        print(f"Top {len(results)} results for: \"{query}\"")
        print("=" * 60)

        for chunk in results:
            print(
                f"\n  [{chunk['rank']}] "
                f"similarity={chunk['similarity']:.4f}  "
                f"distance={chunk['distance']:.4f}  |  "
                f"{chunk['source']}  |  "
                f"chunk_index={chunk['chunk_index']}  |  "
                f"{chunk['token_count']} tokens"
            )
            print(chunk["text"])

        print()
