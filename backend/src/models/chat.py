from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    query: str
    context_snippet: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    source_chunks: List[str]