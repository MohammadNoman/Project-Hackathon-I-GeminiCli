import pytest
from pydantic import ValidationError
from src.models.chat import ChatRequest, ChatResponse

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