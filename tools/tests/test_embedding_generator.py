import pytest
from tools.embedding_generator import read_markdown_file, chunk_text, generate_embeddings, upload_embeddings_to_qdrant
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from unittest.mock import patch, MagicMock

def test_read_markdown_file_exists(tmp_path):
    """
    Test that the read_markdown_file function can read an existing Markdown file.
    """
    # Create a dummy Markdown file
    file_content = "# Test Title\nThis is some test content."
    file_path = tmp_path / "test_file.md"
    file_path.write_text(file_content)

    # Call the function to read the file
    content = read_markdown_file(str(file_path))

    # Assert that the content is read correctly
    assert content == file_content

def test_read_markdown_file_non_existent():
    """
    Test that the read_markdown_file function raises FileNotFoundError for a non-existent file.
    """
    with pytest.raises(FileNotFoundError):
        read_markdown_file("non_existent_file.md")

def test_read_markdown_file_empty(tmp_path):
    """
    Test that the read_markdown_file function can read an empty Markdown file.
    """
    file_content = ""
    file_path = tmp_path / "empty_file.md"
    file_path.write_text(file_content)

    content = read_markdown_file(str(file_path))
    assert content == file_content

def test_chunk_text_simple_case():
    """
    Test that chunk_text splits a simple text into chunks correctly.
    """
    text = "This is a long sentence that needs to be chunked into smaller pieces."
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    assert len(chunks) > 1
    assert all(len(chunk) <= 10 for chunk in chunks)
    assert chunks[0] == "This is a "
    assert chunks[1] == "long sente"

def test_chunk_text_with_overlap():
    """
    Test that chunk_text handles chunk overlap correctly.
    """
    text = "abcdefghij"
    chunks = chunk_text(text, chunk_size=5, chunk_overlap=2)
    assert chunks == ["abcde", "defgh", "ghij"] # Corrected expectation


def test_chunk_text_empty_input():
    """
    Test that chunk_text returns an empty list for empty input.
    """
    text = ""
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    assert chunks == []

def test_chunk_text_chunk_size_greater_than_text_length():
    """
    Test that chunk_text returns a single chunk if chunk_size > text length.
    """
    text = "short text"
    chunks = chunk_text(text, chunk_size=20, chunk_overlap=0)
    assert chunks == ["short text"]

@patch('tools.embedding_generator.OpenAI')
def test_generate_embeddings_single_chunk(mock_openai):
    """
    Test that generate_embeddings correctly calls the OpenAI API for a single chunk.
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.embeddings.create.return_value.data = [
        MagicMock(embedding=[0.1, 0.2, 0.3])
    ]

    text_chunks = ["single chunk of text"]
    embeddings = generate_embeddings(text_chunks)

    mock_openai.assert_called_once_with(api_key="mock_api_key") # Assuming api_key is passed or loaded
    mock_client.embeddings.create.assert_called_once_with(
        input=text_chunks,
        model="text-embedding-ada-002"
    )
    assert embeddings == [[0.1, 0.2, 0.3]]

@patch('tools.embedding_generator.OpenAI')
def test_generate_embeddings_multiple_chunks(mock_openai):
    """
    Test that generate_embeddings correctly calls the OpenAI API for multiple chunks.
    """
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.embeddings.create.return_value.data = [
        MagicMock(embedding=[0.1, 0.2, 0.3]),
        MagicMock(embedding=[0.4, 0.5, 0.6])
    ]

    text_chunks = ["first chunk", "second chunk"]
    embeddings = generate_embeddings(text_chunks)

    mock_client.embeddings.create.assert_called_once_with(
        input=text_chunks,
        model="text-embedding-ada-002"
    )
    assert embeddings == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]

@patch('tools.embedding_generator.OpenAI')
def test_generate_embeddings_empty_chunks(mock_openai):
    """
    Test that generate_embeddings returns an empty list for empty input.
    """
    text_chunks = []
    embeddings = generate_embeddings(text_chunks)
    mock_openai.assert_not_called()
    assert embeddings == []

@patch('tools.embedding_generator.QdrantClient')
def test_upload_embeddings_to_qdrant_success(mock_qdrant_client):
    """
    Test that upload_embeddings_to_qdrant successfully uploads points to Qdrant.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance
    mock_client_instance.upsert.return_value = MagicMock(status='completed')

    embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadatas = [{"id": 1, "text": "chunk1"}, {"id": 2, "text": "chunk2"}]
    collection_name = "test_collection"

    upload_embeddings_to_qdrant(embeddings, metadatas, collection_name)

    mock_qdrant_client.assert_called_once_with(url="mock_qdrant_url", api_key="mock_qdrant_api_key")
    mock_client_instance.upsert.assert_called_once_with(
        collection_name=collection_name,
        wait=True, # Added wait=True to expectation
        points=[
            PointStruct(id=0, vector=[0.1, 0.2, 0.3], payload={"id": 1, "text": "chunk1"}), # Corrected ID and payload
            PointStruct(id=1, vector=[0.4, 0.5, 0.6], payload={"id": 2, "text": "chunk2"})  # Corrected ID and payload
        ]
    )

@patch('tools.embedding_generator.QdrantClient')
def test_upload_embeddings_to_qdrant_empty_input(mock_qdrant_client):
    """
    Test that upload_embeddings_to_qdrant handles empty input gracefully.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance

    embeddings = []
    metadatas = []
    collection_name = "test_collection"

    upload_embeddings_to_qdrant(embeddings, metadatas, collection_name)

    mock_qdrant_client.assert_not_called()
    mock_client_instance.upsert.assert_not_called()

@patch('tools.embedding_generator.QdrantClient')
def test_upload_embeddings_to_qdrant_mismatched_lengths(mock_qdrant_client):
    """
    Test that upload_embeddings_to_qdrant raises ValueError for mismatched input lengths.
    """
    embeddings = [[0.1, 0.2, 0.3]]
    metadatas = [{"id": 1, "text": "chunk1"}, {"id": 2, "text": "chunk2"}] # Mismatched

    with pytest.raises(ValueError, match="Embeddings and metadatas lists must have the same length."):
        upload_embeddings_to_qdrant(embeddings, metadatas, "test_collection")

@patch('tools.embedding_generator.QdrantClient')
def test_upload_embeddings_to_qdrant_api_failure(mock_qdrant_client):
    """
    Test that upload_embeddings_to_qdrant handles Qdrant API failures.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance
    mock_client_instance.upsert.side_effect = Exception("Qdrant API Error")

    embeddings = [[0.1, 0.2, 0.3]]
    metadatas = [{"id": 1, "text": "chunk1"}]
    collection_name = "test_collection"

    with pytest.raises(Exception, match="Qdrant API Error"):
        upload_embeddings_to_qdrant(embeddings, metadatas, collection_name)





