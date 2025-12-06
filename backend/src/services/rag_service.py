from typing import List, Optional

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