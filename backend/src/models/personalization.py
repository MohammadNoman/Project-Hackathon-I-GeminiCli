from pydantic import BaseModel

class PersonalizeRequest(BaseModel):
    text: str

class PersonalizeResponse(BaseModel):
    personalized_text: str
    original_text: str
