# Document-Agnostic RAG System

A modular Retrieval-Augmented Generation (RAG) system that ingests multiple document formats, builds a vector index, and answers questions grounded strictly in provided documents with citations.

---

## 🚀 Overview

This project implements a production-style RAG pipeline with a strong focus on **document ingestion quality**, **modular architecture**, and **evaluation-driven development**.

It supports mixed-format document ingestion, robust parsing, chunking, embedding, retrieval, and answer generation with citations.

---

## ✨ Features

### 📄 Multi-format ingestion
Supports:
- PDF
- DOCX
- PPTX
- XLSX 

---

### 🧠 RAG Pipeline
- Document parsing → normalization
- Chunking with overlap strategy
- Embedding generation (SentenceTransformers)
- Vector storage (ChromaDB)
- Top-K retrieval
- LLM-based grounded answer generation
- Citation-backed responses

---

### 🧩 Architecture Highlights
- Clean separation of concerns
- Swappable components:
  - Embedders
  - Vector stores
  - LLM providers
- Factory-based parser registry
- Service-layer design (`IngestionService`, `QueryService`)
- Startup-time dependency container
---

### 📊 Evaluation framework
- Recall@K for retrieval quality
- Citation correctness tracking
- Sample QA dataset included

---

## 🏗️ System Architecture

File Upload
↓
MIME Detection
↓
Parser Registry (PDF / DOCX / PPTX / XLSX)
↓
Normalized Document (text + metadata)
↓
Chunking Layer
↓
Embedding Layer (SentenceTransformers)
↓
Vector Store (ChromaDB)
↓
Retriever (Top-K)
↓
LLM Generator
↓
Answer + Citations


---

## 🧱 Tech Stack

- **Backend:** FastAPI
- **Vector DB:** ChromaDB
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Parsing:**
  - PyMuPDF (PDF)
  - python-docx (DOCX)
  - python-pptx (PPTX)
  - openpyxl (XLSX)

- **LLM (optional):**
  - OpenAI-compatible API (pluggable)

---

## 📥 Ingestion Flow

1. Upload file(s)
2. Detect MIME type
3. Validate file (unsupported / corrupted / encrypted)
4. Select parser via registry
5. Extract structured text
6. Normalize into internal schema
7. Chunk text with overlap
8. Generate embeddings
9. Store in vector database

---

## 🔎 Query Flow

1. User submits question
2. Question is embedded
3. Vector similarity search (Top-K retrieval)
4. Context assembly from chunks
5. LLM generates grounded response
6. Citations returned with answer

---

## 📡 API Endpoints

### Ingest Documents

```http
POST /ingest
Upload one or multiple documents for indexing.

POST /query

REQUEST:

{
  "question": "What was the Q3 revenue growth?"
}

RESPONSE:

{
  "answer": "Revenue grew by 18% in Q3.",
  "citations": [
    {
      "source": "financial_report.pdf",
      "page": 12
    }
  ]
}
```

## ⚙️ Setup Instructions

1. Install dependencies
pip install -r requirements.txt

2. Run server
uvicorn app.main:app --reload

## .env

CHROMA_PATH=./chroma_db

# Optional (if using LLM backend)
OPENAI_API_KEY=your_key_here
BASE_URL=your_base_url_here

## ⚠️ Security Considerations
Documents treated as untrusted input
Prompt injection attempts inside documents are ignored
Only retrieved context is passed to the LLM
No execution of document instructions