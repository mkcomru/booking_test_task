from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///./bookings.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )

    environment: str = "dev"
    debug: bool = True

    database: DatabaseSettings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
