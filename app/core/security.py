from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(raw_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def create_jwt_token(subject:str, starts_delta:timedelta=None, expires_delta:timedelta=None) -> str:
    start = datetime.utcnow() 
    if starts_delta:
        start += starts_delta

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expire, "nbf": start, "sub": subject}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token:str):
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ACCESS_TOKEN_ALGORITHM]
    )
    return payload