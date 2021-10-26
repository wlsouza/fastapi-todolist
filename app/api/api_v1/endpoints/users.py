from app.schemas import user
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()

@router.post("/",response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
    ) -> Any:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Already exists an user with this email.",
        )
    user = await crud.user.create(db=db, user_in=user_in)
    return user