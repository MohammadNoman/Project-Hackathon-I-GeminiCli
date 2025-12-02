from qdrant_client import QdrantClient
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
