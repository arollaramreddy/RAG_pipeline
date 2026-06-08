# ASU Career Services RAG Pipeline

A Retrieval-Augmented Generation (RAG) system that answers questions about **ASU career services and career development** using real student discussions from Reddit r/ASU and Quora.

Instead of relying on an LLM's general training knowledge, the system retrieves the most relevant passages from actual student conversations and generates answers grounded exclusively in that content — citing the specific people who said each thing.

GitHub: [https://github.com/arollaramreddy/RAG_pipeline](https://github.com/arollaramreddy/RAG_pipeline)

---

## What it covers

- ASU career fairs — are they worth attending?
- ASU Career Services — what do students think?
- Handshake — how useful is it for finding internships and jobs?
- On-campus jobs — how to get one, how competitive is it?
- Internship strategies — what actually works for ASU students?

---

## Project structure

```
RAG_pipeline/
├── app.py                        # Gradio web UI (run this to use the system)
├── main.py                       # Pipeline setup: clean → chunk → embed
├── code/
│   ├── clean_docs.py             # Strips boilerplate from raw discussion files
│   ├── data_ingestion_chunking.py# Tokenizes and chunks the cleaned text
│   ├── embed_retrieve.py         # Embeds chunks and stores them in ChromaDB
│   └── generation.py             # Retrieves context and generates answers via Groq
├── documents/
│   ├── textFiles/                # Raw Reddit and Quora discussion files
│   └── cleanedTextFiles/         # Cleaned versions (produced by main.py)
├── chroma_db/                    # Vector store (produced by main.py)
├── .env                          # Your API keys (not committed)
├── .env.example                  # Template for .env
├── planning.md                   # Project spec and architecture notes
└── requirements.txt              # Python dependencies
```

---

## Pipeline stages

```
Raw discussions
      ↓  clean_docs.py          — remove ads, vote buttons, nav boilerplate
Cleaned text
      ↓  data_ingestion_chunking.py  — sliding-window token chunks (200 tokens, 30 overlap)
Chunks
      ↓  embed_retrieve.py      — all-MiniLM-L6-v2 embeddings → ChromaDB (cosine similarity)
Vector index
      ↓  generation.py          — top-k retrieval → Groq LLM (llama-3.3-70b-versatile)
Grounded answer
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/arollaramreddy/RAG_pipeline.git
cd RAG_pipeline
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

Then open `.env` and set:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [https://console.groq.com](https://console.groq.com).

---

## How to run

### Step 1 — Build the index (run once)

```bash
python main.py
```

This cleans all 16 discussion files, chunks them into token-sized passages, embeds them with `all-MiniLM-L6-v2`, and saves the vector index to `chroma_db/`. You only need to run this again if you add new source documents.

### Step 2 — Launch the web UI (run any time)

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860) in your browser, type a question, and get a grounded answer with source attribution.

---

## Example questions

- What do students say about the usefulness of ASU career fairs?
- What do students think about ASU Career Services?
- Is Handshake useful for finding internships and jobs?
- What advice do students give for finding on-campus jobs?
- What strategies do students recommend for improving internship opportunities?

---

## Tech stack

| Component | Tool |
|-----------|------|
| Embedding model | `all-MiniLM-L6-v2` (sentence-transformers) |
| Vector store | ChromaDB (cosine similarity) |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Web UI | Gradio |
| Tokenizer | WordPiece via HuggingFace Transformers |
