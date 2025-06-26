import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chromadb_data")

def semantic_search(query: str, collection_name: str = "products", top_k: int = 5) -> List[Dict]:
    """
    Search ChromaDB for products relevant to the query.
    Args:
        query: User's search query.
        collection_name: Name of the ChromaDB collection.
        top_k: Number of results to return.
    Returns:
        List of product metadata dicts.
    """
    collection = client.get_collection(collection_name)
    embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    # Each result contains ids, documents, metadatas
    return results["metadatas"][0] if results["metadatas"] else [] 