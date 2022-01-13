from typing import Any, AsyncGenerator, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings
from app.core.security import decode_jwt_token
from app.database.session import async_session

GET_TOKEN_PAYLOAD_RESPONSES = {403: {"model": schemas.HTTPError}}
GET_TOKEN_USER_RESPONSES = GET_TOKEN_PAYLOAD_RESPONSES | {
    403: {"model": schemas.HTTPError},
    404: {"model": schemas.HTTPError},
}
GET_TOKEN_ACTIVE_USER_RESPONSES = GET_TOKEN_USER_RESPONSES | {
    403: {"model": schemas.HTTPError}
}
GET_TOKEN_ACTIVE_SUPERUSER_RESPONSES = GET_TOKEN_ACTIVE_USER_RESPONSES | {
    403: {"model": schemas.HTTPError}
}

# TODO: Make reusable_oauth2 more abstract to use
# in APIv1 and a possible APIv2, APIv3...
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db() -> AsyncGenerator:
    async with async_session() as db:
        yield db


def get_token_payload(token: str = Depends(reusable_oauth2)) -> Dict[str, Any]:
    try:
        payload = decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The token has expired",
        )
    except jwt.ImmatureSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The token is not yet valid.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validade credentials",
        )
    return payload


async def get_token_user(
    db: AsyncSession = Depends(get_db),
    payload: Dict[str, Any] = Depends(get_token_payload),
) -> models.User:
    try:
        token_data = schemas.TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validade credentials",
        )
    user = await crud.user.get_by_id(db, id=int(token_data.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_token_active_user(
    user: models.User = Depends(get_token_user),
) -> models.User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return user


def get_token_active_superuser(
    user: models.User = Depends(get_token_active_user),
) -> models.User:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user
