from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

class TextbookContentBase(BaseModel):
    title: str
    body: str
    language: str = "en" # Default to English
    metadata: Optional[Dict[str, Any]] = None # For personalization tags, keywords, etc.

class TextbookContentCreate(TextbookContentBase):
    pass

class TextbookContentUpdate(TextbookContentBase):
    pass

class TextbookContentInDB(TextbookContentBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4) # Auto-generate UUID for ID
    
    class Config:
        from_attributes = True # Allow ORM mode
