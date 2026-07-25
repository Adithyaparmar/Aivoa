from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq — mandatory tech stack: gemma2-9b-it, llama-3.3-70b-versatile as fallback/context
    groq_api_key: str = ""
    groq_extraction_model: str = "llama-3.3-70b-versatile"
    groq_reasoning_model: str = "llama-3.3-70b-versatile"

    # Postgres (MySQL also fine per assignment; Postgres chosen here)
    database_url: str = "postgresql://postgres:postgres@localhost:5432/aivoa"

    max_upload_mb: int = 10

    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
