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
from app.tests.utils.task import create_random_task_in_db

# region delete task by id - DELETE /tasks/{task_id}


@pytest.mark.asyncio
async def test_resource_tasks_by_id_must_accept_delete_verb(
    async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}"
    )
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_task_is_deleted_by_id_must_return_200(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=active_user)
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_task_is_deleted_by_id_it_must_be_returned(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=active_user)
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.json().get("id") == task.id


@pytest.mark.asyncio
async def test_when_task_is_deleted_by_id_it_must_be_persisted(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=active_user)
    headers = get_user_token_headers(active_user)
    await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    db_user = await crud.task.get_by_id(db=db, id=task.id)
    assert not db_user


@pytest.mark.asyncio
async def test_when_deleting_task_by_id_if_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.delete(f"{settings.API_V1_STR}/tasks/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_deleting_task_by_id_if_token_is_expired_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=active_user)
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_task_by_id_if_token_user_is_not_active_must_return_403(
    inactive_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=inactive_user)
    headers = get_user_token_headers(inactive_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_task_of_another_user_by_id_if_token_user_is_superuser_must_return_200(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_deleting_task_of_another_user_by_id_if_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    task = await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_task_of_another_user_by_id_if_task_not_exist_and_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(db=db)
    await crud.task.delete_by_id(db=db, id=created_task.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_deleting_task_of_another_user_by_id_if_task_not_exist_and_token_user_is_superuser_must_return_404(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(db=db)
    await crud.task.delete_by_id(db=db, id=created_task.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.delete(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# endregion
