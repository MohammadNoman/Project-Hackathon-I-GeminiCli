from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here to ensure they are registered with the Base
from backend.src.models import orm