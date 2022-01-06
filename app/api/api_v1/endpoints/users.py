from typing import Any

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models, crud
from app.api import deps

router = APIRouter()

@router.post("/",response_model=schemas.User, status_code=status.HTTP_201_CREATED, responses={400:{"model":schemas.HTTPError}})
async def create_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(deps.get_db)
    ) -> Any:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Already exists an user with this email.",
        )
    user = await crud.user.create(db=db, user_in=user_in)
    return user

@router.get("/me/", response_model=schemas.User, status_code=status.HTTP_200_OK, responses=deps.GET_TOKEN_USER_RESPONSES)
async def get_current_user(
    user:models.User = Depends(deps.get_token_user)
)-> Any:
    return user
