from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Definition for base settings."""

    app_name: str = "Inventures URL Shortener - Local"
    app_version: str = "1.0.0"
    app_env: str = "development"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Settings loaded for environment: {settings.env_name}")
    return settings
