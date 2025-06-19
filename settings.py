import os

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    PROJECT_NAME: str = "Spotlight"
    ROOT_PATH: str = "/spotlight"
    PREFIX: str = "/api/v1"

    DATABASE_URL: str = os.getenv('DATABASE_URL')

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT'))
    REDIS_DB: int = int(os.getenv('REDIS_DB'))
    REDIS_DECODE_RESPONSES: bool = True


@lru_cache
def get_settings():
    return Settings()
