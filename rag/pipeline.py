from rag.embeddings import embed_texts
from rag.vector_store import search_vector
from rag.generator import generator_answer
from rag.reranker import rerank


def answer_query(query: str, top_k: int = 3) -> dict:
    query_embedding = embed_texts([query])[0]
    results = search_vector(query_embedding, top_k=top_k)

    chunks = results["documents"][0]
    distances = results["distances"][0]

    if not chunks:
        return {"answer": "I couldn't find anything relevant in your documents.", "sources": []}

    reranked_chunks = rerank(query , chunks , top_k)
    context = "\n".join(reranked_chunks)
    answer = generator_answer(query, context)

    sources = [{"text": c,} for c in reranked_chunks]
    return {"answer": answer, "sources": sources}