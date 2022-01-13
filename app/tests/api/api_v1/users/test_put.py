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
from app.tests.utils.user import (
    fake,
    random_active_superuser_dict,
    random_active_user_dict,
    random_user_dict,
)






# region update user - PUT /users/{user_id}


@pytest.mark.asyncio
async def test_when_successfully_update_user_by_id_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_successfully_update_user_by_id_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("full_name") == payload.get("full_name")


@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_token_user_is_not_superuser_it_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{target_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_token_user_is_superuser_the_user_must_be_updated(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    payload = random_user_dict()
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{target_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("full_name") == payload.get("full_name")


@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient, active_user: models.User
) -> None:
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}",
        headers=headers,
        json={},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{inactive_user.id}",
        headers=headers,
        json={},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_user_is_updated_if_email_is_changed_by_non_superuser_the_user_must_be_deactivated(
    active_user: models.User, async_client: AsyncClient
) -> None:
    payload = random_active_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("is_active") is False


@pytest.mark.asyncio
async def test_when_user_is_updated_if_email_is_changed_by_superuser_the_user_must_continue_activate(
    async_client: AsyncClient, active_superuser: models.User
) -> None:
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_superuser.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("is_active") is True


@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_user_not_exist_and_token_user_is_not_superuser_must_return_403(
    active_user: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    payload = random_active_user_dict()
    target_user = await crud.user.create(
        db=db, user_in=payload
    )
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{target_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_user_not_exist_and_token_user_is_superuser_must_return_404(
    active_superuser: models.User, async_client: AsyncClient, db: AsyncSession
) -> None:
    payload = random_active_user_dict()
    target_user = await crud.user.create(
        db=db, user_in=payload
    )
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{target_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_when_updating_user_to_superuser_if_token_user_is_not_superuser_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{active_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_user_to_superuser_if_token_user_is_superuser_must_return_200(
    db: AsyncSession, async_client: AsyncClient, active_superuser: models.User
) -> None:
    target_user = await crud.user.create(
        db=db, user_in=random_active_user_dict()
    )
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/{target_user.id}",
        headers=headers,
        json=payload,
    )
    assert response.json().get("is_superuser") is True


# endregion



# region update own user - PUT /users/me


@pytest.mark.asyncio
async def test_resource_users_me_must_accept_post_verb(
    async_client: AsyncClient,
) -> None:
    response = await async_client.put(url=f"{settings.API_V1_STR}/users/me")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_when_own_user_is_updated_must_return_200(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_active_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_when_own_user_is_updated_it_must_be_returned(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_active_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.json().get("full_name") == payload.get("full_name")


@pytest.mark.asyncio
async def test_when_own_user_is_updated_if_email_is_changed_by_non_superuser_the_user_must_be_deactivated(
    active_user: models.User, async_client: AsyncClient
) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.json().get("is_active") is False


@pytest.mark.asyncio
async def test_when_own_user_is_updated_if_email_is_changed_by_superuser_the_user_must_continue_activate(
    async_client: AsyncClient, active_superuser: models.User
) -> None:
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.json().get("is_active") is True


@pytest.mark.asyncio
async def test_when_updating_own_user_if_body_has_not_valid_field_must_return_422(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = {"id": 1}
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_when_updating_own_user_if_user_is_not_authenticated_must_return_401(
    async_client: AsyncClient,
) -> None:
    response = await async_client.put(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_when_updating_own_user_if_token_is_expired_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_own_user_if_token_user_is_not_active_must_return_403(
    async_client: AsyncClient, inactive_user: models.User
) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_own_user_if_user_not_exist_must_return_404(
    active_user: models.User, async_client: AsyncClient, db:AsyncSession
) -> None:
    headers = get_user_token_headers(active_user)
    await crud.user.delete_by_id(db=db, id=active_user.id)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_when_updating_own_user_to_superuser_if_user_is_not_superuser_must_return_403(
    async_client: AsyncClient, active_user: models.User
) -> None:
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_when_updating_own_user_to_superuser_if_user_is_superuser_must_return_200(
    async_client: AsyncClient, active_superuser: models.User
) -> None:
    payload = random_active_superuser_dict()
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(
        f"{settings.API_V1_STR}/users/me", headers=headers, json=payload
    )
    assert response.status_code == status.HTTP_200_OK


# endregion

# region send verification email - POST /users/{id}/verification -- talvez?
# endregion

# region /users/{id}/activate?token=xpto
