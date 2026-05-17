import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
collection = client.get_or_create_collection(name="enterprise_docs")
embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

def retrieve(question: str, top_k=5):
    q_emb = embedder.encode([question]).tolist()[0]
    result = collection.query(query_embeddings=[q_emb], n_results=top_k)

    chunks = []
    ids = result["ids"][0]
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    distances = result.get("distances", [[0]*len(ids)])[0]

    for i in range(len(ids)):
        chunks.append({
            "chunk_id": ids[i],
            "text": docs[i],
            "doc_id": metas[i]["doc_id"],
            "title": metas[i]["title"],
            "source_type": metas[i]["source_type"],
            "allowed_roles": metas[i]["allowed_roles"],
            "ref": metas[i]["ref"],
            "score": float(1 / (1 + distances[i])) if i < len(distances) else 0.8
        })
    return chunks