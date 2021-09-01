import secrets

from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: PostgresDsn = "postgresql://localhost:5432/todolist_db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()