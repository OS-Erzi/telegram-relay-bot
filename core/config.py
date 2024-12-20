from __future__ import annotations
from typing import ClassVar
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DIR = Path(__file__).absolute().parent.parent.parent
BOT_DIR = Path(__file__).absolute().parent.parent


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class BotSettings(EnvBaseSettings):
    TOKEN: str
    OWNER: int
    RATE_LIMIT: int | float = 0.5

class DBSettings(EnvBaseSettings):
    DB_UPDATE_INTERVAL: int = 60 #seconds
    DBConnect: str
    DBBase: str
    DBUsers: str
    DBBlock: str

class CacheSettings(EnvBaseSettings):
    MAX_WHITELIST_SIZE: int = 10000 # Максимальный размер белого списка
    CACHE_LIFETIME: int = 3600 # Время жизни кэша блокировок (в секундах)

class Settings(BotSettings, DBSettings, CacheSettings):
    bot: ClassVar[type[BotSettings]] = BotSettings
    db: ClassVar[type[BotSettings]] = DBSettings

    DEBUG: bool = False

def get_settings() -> Settings:
    return Settings()