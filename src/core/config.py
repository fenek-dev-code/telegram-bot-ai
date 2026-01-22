from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    BOT_TOKEN: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    # Опциональные с дефолтами
    ADMIN_IDS: List[int] = []
    LOG_LEVEL: str = "info"
    DEBUG: bool = False

    # Настройки вашего проекта
    REFERRAL_PERCENT: float = 5.0
    VIDEO_CONVERSION_PRICE: float = 10.0
    MAX_VIDEO_SIZE_MB: int = 500


# Глобальный объект настроек
config = Settings()
