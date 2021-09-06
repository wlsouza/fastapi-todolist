from typing import Union

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: Union[str, PostgresDsn] = 'postgresql://postgres:postgres@localhost:5432/foobar'
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()