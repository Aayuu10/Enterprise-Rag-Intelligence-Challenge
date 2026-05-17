# Enterprise-Rag-Intelligence-Challenge

A free, local-first implementation of a secure **Enterprise RAG** system built for the **Enterprise RAG Intelligence Challenge**. This project is designed to answer natural-language questions across multi-format enterprise data while enforcing strict role-based access control (RBAC), producing grounded responses, and showing citations with retrieval traceability.

## Overview

This project simulates a large enterprise environment where information is spread across disconnected systems such as policy documents, CSV datasets, incident records, and JSON logs. The system retrieves relevant context from these sources, filters results according to user roles, and generates answers using only authorized evidence.

The implementation is designed to satisfy the main challenge goals:
- Intelligent retrieval across multiple source types
- Secure access control with strict RBAC filtering
- Accurate answer generation from retrieved context
- Explainability through citations and retrieved evidence
- Minimal hallucination by grounding every answer in source chunks
- Fully free stack using local models and open-source tools

## Features

- Multi-format ingestion for TXT/PDF-like documents, CSV files, and JSON logs
- Semantic retrieval using `sentence-transformers`
- Local vector storage with `ChromaDB`
- RBAC enforcement before answer generation
- Local LLM inference with `Ollama`
- FastAPI backend for query handling
- Streamlit frontend for interactive demo
- SQLite metadata store for users and document permissions
- Synthetic enterprise dataset for safe demonstration
- Evidence panel with chunk-level citations and confidence score

## Tech Stack

| Layer | Tool |
|------|------|
| Backend API | FastAPI |
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Metadata Store | SQLite |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| LLM | Ollama (`phi3:mini` or `llama3.1:8b`) |
| Data Processing | Pandas |
| Testing | Pytest |

## Project Structure

```bash
submission/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── db.py
│   ├── auth.py
│   ├── permissions.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── router.py
│   ├── generator.py
│   ├── prompts.py
│   └── utils.py
│
├── data/
│   ├── pdfs/
│   ├── csv/
│   ├── json/
│   ├── metadata/
│   └── permissions/
│
├── indexes/
├── scripts/
│   ├── create_synthetic_data.py
│   ├── build_index.py
│   └── seed_sqlite.py
│
├── ui/
│   └── streamlit_app.py
│
├── tests/
│   ├── test_rbac.py
│   ├── test_retrieval.py
│   └── test_api.py
│
├── requirements.txt
├── .env
└── README.md
```

## Architecture

The system follows a retrieval-augmented generation pipeline with access control built into the retrieval flow.

### Flow

1. A user submits a question from the Streamlit UI.
2. The FastAPI backend receives the query along with the user's role.
3. The retriever converts the query into embeddings and searches ChromaDB.
4. Retrieved chunks are filtered using RBAC rules.
5. Only authorized chunks are passed to the local LLM.
6. The LLM generates a grounded answer with citations.
7. The UI displays the answer, confidence, citations, and evidence.

### Security Design

RBAC is enforced **before** generation. Unauthorized chunks are never sent to the model. This reduces the risk of accidental data leakage and supports the challenge requirement for restricted document access and safe handling of sensitive queries.

## Dataset

The project uses a synthetic enterprise dataset created locally. It includes:

- HR policy documents
- Employee records
- Finance reports
- Incident registers
- Security logs
- Metadata files describing source type, sensitivity, and allowed roles
- User-role mappings for HR, Finance, Security, and Manager roles

This dataset is intentionally synthetic so the project can be shared and tested without using real company data.

## Roles and Access

Example role permissions used in the project:

| Role | Can Access |
|------|------------|
| HR | HR policies, employee records |
| Finance | Finance reports |
| Security | Security logs, incident records |
| Manager | High-level policies, summaries, selected reports |

The permission model is stored in metadata and applied during retrieval filtering.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aayuu10/Enterprise-Rag-Intelligence-Challenge.git
cd Enterprise-Rag-Intelligence-Challenge
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / macOS
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Ollama Setup

This project uses Ollama for free local inference.

### Install Ollama
Download and install Ollama from:

[https://ollama.com](https://ollama.com)

### Pull a model

For low-end laptops:
```bash
ollama pull phi3:mini
```

For better answer quality on stronger systems:
```bash
ollama pull llama3.1:8b
```

### Test the model

```bash
ollama run phi3:mini
```

## Environment Variables

Create a `.env` file in the project root:

```env
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_DIR=./indexes/chroma
SQLITE_PATH=./indexes/app.db
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=phi3:mini
```

## Running the Project

Run the following commands in order.

### 1. Generate synthetic enterprise data

```bash
python scripts/create_synthetic_data.py
```

### 2. Seed SQLite with users and document metadata

```bash
python scripts/seed_sqlite.py
```

### 3. Build the vector index

```bash
python scripts/build_index.py
```

### 4. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

### 5. Start the Streamlit frontend

Open a new terminal and run:

```bash
streamlit run ui/streamlit_app.py
```

## Example Queries

Use these queries to test the system:

- What is the company leave policy?
- Show recent security incidents.
- Summarize Q2 finance records.
- Who can access employee salary details?
- What critical security events were logged?

Also test unauthorized scenarios, for example:
- Ask a Finance user to access HR salary information
- Ask an HR user to view security logs

The expected behavior is either a safe denial or a response limited to authorized evidence.

## API Endpoints

### Health Check
```http
GET /health
```

### Query Endpoint
```http
POST /query
```

Sample request body:

```json
{
  "user_id": "u_mgr_1",
  "role": "Manager",
  "question": "Summarize recent incidents and related policies"
}
```

## Testing

Run tests with:

```bash
pytest
```

Included tests:
- RBAC access validation
- Retrieval result validation
- API health endpoint test

## Why This Project Meets the Challenge

This implementation directly targets the core challenge requirements:

- **Intelligent Retrieval**: semantic retrieval over multi-format enterprise data
- **Cross-Source Context**: supports policy docs, CSV records, and JSON logs
- **Query-Aware Routing**: queries can be routed by domain intent
- **Secure Access Control**: strict RBAC filtering before generation
- **Accurate Answer Generation**: answers are grounded in retrieved chunks
- **Source Attribution**: citations and evidence are returned to the UI
- **Minimal Hallucinations**: prompts force the model to answer only from context
- **Explainability**: retrieved chunks and confidence are shown to the user

## Limitations

- Local models are slower than cloud APIs on weaker laptops
- `phi3:mini` is lightweight but less capable than larger models
- Current document pipeline uses plain text for policy documents; this can be extended to full PDF parsing
- Retrieval is semantic-first; hybrid search can be added later for stronger exact-match performance

## Future Improvements

- Add BM25 + semantic hybrid retrieval
- Add reranking for better chunk selection
- Add full PDF parsing and page-level citations
- Add audit logging for denied queries
- Add JWT-based authentication
- Add role-aware dashboard analytics
- Add evaluation notebook for retrieval and groundedness metrics

## Demo Output

The final demo should show:
- Role selection
- Natural language querying
- Retrieved evidence chunks
- Confidence score
- Source citations
- Proper access denial for restricted queries

## Author

Built by **Aayush Koli** as part of the **Enterprise RAG Intelligence Challenge**.
