import os
from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    WP_URL: AnyHttpUrl = os.getenv("WP_URL", "http://localhost")
    WP_JWT_USER: str = os.getenv("WP_JWT_USER", "admin")
    WP_JWT_PASSWORD: str = os.getenv("WP_JWT_PASSWORD", "password")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_me")
    JWT_ALGORITHM: str = "HS256"
    TWITTER_BEARER_TOKEN: str | None = os.getenv("TWITTER_BEARER_TOKEN")
    IG_APP_ID: str | None = os.getenv("IG_APP_ID")
    IG_APP_SECRET: str | None = os.getenv("IG_APP_SECRET")
    STRIPE_SECRET_KEY: str | None = os.getenv("STRIPE_SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
