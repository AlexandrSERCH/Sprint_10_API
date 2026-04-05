from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "https://qa-desk.stand.praktikum-services.ru"
    REQUEST_TIMEOUT: int = 20


@lru_cache()
def get_settings() -> Settings:
    """Кэшируем настройки"""
    return Settings()
