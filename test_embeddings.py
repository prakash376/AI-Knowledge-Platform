from rag.embeddings import embed_texts
from rag.vector_store import add_vectors, search_vector

texts = ["The cat sat on the mat.", "Python is a programming language.", "Dogs are loyal animals."]
ids = ["1", "2", "3"]

embeddings = embed_texts(texts)
add_vectors(ids=ids, embeddings=embeddings,documents=texts)

query = "Tell me about coding"
query_embedding = embed_texts([query])[0]

result = search_vector(query_embedding, top_k=2)
print(result)