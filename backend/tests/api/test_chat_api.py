import pytest
from pydantic import ValidationError
from backend.src.models.chat import ChatRequest, ChatResponse
from fastapi.testclient import TestClient
from backend.src.main import app # Import the FastAPI app instance
from unittest.mock import patch, MagicMock

def test_chat_request_valid():
    """Test valid ChatRequest data."""
    request_data = {"query": "Hello", "context_snippet": "Some context", "conversation_id": "123"}
    request = ChatRequest(**request_data)
    assert request.query == "Hello"
    assert request.context_snippet == "Some context"
    assert request.conversation_id == "123"

def test_chat_request_missing_query():
    """Test ChatRequest with missing query."""
    request_data = {"context_snippet": "Some context"}
    with pytest.raises(ValidationError):
        ChatRequest(**request_data)

def test_chat_request_extra_fields():
    """Test ChatRequest with extra fields, ensuring they are ignored."""
    request_data = {"query": "Hello", "extra_field": "ignore_me"}
    request = ChatRequest(**request_data)
    assert request.query == "Hello"
    assert not hasattr(request, "extra_field")

def test_chat_response_valid():
    """Test valid ChatResponse data."""
    response_data = {"response": "Hi there!", "source_chunks": ["chunk1", "chunk2"]}
    response = ChatResponse(**response_data)
    assert response.response == "Hi there!"
    assert response.source_chunks == ["chunk1", "chunk2"]

def test_chat_response_missing_response():
    """Test ChatResponse with missing response."""
    response_data = {"source_chunks": ["chunk1"]}
    with pytest.raises(ValidationError):
        ChatResponse(**response_data)

def test_chat_response_empty_source_chunks():
    """Test ChatResponse with empty source_chunks."""
    response_data = {"response": "Hi there!", "source_chunks": []}
    response = ChatResponse(**response_data)
    assert response.response == "Hi there!"
    assert response.source_chunks == []

# Fixture for the TestClient
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@patch('backend.src.main.get_rag_response')
def test_chat_endpoint_success(mock_get_rag_response, client):
    """
    Test the /chat endpoint for a successful chat interaction.
    """
    mock_get_rag_response.return_value = ("This is a mocked RAG response.", ["relevant chunk 1", "relevant chunk 2"])

    request_payload = {
        "query": "What is robot kinematics?",
        "context_snippet": "Kinematics is the study of motion.",
        "conversation_id": "test-conv-123"
    }

    response = client.post("/chat", json=request_payload)

    assert response.status_code == 200
    response_data = ChatResponse(**response.json())
    assert response_data.response == "This is a mocked RAG response."
    assert response_data.source_chunks == ["relevant chunk 1", "relevant chunk 2"]

    mock_get_rag_response.assert_called_once_with(
        request_payload["query"],
        "textbook_content",
        request_payload["context_snippet"]
    )

@patch('backend.src.main.get_rag_response')
def test_chat_endpoint_missing_query(mock_get_rag_response, client):
    """
    Test the /chat endpoint for missing query in the request payload.
    """
    request_payload = {
        "context_snippet": "Some context"
    }
    response = client.post("/chat", json=request_payload)
    assert response.status_code == 422 # Pydantic validation error

    mock_get_rag_response.assert_not_called()

@patch('backend.src.main.get_rag_response')
def test_chat_endpoint_empty_qdrant_results(mock_get_rag_response, client):
    """
    Test the /chat endpoint when Qdrant search returns no relevant chunks.
    """
    mock_get_rag_response.return_value = ("LLM response without context.", [])

    request_payload = {
        "query": "What is robot kinematics?"
    }

    response = client.post("/chat", json=request_payload)

    assert response.status_code == 200
    response_data = ChatResponse(**response.json())
    assert response_data.response == "LLM response without context."
    assert response_data.source_chunks == []

    mock_get_rag_response.assert_called_once_with(
        request_payload["query"],
        "textbook_content", # Corrected collection name
        None
    )

@patch('backend.src.main.get_rag_response')
def test_chat_endpoint_rag_service_failure(mock_get_rag_response, client):
    """
    Test the /chat endpoint when an internal RAG service (e.g., LLM response) fails.
    """
    mock_get_rag_response.side_effect = Exception("Internal RAG Error") # Simulate failure

    request_payload = {
        "query": "Test query"
    }

    response = client.post("/chat", json=request_payload)

    assert response.status_code == 500 # Internal Server Error
    assert "Internal RAG Error" in response.json()["message"]

    mock_get_rag_response.assert_called_once_with(
        request_payload["query"],
        "textbook_content", # Corrected collection name
        None
    )