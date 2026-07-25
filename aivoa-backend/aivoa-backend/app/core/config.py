from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # Groq
    groq_api_key: str = ""
    groq_extraction_model: str = "gemma2-9b-it"
    groq_reasoning_model: str = "llama-3.3-70b-versatile"

    # Database
    database_url: str

    # App
    max_upload_mb: int = 10
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
