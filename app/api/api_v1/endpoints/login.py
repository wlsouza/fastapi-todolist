from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings


router = APIRouter()

# TODO: Improve errors messages.
@router.post("/access-token", response_model=schemas.Token, responses={400:{"model":schemas.HTTPError}, 401:{"model":schemas.HTTPError}})
async def login_access_token(db:AsyncSession = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate_user(
        db, user_email=form_data.username, password= form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="testando"
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_jwt_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }