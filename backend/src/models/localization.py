from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "Urdu"

class TranslateResponse(BaseModel):
    translated_text: str
    original_text: str
    language: str
