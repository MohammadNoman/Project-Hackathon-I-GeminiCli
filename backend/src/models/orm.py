import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..database.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    software_background = Column(String)
    hardware_background = Column(String)
    language_preference = Column(String)
    hashed_password = Column(String)