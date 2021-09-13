from fastapi.testclient import TestClient
from fastapi import status
from requests.sessions import Session

from app.core.config import settings
from app import schemas

def test_resource_token_must_accept_port_verb(client: TestClient) -> None:
    response = client.post(f"{settings.API_V1_STR}/login/access-token")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

def test_when_credential_are_valid_retuns_status_200(db: Session, client: TestClient) -> None:
    pass
    # TODO: IMPLEMENT AN INSERT OF A USER TO TEST
    # payload = {
    #     "username": None,
    #     "password": None
    # }
    # response = client.post(f"{settings.API_V1_STR}/login/access-token", data=payload)
    # assert response.status_code == status.HTTP_200_OK