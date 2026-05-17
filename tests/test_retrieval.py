from app.retriever import retrieve

def test_retrieve():
    results = retrieve("What is the leave policy?", top_k=3)
    assert len(results) > 0