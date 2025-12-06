import pytest
from unittest.mock import patch, MagicMock
from backend.src.services.rag_service import build_prompt, get_llm_response

def test_build_prompt_without_context():
    """
    Test that build_prompt correctly constructs a prompt without context snippets.
    """
    query = "What is robot kinematics?"
    expected_prompt_start = "Based on the provided information, please answer the following question:"
    prompt = build_prompt(query)
    assert prompt.startswith(expected_prompt_start)
    assert query in prompt
    assert "Context:" not in prompt

def test_build_prompt_with_context():
    """
    Test that build_prompt correctly constructs a prompt with context snippets.
    """
    query = "What is inverse kinematics?"
    context_snippets = ["Inverse kinematics is the mathematical process of calculating the variable joint parameters needed to achieve a desired configuration of the kinematic chain.", "Kinematic chains are used in robotics."]
    expected_prompt_start = "Based on the provided information, please answer the following question:"
    expected_context_section_start = "Context:"
    
    prompt = build_prompt(query, context_snippets)
    assert prompt.startswith(expected_prompt_start)
    assert query in prompt
    assert expected_context_section_start in prompt
    assert "Inverse kinematics is the mathematical process" in prompt
    assert "Kinematic chains are used in robotics." in prompt

def test_build_prompt_empty_query():
    """
    Test that build_prompt handles an empty query gracefully.
    """
    query = ""
    with pytest.raises(ValueError, match="Query cannot be empty."):
        build_prompt(query)

def test_build_prompt_long_context_truncation():
    """
    Test that build_prompt truncates long context snippets if necessary.
    (This requires an assumption about max prompt length, which can be refined later)
    """
    query = "Summarize this."
    long_context = "a" * 2000 # Example of a very long context
    
    # We expect some form of truncation or summary, so the full long_context might not be in the prompt
    prompt = build_prompt(query, [long_context])
    assert query in prompt
    assert len(prompt) < (len(long_context) + len(query) + 200) # Expect some reduction in total size

@patch('backend.src.services.rag_service.OpenAI')
def test_get_llm_response_success(mock_openai):
    """
    Test that get_llm_response correctly calls the OpenAI API and returns the response.
    """
    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    mock_client_instance.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="LLM Response"))
    ]

    prompt_text = "Generated prompt for LLM."
    response = get_llm_response(prompt_text)

    mock_openai.assert_called_once_with(api_key="mock_openai_api_key")
    mock_client_instance.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_text}]
    )
    assert response == "LLM Response"

@patch('backend.src.services.rag_service.OpenAI')
def test_get_llm_response_api_failure(mock_openai):
    """
    Test that get_llm_response handles OpenAI API failures.
    """
    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    mock_client_instance.chat.completions.create.side_effect = Exception("OpenAI LLM Error")

    prompt_text = "Generated prompt for LLM."
    with pytest.raises(Exception, match="OpenAI LLM Error"):
        get_llm_response(prompt_text)

@patch('backend.src.services.rag_service.OpenAI')
def test_get_llm_response_no_choices(mock_openai):
    """
    Test that get_llm_response handles cases where no choices are returned.
    """
    mock_client_instance = MagicMock()
    mock_openai.return_value = mock_client_instance
    mock_client_instance.chat.completions.create.return_value.choices = []

    prompt_text = "Generated prompt for LLM."
    response = get_llm_response(prompt_text)
    assert response == "No response from LLM."
