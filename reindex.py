import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ingestion.loaders import load_document
from ingestion.chunker import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import add_vectors

text = load_document("sample_lecture.txt")
chunks = chunk_text(text, chunk_size=500, chunk_overlap=50)

embeddings = embed_texts(chunks)
ids = [f"lecture_chunk_{i}" for i in range(len(chunks))]

add_vectors(ids=ids, embeddings=embeddings, documents=chunks)
print(f"Indexed {len(chunks)} chunks from sample_lecture.txt")