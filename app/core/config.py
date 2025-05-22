from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:1@localhost:5432/logparse"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()