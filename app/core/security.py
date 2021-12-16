from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(raw_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def create_access_token(subject:str, expires_delta:timedelta= None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt
