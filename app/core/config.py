import secrets
from typing import Union, Optional, Dict, Any
from pathlib import Path

from pydantic import BaseSettings, PostgresDsn, validator
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost"
    API_V1_STR: str = "/api/v1"

    # Auth configs
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2 # 60 min * 24 hrs * 2 days = 2 days

    # DB configs
    SQLALCHEMY_DATABASE_URI: Union[str, PostgresDsn] = "postgresql+asyncpg://postgres:postgres@localhost:5432/FASTAPI_TODOLIST"
    
    # Broker and Celery configs
    BROKER_URI: str = "amqp://guest@localhost:5672//" 

    # Email configs
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    MAIL_TLS: Optional[bool] = None
    MAIL_SSL: Optional[bool] = None
    EMAIL_TEMPLATES_DIR: Union[Path,str] = Path(__file__).parent.parent / "email-templates/build" #Path("/app/app/email-templates/build")
    EMAIL_CONNECTION_CONFIG: Optional[ConnectionConfig] = None 

    @validator("EMAIL_CONNECTION_CONFIG", pre=True)
    def assemble_email_config(cls, v: Optional[ConnectionConfig], values: Dict[str, Any]) -> Any:
        if isinstance(v, ConnectionConfig):
            return v
        return ConnectionConfig(
            MAIL_USERNAME=values.get("MAIL_USERNAME"),
            MAIL_PASSWORD=values.get("MAIL_PASSWORD"),
            MAIL_FROM=values.get("MAIL_FROM"),
            MAIL_PORT=values.get("MAIL_PORT"),
            MAIL_SERVER=values.get("MAIL_SERVER"),
            MAIL_TLS=values.get("MAIL_TLS"),
            MAIL_SSL=values.get("MAIL_SSL"),
            TEMPLATE_FOLDER=values.get("EMAIL_TEMPLATES_DIR"),
        )
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()