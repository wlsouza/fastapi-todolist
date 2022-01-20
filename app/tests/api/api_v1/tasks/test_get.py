import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.config import settings
from app.tests.utils.auth import (
    get_expired_user_token_headers,
    get_user_token_headers,
)
from app.tests.utils.task import create_random_task_in_db

# region get tasks - GET /tasks/


@pytest.mark.asyncio
async def test_when_get_tasks_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_get_tasks_must_return_a_list(
    async_client: AsyncClient, active_user: models.User, db: AsyncSession
) -> None:
    headers = get_user_token_headers(active_user)
    db_task = await create_random_task_in_db(db=db, owner_user=active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_when_get_tasks_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User, db: AsyncSession
) -> None:
    headers = get_user_token_headers(active_user)
    db_task = await create_random_task_in_db(db=db, owner_user=active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert response.json()[0].get("id") == db_task.id


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_user_is_superuser_must_return_all_users_tasks(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    tasks_another_user = filter(
        lambda task: task.get("owner_id") != active_superuser.id,
        response.json(),
    )
    assert tasks_another_user


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_user_is_not_superuser_must_return_only_your_own_tasks(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert not response.json()


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(f"{settings.API_V1_STR}/tasks/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_tasks_if_return_the_correct_quantity_of_tasks(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    for _ in range(3):
        await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/?limit=2", headers=headers
    )
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_when_getting_tasks_if_skip_the_correct_quantity_of_tasks(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    tasks = []
    for _ in range(3):
        tasks.append(
            await create_random_task_in_db(db=db, owner_user=active_user)
        )
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/?skip=2&limit=2", headers=headers
    )
    assert response.json()[0].get("id") == tasks[2].id


# endregion

# region get tasks by id - GET /tasks/{task_id}


@pytest.mark.asyncio
async def test_when_get_tasks_by_id_must_return_200(
    db: AsyncSession, async_client: AsyncClient, active_user: models.User
) -> None:
    task = await create_random_task_in_db(db=db, owner_user=active_user)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_get_tasks_by_id_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(
        db=db, owner_user=active_user
    )
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.json().get("id") == created_task.id


@pytest.mark.asyncio
async def test_when_getting_tasks_by_id_of_another_user_if_token_user_is_superuser_must_return_200(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_getting_tasks_by_id_of_another_user_if_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(db=db)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_tasks_by_id_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(f"{settings.API_V1_STR}/tasks/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(
        db=db, owner_user=active_user
    )
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_getting_tasks_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User, db: AsyncSession
) -> None:
    created_task = await create_random_task_in_db(
        db=db, owner_user=inactive_user
    )
    headers = get_user_token_headers(inactive_user)
    response = await async_client.get(
        f"{settings.API_V1_STR}/tasks/{created_task.id}", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# endregion
