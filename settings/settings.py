from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Phidata API"
    environment: str = "development"
    # Add env variables as needed
    openai_api_key: str
    db_url: str = "postgresql+psycopg://ai:ai@localhost:5532/ai"
    redis_url: str
    class Config:
        env_file = ".env"


settings = Settings()
