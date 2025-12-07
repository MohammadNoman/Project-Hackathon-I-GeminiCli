from qdrant_client import QdrantClient, models
from ..config import settings

def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client.
    """
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        api_key=settings.QDRANT_API_KEY,
    )
    return client

def search_qdrant_collection(
    query_vector: list[float], collection_name: str, limit: int = 5
) -> list[models.ScoredPoint]:
    """
    Searches a Qdrant collection for similar vectors.
    """
    client = get_qdrant_client()
    try:
        search_result = client.query_points(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
        )
        return search_result
    except Exception as e:
        print(f"Error searching Qdrant collection '{collection_name}': {e}")
        raise
