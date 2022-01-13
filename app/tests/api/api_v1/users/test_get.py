import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.core.config import settings
from app.tests.utils.user import random_active_user_dict
from app.tests.utils.auth import (
    get_expired_user_token_headers,
    get_user_token_headers,
)


# region Create user - GET /users/{user_id}

@pytest.mark.asyncio
async def test_when_successfully_get_user_by_id_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{active_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_successfully_get_user_by_id_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{active_user.id}", headers=headers
    )
    assert response.json().get("email") == active_user.email


@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_token_user_is_not_superuser_it_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_token_user_is_superuser_the_user_must_be_returned(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers
    )
    assert response.json().get("id") == target_user.id


@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, active_user: models.User
) -> None:
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{active_user.id}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{active_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{inactive_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_user_not_exist_and_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_user_not_exist_and_token_user_is_superuser_must_return_404(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion

# region get own user - GET /users/me

@pytest.mark.asyncio
async def test_when_own_user_is_gotten_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_own_user_is_gotten_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.json().get("id") == active_user.id


@pytest.mark.asyncio
async def test_when_getting_own_user_if_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_getting_own_user_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_own_user_if_user_not_exist_must_return_404(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    headers = get_user_token_headers(active_user)
    await crud.user.delete_by_id(db=db, id=active_user.id)
    response = await async_client.get(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion