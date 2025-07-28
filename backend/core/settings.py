from pathlib import Path
from functools import lru_cache

# --- kluczowa zmiana: ---
try:
    # Pydantic 2.x
    from pydantic_settings import BaseSettings
except ImportError:          # awaryjnie, gdy ktoś jednak ma Pydantic 1.x
    from pydantic import BaseSettings

from pydantic import Field, AnyUrl

BASE_DIR = Path(__file__).resolve().parent.parent



class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./cmsai.db"
    # JWT settings
    secret_key: str = "CHANGE_ME_SUPER_SECRET"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    # OpenAI API
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    openai_image_size: str = "1024x1024"
    openai_daily_limit: int = 50000  # daily token usage limit (for OpenAI)
    # WordPress API credentials
    wordpress_url: str = ""           # e.g. "https://example.com"
    wordpress_username: str = ""
    wordpress_password: str = ""
    # Scheduler
    article_publish_interval: int = 6  # hours between auto-publish
    # Stripe API
    stripe_api_key: str = ""
    # Twitter (X) API
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_secret: str = ""
    twitter_daily_limit: int = 5
    # Instagram API
    instagram_access_token: str = ""
    instagram_user_id: str = ""        # Business Account ID for Instagram posting
    instagram_daily_limit: int = 5
    admin_email: str = Field("admin@example.com", env="ADMIN_EMAIL")
    admin_password: str = Field("Radek125r!",     env="ADMIN_PASSWORD")

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        env_file_encoding = "utf-8"



# Instantiate settings singleton
settings = Settings()
