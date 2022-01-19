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
from app.tests.utils.task import random_task_dict
from app.tests.utils.user import random_active_user_dict

# region create task - POST /tasks/


@pytest.mark.asyncio
async def test_resource_task_must_accept_post_verb(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(url=f"{settings.API_V1_STR}/tasks/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_task_is_created_returns_status_201(
    active_user: models.User,
    async_client: AsyncClient,
) -> None:
    headers = get_user_token_headers(active_user)
    task_dict = random_task_dict() | {"owner_id": active_user.id}
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_when_task_is_created_it_must_be_returned(
    active_user: models.User,
    async_client: AsyncClient,
) -> None:
    headers = get_user_token_headers(active_user)
    task_dict = random_task_dict() | {"owner_id": active_user.id}
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert task_dict["title"] == response.json().get("title")


@pytest.mark.asyncio
async def test_when_task_is_created_it_must_be_persisted(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    headers = get_user_token_headers(active_user)
    task_dict = random_task_dict() | {"owner_id": active_user.id}
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    db_task = await crud.task.get_by_id(db=db, id=response.json().get("id"))
    assert db_task


@pytest.mark.asyncio
async def test_when_creating_task_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, active_user: models.User
) -> None:
    task_dict = random_task_dict() | {"owner_id": active_user.id}
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", json=task_dict
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_creating_task_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    task_dict = random_task_dict() | {"owner_id": active_user.id}
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_creating_task_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    task_dict = random_task_dict() | {"owner_id": inactive_user.id}
    headers = get_user_token_headers(inactive_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_creating_task_to_another_user_if_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    task_dict = random_task_dict() | {"owner_id": target_user.id}
    headers = get_user_token_headers(active_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_creating_task_to_another_user_if_token_user_is_superuser_must_return_201(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    task_dict = random_task_dict() | {"owner_id": target_user.id}
    headers = get_user_token_headers(active_superuser)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_when_creating_task_to_non_existent_user_if_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    task_dict = random_task_dict() | {"owner_id": target_user.id}
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_creating_task_to_non_existent_user_if_token_user_is_superuser_must_return_404(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    task_dict = random_task_dict() | {"owner_id": target_user.id}
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.post(
        f"{settings.API_V1_STR}/tasks/", headers=headers, json=task_dict
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# endregion
