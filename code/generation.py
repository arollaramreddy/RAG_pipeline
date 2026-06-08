"""
generation.py  —  Milestone 5: Grounded Answer Generation

Pipeline:
    user query
        → retrieve()           [top-k chunks from ChromaDB]
        → build context prompt [numbered blocks with source labels]
        → Groq LLM             [llama-3.3-70b-versatile]
        → grounded answer      [with source citations]

The LLM is instructed to answer ONLY from the retrieved context.
If the context does not contain enough information to answer, it says so
rather than drawing on its general training knowledge.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from embed_retrieve import retrieve, TOP_K

# Load GROQ_API_KEY from .env (if present)
load_dotenv(Path(__file__).parent.parent / ".env")

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"

# Only pass chunks whose cosine similarity meets this bar.
# Chunks below this score are too loosely related to be useful and are dropped
# before the LLM ever sees them, preventing off-topic answers.
SIMILARITY_THRESHOLD = 0.45

SYSTEM_PROMPT = """\
You are a precise assistant for ASU (Arizona State University) career services and career development.

Answer the user's question using ONLY the context passages provided below.
Do not use any knowledge from your training data that is not reflected in the context.

The context passages contain real student and user discussions. Each passage includes
the name of the person who wrote it (a Reddit username or a Quora profile name)
appearing on its own line just before their comment.

Rules:
- Answer ONLY the specific question asked. Do not include tangentially related information.
- Always attribute statements to the specific person who said them.
  Use phrasing like: "Clint Potts said ...", "According to Siri Gowtham, ...",
  "u/FindTheOthers623 noted that ...", or "As u/Ok-Cost-5079 put it, ...".
- Every claim in your answer must be tied to a named person from the context.
- Do not merge or paraphrase multiple people's views without naming each one.
- If the context only partially answers the question, share what named people said and note the gap.
- If the context does not contain enough information to answer the specific question, reply with exactly:
  "The provided context does not contain enough information to answer this question."
- Do not invent names, quotes, or facts not present in the context.
- Do NOT add a "Sources:" section — that will be appended automatically.
"""


# ── Core function ─────────────────────────────────────────────────────────────
def generate(query: str, top_k: int = TOP_K) -> dict:
    """
    Retrieve relevant chunks for `query` and generate a grounded answer via Groq.

    Args:
        query  : natural-language question from the user
        top_k  : number of chunks to retrieve (default mirrors embed_retrieve.TOP_K)

    Returns:
        dict with keys:
            answer   (str)       : LLM-generated answer grounded in the retrieved context
            sources  (list[str]) : unique source files used in the retrieved chunks
            chunks   (list[dict]): raw retrieve() results for inspection
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Set it in your .env file or as an environment variable."
        )

    # Step 1 — retrieve, then drop chunks below the similarity threshold
    all_chunks = retrieve(query, top_k=top_k)
    chunks = [c for c in all_chunks if c["similarity"] >= SIMILARITY_THRESHOLD]

    if not chunks:
        msg = "The provided context does not contain enough information to answer this question."
        return {"answer": msg, "sources": [], "chunks": all_chunks}

    # Step 2 — build context block (only from high-relevance chunks)
    context_lines = []
    for chunk in chunks:
        context_lines.append(
            f"[{chunk['source']} | similarity: {chunk['similarity']:.4f}]\n{chunk['text']}"
        )
    context_text = "\n\n---\n\n".join(context_lines)

    user_message = f"Context:\n\n{context_text}\n\nQuestion: {query}"

    # Step 3 — call Groq
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.2,   # low temperature → factual, grounded output
    )

    answer = response.choices[0].message.content.strip()

    # Collect unique source files in retrieval-rank order
    sources = list(dict.fromkeys(
        s for chunk in chunks for s in chunk["source"].split(" + ")
    ))

    # Only append the sources block when the LLM produced a real answer.
    # If it replied with the no-information message, sources are irrelevant.
    NO_INFO = "The provided context does not contain enough information to answer this question."
    if NO_INFO in answer:
        return {"answer": answer, "sources": [], "chunks": chunks}

    answer_with_sources = answer + "\n\nSources: " + ", ".join(sources)
    return {"answer": answer_with_sources, "sources": sources, "chunks": chunks}


# ── Interactive loop ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("ASU Career Services RAG — Generation (Milestone 5)")
    print(f"Model  : {GROQ_MODEL}")
    print(f"Top-k  : {TOP_K}")
    print("=" * 60)
    print("Type your question and press Enter.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Query: ").strip()

        if not query:
            continue
        if query.lower() == "exit":
            print("Goodbye!")
            break

        result = generate(query)

        print(f"\n{'=' * 60}")
        print("ANSWER")
        print("=" * 60)
        print(result["answer"])

        print(f"\n{'─' * 60}")
        print("RETRIEVED CHUNKS")
        print("─" * 60)
        for chunk in result["chunks"]:
            print(
                f"\n  [{chunk['rank']}] similarity={chunk['similarity']:.4f}  "
                f"distance={chunk['distance']:.4f}  |  {chunk['source']}  |  "
                f"{chunk['token_count']} tokens"
            )
            print(chunk["text"])

        print()
