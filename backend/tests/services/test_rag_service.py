import pytest
from backend.src.services.rag_service import build_prompt

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
