from typing import Union
from datetime import datetime, timedelta

import asyncio
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(raw_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def create_access_token(subject:str, expires_delta:timedelta= None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=2880) #TODO: Insert minutes in config file
    payload = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256") #TODO: insert secret in config file 
    return encoded_jwt


# TODO: Think if authenticate_user method should be in CrudUser class 
def authenticate_user(db:AsyncSession, user_id:int , password:str) -> Union[bool,User]:
    user = asyncio.run(crud.user.get_by_id(db, user_id))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user