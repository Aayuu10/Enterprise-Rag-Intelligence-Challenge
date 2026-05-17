SYSTEM_PROMPT = """
You are a secure enterprise RAG assistant.
Answer only from the retrieved context.
Do not use outside knowledge.
Do not guess.
If the answer is not supported, say:
'I do not have enough authorized information to answer that.'
Always include source citations in square brackets like [1], [2].
Never reveal unauthorized data.
"""

def build_prompt(question: str, chunks: list):
    context_parts = []
    for i, c in enumerate(chunks, start=1):
        context_parts.append(
            f"[{i}] Title: {c['title']}\n"
            f"Source Type: {c['source_type']}\n"
            f"Reference: {c['ref']}\n"
            f"Content: {c['text']}\n"
        )
    context = "\n".join(context_parts)

    return f"""
Question:
{question}

Retrieved Context:
{context}

Instructions:
- Answer only from the retrieved context.
- Use inline citations like [1], [2].
- If evidence is weak or missing, say so.
"""