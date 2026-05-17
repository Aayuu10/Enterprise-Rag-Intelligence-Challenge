from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    user_id: str
    role: str
    question: str

class RetrievedChunk(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    source_type: str
    title: str
    score: float
    citation: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[str]
    confidence: float
    retrieved_chunks: List[RetrievedChunk]
    denied: bool = False
    message: Optional[str] = None