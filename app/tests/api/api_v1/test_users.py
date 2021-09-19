from os import SEEK_DATA
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_resource_users_must_accept_post_verb(client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/users/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_creating_user_if_that_user_already_exist_returns_status_400(client: TestClient):
    pass

def test_when_user_is_created_returns_status_201(client: TestClient) -> None:
    pass

def test_when_user_is_created_it_must_be_returned(client: TestClient) -> None:
    pass

def test_when_user_is_created_it_must_be_persisted(client: TestClient, db: Session) -> None:
    pass

