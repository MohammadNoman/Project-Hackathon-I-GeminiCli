import pytest
from unittest.mock import MagicMock, patch
from qdrant_client import models
from backend.src.services.qdrant_service import get_qdrant_client, search_qdrant_collection # Keep this line for now, will modify later

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "http://mock-qdrant:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "mock-qdrant-api-key")
    monkeypatch.setenv("OPENAI_API_KEY", "mock-openai-api-key")
    monkeypatch.setenv("NEON_DATABASE_URL", "postgresql://user:password@host:port/database")

@patch('backend.src.services.qdrant_service.QdrantClient')
def test_get_qdrant_client(mock_qdrant_client):
    """
    Test that get_qdrant_client initializes QdrantClient correctly.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance

    # Mock settings.QDRANT_HOST and settings.QDRANT_API_KEY
    with patch('backend.src.services.qdrant_service.settings') as mock_settings:
        mock_settings.QDRANT_HOST = "mock_host"
        mock_settings.QDRANT_API_KEY = "mock_api_key"
        
        client = get_qdrant_client()
        
        mock_qdrant_client.assert_called_once_with(host="mock_host", api_key="mock_api_key")
        assert client == mock_client_instance

@patch('backend.src.services.qdrant_service.QdrantClient')
def test_search_qdrant_collection_success(mock_qdrant_client):
    """
    Test that search_qdrant_collection returns expected results for a successful search.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance
    
    # Mock the search response
    mock_search_result_1 = MagicMock(
        payload={"text": "chunk1", "source": "doc1.md"},
        score=0.9
    )
    mock_search_result_2 = MagicMock(
        payload={"text": "chunk2", "source": "doc2.md"},
        score=0.8
    )
    mock_client_instance.query_points.return_value = [mock_search_result_1, mock_search_result_2]

    # Mock settings for client initialization
    with patch('backend.src.services.qdrant_service.settings') as mock_settings:
        mock_settings.QDRANT_HOST = "mock_host"
        mock_settings.QDRANT_API_KEY = "mock_api_key"
        
        query_vector = [0.1, 0.2, 0.3]
        collection_name = "test_collection"
        limit = 2
        
        results = search_qdrant_collection(query_vector, collection_name, limit)
        
        mock_client_instance.query_points.assert_called_once_with(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
        )
        assert len(results) == 2
        assert results[0].payload == {"text": "chunk1", "source": "doc1.md"}
        assert results[0].score == 0.9
        assert results[1].payload == {"text": "chunk2", "source": "doc2.md"}
        assert results[1].score == 0.8

@patch('backend.src.services.qdrant_service.QdrantClient')
def test_search_qdrant_collection_empty_results(mock_qdrant_client):
    """
    Test that search_qdrant_collection returns an empty list if no results are found.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance
    mock_client_instance.query_points.return_value = []

    with patch('backend.src.services.qdrant_service.settings'): # Mock settings implicitly
        query_vector = [0.1, 0.2, 0.3]
        collection_name = "test_collection"
        limit = 2
        
        results = search_qdrant_collection(query_vector, collection_name, limit)
        
        assert results == []

@patch('backend.src.services.qdrant_service.QdrantClient')
def test_search_qdrant_collection_api_failure(mock_qdrant_client):
    """
    Test that search_qdrant_collection handles Qdrant API failures.
    """
    mock_client_instance = MagicMock()
    mock_qdrant_client.return_value = mock_client_instance
    mock_client_instance.query_points.side_effect = Exception("Qdrant Search Error")

    with patch('backend.src.services.qdrant_service.settings'): # Mock settings implicitly
        query_vector = [0.1, 0.2, 0.3]
        collection_name = "test_collection"
        limit = 2
        
        with pytest.raises(Exception, match="Qdrant Search Error"):
            search_qdrant_collection(query_vector, collection_name, limit)