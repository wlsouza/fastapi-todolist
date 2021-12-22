from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models, crud
from app.core.config import settings
from app.database.session import async_session

default_auth_responses = {403:{"model":schemas.HTTPError},404:{"model":schemas.HTTPError}}

#TODO: Make reusable_oauth2 more abstract to use in APIv1 and a possible APIv2, APIv3...
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

async def get_db() -> AsyncGenerator:
    async with async_session() as db:
        yield db


#TODO: Try document error on OPENAPI
async def get_token_user(
    db: AsyncSession = Depends(get_db), token:str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ACCESS_TOKEN_ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validade credentials"
        )
    user = await crud.user.get_by_id(db, id=int(token_data.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user