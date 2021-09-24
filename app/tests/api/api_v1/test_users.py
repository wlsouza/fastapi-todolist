from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.user import random_user_dict

def test_resource_users_must_accept_post_verb(client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/users/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_user_is_created_returns_status_201(client: TestClient) -> None:
    user_dict = random_user_dict()
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert response.status_code == status.HTTP_201_CREATED

def test_when_user_is_created_it_must_be_returned(client: TestClient) -> None:
    user_dict = random_user_dict()
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert user_dict["email"] == response.json().get("email")

def test_when_user_is_created_it_must_be_persisted(client: TestClient, db: Session) -> None:
    user_dict = random_user_dict()
    client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    db_user = crud.user.get_by_email(db=db, email=user_dict["email"])
    assert db_user

def test_when_creating_user_if_that_user_already_exist_returns_status_400(client: TestClient, db: Session) -> None:
    user_dict = random_user_dict()
    crud.user.create(db=db, user_in=user_dict)
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

