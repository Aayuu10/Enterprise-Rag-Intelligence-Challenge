def route_query(question: str):
    q = question.lower()

    if any(w in q for w in ["employee", "leave", "salary", "hr", "policy"]):
        return {"domain": "HR", "preferred_sources": ["pdf", "csv"]}

    if any(w in q for w in ["budget", "expense", "finance", "invoice", "cost"]):
        return {"domain": "Finance", "preferred_sources": ["csv"]}

    if any(w in q for w in ["security", "incident", "alert", "audit", "log"]):
        return {"domain": "Security", "preferred_sources": ["json", "csv"]}

    return {"domain": "General", "preferred_sources": ["pdf", "csv", "json"]}