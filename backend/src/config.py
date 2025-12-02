from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Chatbot API Keys
    OPENAI_API_KEY: str
    QDRANT_HOST: str
    QDRANT_API_KEY: str

    # Database Connection
    NEON_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
