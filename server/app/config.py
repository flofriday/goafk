from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "goafk"
    telegram_bot_token: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
