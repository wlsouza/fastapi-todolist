import secrets
from typing import Union

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2 # 60 min * 24 hrs * 2 days = 2 days
    SQLALCHEMY_DATABASE_URI: Union[str, PostgresDsn] = 'postgresql+asyncpg://postgres:postgres@localhost:5432/FASTAPI_TODOLIST"'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()