from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages application settings and environment variables.
    """
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/mydb"
    # Langfuse credentials
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-..."
    LANGFUSE_SECRET_KEY: str = "sk-lf-..."
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    # OpenAI API Key for LLMs
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
