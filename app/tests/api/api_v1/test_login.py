import pytest
from fastapi import status
from sqlalchemy.orm import Session
from httpx import AsyncClient

from app import schemas
from app.core.config import settings
from app.tests.utils import user
from app.tests.utils.user import random_user_dict

@pytest.mark.asyncio
async def test_resource_token_must_accept_post_verb(async_client: AsyncClient) -> None:
    response = await async_client.post(f"{settings.API_V1_STR}/login/access-token")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

#TODO: refactor the tests to not use /users/ post to create a random user.

@pytest.mark.asyncio
async def test_when_credentials_are_valid_returns_status_200(async_client: AsyncClient) -> None:
    user_dict = random_user_dict()
    await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    payload = {
        "username": user_dict.get("email"),
        "password": user_dict.get("password")
    }
    response = await async_client.post(f"{settings.API_V1_STR}/login/access-token", data=payload)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_credentials_are_invalid_returns_status_401(async_client: AsyncClient) -> None:
    user_dict = random_user_dict()
    await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    payload = {
        "username": user_dict.get("email"),
        "password": f"{user_dict.get('password')}_invalid_password"
    }
    response = await async_client.post(f"{settings.API_V1_STR}/login/access-token", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

