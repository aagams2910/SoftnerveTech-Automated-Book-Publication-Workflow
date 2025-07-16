import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import time

chroma_client = chromadb.PersistentClient(path="chromadb_data")
collection = chroma_client.get_or_create_collection("chapter_versions")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def save_version(text: str, metadata: dict):
    """
    Save a version of the chapter with metadata to ChromaDB.
    """
    embedding = embedder.encode([text])[0].tolist()
    doc_id = f"version_{int(time.time() * 1000)}"
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id],
        embeddings=[embedding]
    )
    return doc_id

def semantic_search(query: str, top_k: int = 5):
    """
    Perform semantic search over stored versions using SentenceTransformer embeddings.
    """
    query_embedding = embedder.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return [
        {
            'text': doc,
            'metadata': meta,
            'score': score
        }
        for doc, meta, score in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
    ] 