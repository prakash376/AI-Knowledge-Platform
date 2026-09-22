import chromadb

_cilent = None
_collection = None

def get_collection():
    global _cilent, _collection
    if _cilent is None:
        _cilent = chromadb.PersistentClient(path="./vector_store")
        _collection = _cilent.get_or_create_collection(name="document")
    return _collection

def add_vectors(ids:list[str], embeddings:list[list[float]], documents:list[str]): 
    collection = get_collection()
    collection.add(ids=ids, embeddings=embeddings, documents=documents)

def search_vector(query_embeddings:list[str], top_k: int = 3):
    collection = get_collection()
    return collection.query(query_embeddings=[query_embeddings], n_results=top_k)
