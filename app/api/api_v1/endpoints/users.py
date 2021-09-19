from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
    ) -> Any:
    return None
