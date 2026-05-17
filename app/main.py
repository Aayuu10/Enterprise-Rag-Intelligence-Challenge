from fastapi import FastAPI
from app.schemas import QueryRequest, QueryResponse, RetrievedChunk
from app.db import init_db
from app.retriever import retrieve
from app.permissions import filter_authorized_chunks
from app.generator import generate_answer

app = FastAPI(title="Enterprise RAG Free")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query_system(req: QueryRequest):
    retrieved = retrieve(req.question, top_k=6)
    allowed = filter_authorized_chunks(req.role, retrieved)

    if not allowed:
        return QueryResponse(
            answer="Access denied or no relevant authorized information found.",
            citations=[],
            confidence=0.0,
            retrieved_chunks=[],
            denied=True,
            message="You are not authorized to access the relevant records."
        )

    answer = generate_answer(req.question, allowed)

    citations = [f"{c['title']} ({c['ref']})" for c in allowed]
    confidence = round(sum(c["score"] for c in allowed) / len(allowed), 2)

    return QueryResponse(
        answer=answer,
        citations=citations,
        confidence=confidence,
        retrieved_chunks=[
            RetrievedChunk(
                chunk_id=c["chunk_id"],
                doc_id=c["doc_id"],
                text=c["text"],
                source_type=c["source_type"],
                title=c["title"],
                score=c["score"],
                citation=f"{c['title']} ({c['ref']})"
            ) for c in allowed
        ]
    )