from app.crud import crud_user
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate
from app.tests.utils.user import random_user_dict


def test_create_user_by_schema(db: Session) -> None:
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = crud.user.create(db=db, user_in=user_in)
    assert new_user.email == user_in.email

def test_create_user_by_dict(db: Session) -> None:
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    assert new_user.email == user_dict["email"]

def test_when_create_user_return_hashed_password(db: Session) -> None:
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = crud.user.create(db=db, user_in=user_in)
    assert hasattr(new_user, "hashed_password")

def test_when_create_user_if_attribute_is_active_is_not_set_it_must_be_true(db: Session) -> None:
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    assert new_user.is_active == True

def test_when_create_user_if_attribute_is_superuser_is_not_set_it_must_be_false(db: Session) -> None:
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    assert new_user.is_superuser == False

def test_if_get_by_email_return_correct_user(db: Session) -> None:
    user_dict = random_user_dict()
    crud.user.create(db=db, user_in=user_dict)
    returned_user = crud.user.get_by_email(db=db, email=user_dict["email"])
    assert returned_user.email == user_dict["email"]

def test_if_get_by_id_return_correct_user(db: Session) -> None:
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    returned_user = crud.user.get_by_id(db=db, id= new_user.id)
    assert returned_user.id == new_user.id

def test_if_delete_by_id_really_delete_the_user(db: Session):
    user_dict = random_user_dict()
    new_user = crud.user.create(db=db, user_in=user_dict)
    crud.user.delete_by_id(db=db, id=new_user.id)
    returned_user = crud.user.get_by_id(db=db, id=new_user.id)
    assert returned_user == None