import os

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    PROJECT_NAME: str = "Spotlight"
    ROOT_PATH: str = "/spotlight"
    PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.getenv('DATABASE_URL')


@lru_cache
def get_settings():
    return Settings()
