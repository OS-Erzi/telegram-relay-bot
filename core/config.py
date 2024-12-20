from __future__ import annotations
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR = Path(__file__).absolute().parent.parent.parent
BOT_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class BotSettings(EnvBaseSettings):
    TOKEN: str
    OWNER: int
    RATE_LIMIT: int | float = 0.5  # for throttling control

class Settings(BotSettings):
    DEBUG: bool = False


def get_settings() -> Settings:
    return Settings()