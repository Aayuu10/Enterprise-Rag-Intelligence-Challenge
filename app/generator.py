import requests
from app.config import settings
from app.prompts import SYSTEM_PROMPT, build_prompt

def generate_answer(question: str, chunks: list):
    prompt = build_prompt(question, chunks)
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(settings.OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["response"]