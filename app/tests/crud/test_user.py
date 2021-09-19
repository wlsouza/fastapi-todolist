from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.tests.utils.user import random_user_dict


def test_create_user_by_schema(db: Session):
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = crud.user.create(db=db, user_in=user_in)
    assert new_user.email == user_in.email

def test_create_user_by_dict(db: Session):
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    assert new_user.email == user_dict["email"]

def test_when_create_user_return_hashed_password(db: Session):
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = crud.user.create(db=db, user_in=user_in)
    assert hasattr(new_user, "hashed_password")

