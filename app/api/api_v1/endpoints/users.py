from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models, crud
from app.api import deps

router = APIRouter()

@router.post("/",response_model=schemas.User, status_code=status.HTTP_201_CREATED, responses={400:{"model":schemas.Message}})
async def create_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db)
    ) -> Any:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = "Already exists an user with this email.",
        )
    user = await crud.user.create(db=db, user_in=user_in)
    return user

@router.get("/me/", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_current_user(
    user:models.User = Depends(deps.get_token_user)
)-> Any:
    return user