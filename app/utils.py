import uuid

def make_chunk_id():
    return str(uuid.uuid4())

def make_citation(title, source_type, ref):
    return f"{title} | {source_type} | {ref}"