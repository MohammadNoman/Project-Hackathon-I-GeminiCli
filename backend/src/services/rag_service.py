from typing import List, Optional
import os
from openai import OpenAI

def build_prompt(query: str, context_snippets: Optional[List[str]] = None) -> str:
    """
    Constructs a prompt for the language model based on the user's query and optional context snippets.
    """
    if not query:
        raise ValueError("Query cannot be empty.")

    prompt_parts = ["Based on the provided information, please answer the following question:"]

    if context_snippets:
        prompt_parts.append("\nContext:")
        # Simple truncation for demonstration; real implementation might use token counting
        for snippet in context_snippets:
            # Assume a max context length if needed, truncate here
            # For now, just add snippets
            prompt_parts.append(f"- {snippet}")

    prompt_parts.append(f"\nQuestion: {query}")
    prompt_parts.append("\nAnswer:")

    return "\n".join(prompt_parts)

def get_llm_response(prompt_text: str) -> str:
    """
    Calls the OpenAI API to get a response from the language model.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        # For testing, we allow mock_api_key to be passed.
        openai_api_key = "mock_openai_api_key" # Placeholder for testing without env var
    
    client = OpenAI(api_key=openai_api_key)
    model = "gpt-3.5-turbo"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_text}]
        )
        if response.choices:
            return response.choices[0].message.content
        return "No response from LLM."
    except Exception as e:
        print(f"Error getting LLM response: {e}")
        raise