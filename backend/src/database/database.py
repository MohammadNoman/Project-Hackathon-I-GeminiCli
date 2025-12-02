from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings
from .base import Base # Import Base from base.py

# Create the SQLAlchemy engine
# Use settings.NEON_DATABASE_URL to connect to your Neon Postgres database
engine = create_engine(settings.NEON_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
