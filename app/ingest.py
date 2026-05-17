import json
import pandas as pd
from app.utils import make_chunk_id

def chunk_text(text, chunk_size=120):
    words = text.split()
    chunks, current = [], []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks

def ingest_txt_file(path, metadata_row):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    records = []

    for i, chunk in enumerate(chunks, start=1):
        records.append({
            "chunk_id": make_chunk_id(),
            "doc_id": metadata_row["doc_id"],
            "title": metadata_row["title"],
            "text": chunk,
            "source_type": metadata_row["source_type"],
            "allowed_roles": metadata_row["allowed_roles"],
            "ref": f"chunk_{i}"
        })
    return records

def ingest_csv_file(path, metadata_row):
    df = pd.read_csv(path)
    records = []

    for i, row in df.iterrows():
        text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        records.append({
            "chunk_id": make_chunk_id(),
            "doc_id": metadata_row["doc_id"],
            "title": metadata_row["title"],
            "text": text,
            "source_type": metadata_row["source_type"],
            "allowed_roles": metadata_row["allowed_roles"],
            "ref": f"row_{i+1}"
        })
    return records

def ingest_json_file(path, metadata_row):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for i, item in enumerate(data, start=1):
        text = " | ".join([f"{k}: {v}" for k, v in item.items()])
        records.append({
            "chunk_id": make_chunk_id(),
            "doc_id": metadata_row["doc_id"],
            "title": metadata_row["title"],
            "text": text,
            "source_type": metadata_row["source_type"],
            "allowed_roles": metadata_row["allowed_roles"],
            "ref": f"log_{i}"
        })
    return records