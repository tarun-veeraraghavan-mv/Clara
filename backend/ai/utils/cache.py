from langchain_core.documents import Document
from .vector_store import vectorstore
import string

def _normalize_query(query: str) -> str:
    """Converts to lowercase and removes punctuation."""
    return query.lower().translate(str.maketrans('', '', string.punctuation))

def get_cached_response(query: str, threshold: float = 0.7):
    """
    Searches the vector store for a similar query and returns the cached response if the similarity score is above the threshold.
    """
    normalized_query = _normalize_query(query)
    similar_docs = vectorstore.similarity_search_with_score(
        normalized_query, 
        k=3, 
        filter={"cache": "true"}
    )
    for doc, score in similar_docs:
        if score >= threshold:
            return doc.metadata.get("response")
    return None

def add_to_cache(query: str, response: str):
    """
    Adds a new query-response pair to the cache.
    """
    normalized_query = _normalize_query(query)
    document = Document(
        page_content=normalized_query, 
        metadata={
            "response": response, 
            "cache": "true",
            "original_query": query
        }
    )
    vectorstore.add_documents([document])
