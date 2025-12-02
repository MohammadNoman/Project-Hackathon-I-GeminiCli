from pydantic import BaseModel
from typing import Optional
import uuid

class StudentBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    language_preference: Optional[str] = None

class StudentCreate(StudentBase):
    email: str # Email is mandatory for creation

class StudentUpdate(StudentBase):
    pass # All fields optional for update

class StudentInDB(StudentBase):
    id: uuid.UUID # UUID for ID
    email: str # Email is mandatory in DB
    
    class Config:
        from_attributes = True # Allow ORM mode
