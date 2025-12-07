from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Chatbot API Keys
    OPENAI_API_KEY: str
    QDRANT_HOST: str
    QDRANT_API_KEY: str

    # Database Connection
    NEON_DATABASE_URL: str
    
    # Auth
    SECRET_KEY: str = "your-secret-key-keep-it-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
