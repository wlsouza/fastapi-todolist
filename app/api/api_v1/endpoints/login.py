from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings


router = APIRouter()

TODO: Improve errors messages.
@router.post("/access-token", response_model=schemas.Token, responses={400:{"model":schemas.Message}, 401:{"model":schemas.Message}})
async def login_access_token(db:Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate_user(
        db, user_email=form_data.username, password= form_data.password
    )
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            content="Incorrect email or password"
        )
    elif not user.is_active:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }