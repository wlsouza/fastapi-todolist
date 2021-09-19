from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()

@router.post("/")
def create_user(db:Session = Depends(deps.get_db)):
    return None
