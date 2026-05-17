import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings
from app.ingest import ingest_txt_file, ingest_csv_file, ingest_json_file

client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
collection = client.get_or_create_collection(name="enterprise_docs")

embedder = SentenceTransformer(settings.EMBEDDING_MODEL)
metadata_df = pd.read_csv("data/metadata/documents.csv")

all_records = []

for _, row in metadata_df.iterrows():
    source_type = row["source_type"]
    location = row["location"]

    if source_type == "pdf":
        all_records.extend(ingest_txt_file(location, row))
    elif source_type == "csv":
        all_records.extend(ingest_csv_file(location, row))
    elif source_type == "json":
        all_records.extend(ingest_json_file(location, row))

texts = [r["text"] for r in all_records]
ids = [r["chunk_id"] for r in all_records]
metadatas = [{
    "doc_id": r["doc_id"],
    "title": r["title"],
    "source_type": r["source_type"],
    "allowed_roles": r["allowed_roles"],
    "ref": r["ref"]
} for r in all_records]

embeddings = embedder.encode(texts).tolist()

collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"Indexed {len(texts)} chunks.")