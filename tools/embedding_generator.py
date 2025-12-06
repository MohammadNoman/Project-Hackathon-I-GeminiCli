import os
from openai import OpenAI
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct

def read_markdown_file(file_path: str) -> str:
    """
    Reads the content of a Markdown file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise

def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """
    Splits text into chunks with a specified size and overlap.
    """
    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    # Ensure chunk_overlap is not greater than chunk_size - 1
    chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))

    chunks = []
    current_index = 0
    while current_index < len(text):
        end_index = current_index + chunk_size
        
        if end_index >= len(text): # If it's the last chunk or remaining text is smaller than chunk_size
            chunks.append(text[current_index:])
            break
        
        chunk = text[current_index:end_index]
        chunks.append(chunk)
        
        current_index += chunk_size - chunk_overlap
        
    return chunks

def generate_embeddings(text_chunks: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a list of text chunks using the OpenAI API.
    """
    if not text_chunks:
        return []

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        # In a real application, you might raise a custom error or log a warning
        # For testing, we allow mock_api_key to be passed.
        openai_api_key = "mock_api_key" # Placeholder for testing without env var

    client = OpenAI(api_key=openai_api_key)
    model = "text-embedding-ada-002"

    try:
        response = client.embeddings.create(input=text_chunks, model=model)
        embeddings = [item.embedding for item in response.data]
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise

def upload_embeddings_to_qdrant(
    embeddings: list[list[float]], metadatas: list[dict], collection_name: str
):
    """
    Uploads generated embeddings and their metadata to Qdrant.
    """
    if len(embeddings) != len(metadatas):
        raise ValueError("Embeddings and metadatas lists must have the same length.")

    if not embeddings:
        return # Nothing to upload

    qdrant_url = os.environ.get("QDRANT_URL", "mock_qdrant_url")
    qdrant_api_key = os.environ.get("QDRANT_API_KEY", "mock_qdrant_api_key")

    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    points = []
    for i, emb in enumerate(embeddings):
        points.append(
            PointStruct(
                id=i,  # Assigning a simple incrementing ID for now.
                vector=emb,
                payload=metadatas[i]
            )
        )

    try:
        # Create collection if it does not exist (assuming a vector size, will need to be dynamic later)
        if not client.collection_exists(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=len(embeddings[0]), distance=models.Distance.COSINE),
            )
            print(f"Collection '{collection_name}' created.")

        operation_info = client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points,
        )
        print(f"Upsert operation status: {operation_info.status}")
    except Exception as e:
        print(f"Error uploading embeddings to Qdrant: {e}")
        raise