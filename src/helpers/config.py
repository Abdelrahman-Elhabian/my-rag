from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "mini-RAG"
    APP_VERSION: str = "0.1"
    OPENAI_API_KEY: str = ""

    FILE_ALLOWED_TYPES: list = ["text/plain", "application/pdf"]
    FILE_MAX_SIZE: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 512000

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
