from ingestion.loaders import load_document
from ingestion.chunker import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import add_vectors, search_vector

text = load_document("uploads/3d899bcb-8302-4fee-af45-82a0fb1450e9_python_program.pdf")
chunks = chunk_text(text)
print("Number of chunks:", len(chunks))

chunk_ids = [f"doc1_chunk{i}" for i in range (len(chunks))]

embedding = embed_texts(chunks)
add_vectors(ids=chunk_ids, embeddings=embedding, documents=chunks)
print("Chunks stored in vector database.")

query = "what is this document about?"
query_embedding = embed_texts([query])[0] 
result = search_vector(query_embedding , top_k = 2)

print("\n Top matching chunks for your question:")

for doc in result["documents"][0]:
    print("-", doc[:150], "...")