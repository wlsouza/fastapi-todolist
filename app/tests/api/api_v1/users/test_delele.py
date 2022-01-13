import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.core.config import settings
from app.tests.utils.auth import (
    get_expired_user_token_headers,
    get_user_token_headers,
)


# region delete own user - DELETE /users/me

@pytest.mark.asyncio
async def test_resource_users_me_must_accept_delete_verb(
    async_client: AsyncClient,
) -> None:
    response = await async_client.delete(url=f"{settings.API_V1_STR}/users/me")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.asyncio
async def test_when_own_user_is_deleted_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_own_user_is_deleted_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.json().get("id") == active_user.id

@pytest.mark.asyncio
async def test_when_deleting_own_user_if_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.delete(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_deleting_own_user_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_own_user_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

# endregion

# region delete own user - DELETE /users/{user_id}
# endregion

