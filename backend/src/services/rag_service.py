from typing import List, Optional
import os
from openai import OpenAI
from backend.src.services.qdrant_service import search_qdrant_collection
from tools.embedding_generator import generate_embeddings # Assuming tools are importable directly

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

def get_rag_response(query: str, collection_name: str, context_snippet: Optional[str] = None) -> tuple[str, List[str]]:
    """
    Orchestrates the RAG process:
    1. Generates embedding for the query.
    2. Searches Qdrant for relevant context.
    3. Builds a prompt with the query and retrieved context.
    4. Gets a response from the LLM.
    """
    # 1. Generate embedding for the query
    query_embedding = generate_embeddings([query])[0]

    # 2. Search Qdrant for relevant context
    qdrant_results = search_qdrant_collection(query_embedding, collection_name)
    retrieved_context = [point.payload.get("text") for point in qdrant_results if point.payload]

    # Combine provided context_snippet with retrieved_context
    all_context = []
    if context_snippet:
        all_context.append(context_snippet)
    all_context.extend(retrieved_context)
    
    # 3. Build a prompt
    prompt = build_prompt(query, all_context)

    # 4. Get response from LLM
    llm_response = get_llm_response(prompt)
    
    return llm_response, retrieved_context