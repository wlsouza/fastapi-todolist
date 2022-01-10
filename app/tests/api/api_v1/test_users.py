
import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from app import crud, models
from app.core.config import settings
from app.tests.utils.user import fake, random_user_dict, random_active_user_dict, random_active_superuser_dict
from app.tests.utils.auth import get_user_token_headers, get_expired_user_token_headers


@pytest.fixture(scope="session")
async def active_user(db: AsyncSession) -> models.User:
    user_dict = random_active_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user

@pytest.fixture(scope="session")
async def inactive_user(db: AsyncSession) -> models.User:
    user_dict = random_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user

@pytest.fixture(scope="session")
async def active_superuser(db: AsyncSession) -> models.User:
    user_dict = random_active_superuser_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user

# region Create user - GET /users/{user_id}

@pytest.mark.asyncio
async def test_when_successfully_get_user_by_id_must_return_200(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{active_user.id}",headers=headers)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_successfully_get_user_by_id_it_must_be_returned(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{active_user.id}",headers=headers)
    assert response.json().get("email") == active_user.email

@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_token_user_is_not_superuser_it_must_return_403(active_user:models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=user_dict)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{target_user.id}",headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_token_user_is_superuser_the_user_must_be_returned(active_superuser:models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{target_user.id}",headers=headers)
    assert response.json().get("id") == target_user.id

@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_user_is_not_authenticated_must_return_401(async_client: AsyncClient, active_user:models.User) -> None:
    response = await async_client.get(f"{settings.API_V1_STR}/users/{active_user.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_is_expired_must_return_403(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{active_user.id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_user_by_id_if_token_user_is_not_active_must_return_403(async_client: AsyncClient, inactive_user:models.User) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{inactive_user.id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_user_not_exist_and_token_user_is_not_superuser_must_return_403(active_user: models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_different_user_by_id_if_user_not_exist_and_token_user_is_superuser_must_return_404(active_superuser: models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.get(f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
# endregion

# region update user - PUT /users/{user_id}

@pytest.mark.asyncio
async def test_when_successfully_update_user_by_id_must_return_200(async_client: AsyncClient, active_user:models.User) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{active_user.id}",headers=headers, json=payload)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_successfully_update_user_by_id_it_must_be_returned(async_client: AsyncClient, active_user:models.User) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{active_user.id}",headers=headers, json=payload)
    assert response.json().get("email") == payload.get("email")

@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_token_user_is_not_superuser_it_must_return_403(active_user:models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=user_dict)
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{target_user.id}",headers=headers, json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_token_user_is_superuser_the_user_must_be_updated(active_superuser:models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    payload = random_user_dict() 
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{target_user.id}",headers=headers, json=payload)
    assert response.json().get("full_name") == payload.get("full_name")

@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_user_is_not_authenticated_must_return_401(async_client: AsyncClient, active_user:models.User) -> None:
    response = await async_client.put(f"{settings.API_V1_STR}/users/{active_user.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_is_expired_must_return_403(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{active_user.id}", headers=headers, json={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_user_by_id_if_token_user_is_not_active_must_return_403(async_client: AsyncClient, inactive_user:models.User) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{inactive_user.id}", headers=headers, json={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_user_not_exist_and_token_user_is_not_superuser_must_return_403(active_user: models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers, json={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_different_user_by_id_if_user_not_exist_and_token_user_is_superuser_must_return_404(active_superuser: models.User, async_client: AsyncClient, db: AsyncSession) -> None:
    target_user_dict = random_active_user_dict()
    target_user = await crud.user.create(db=db, user_in=target_user_dict)
    await crud.user.delete_by_id(db=db, id=target_user.id)
    headers = get_user_token_headers(active_superuser)
    response = await async_client.put(f"{settings.API_V1_STR}/users/{target_user.id}", headers=headers, json={})
    assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion


# region create user - POST /users/

@pytest.mark.asyncio
async def test_resource_users_must_accept_post_verb(async_client: AsyncClient) -> None:
    response = await async_client.post(url=f"{settings.API_V1_STR}/users/")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.asyncio
async def test_when_user_is_created_returns_status_201(async_client: AsyncClient) -> None:
    user_dict = random_user_dict()
    response = await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_when_user_is_created_it_must_be_returned(async_client: AsyncClient) -> None:
    user_dict = random_user_dict()
    response = await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert user_dict["email"] == response.json().get("email")

@pytest.mark.asyncio
async def test_when_user_is_created_it_must_be_persisted(async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_user_dict()
    await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    db_user = await crud.user.get_by_email(db=db, email=user_dict.get("email"))
    assert db_user

@pytest.mark.asyncio
async def test_when_creating_user_if_that_user_already_exist_returns_status_400(async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    response = await async_client.post(f"{settings.API_V1_STR}/users/", json=user_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# endregion

# region get own user - GET /users/me

@pytest.mark.asyncio
async def test_when_own_user_is_gotten_must_return_200(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_own_user_is_gotten_it_must_be_returned(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.json().get("id") == active_user.id

@pytest.mark.asyncio
async def test_when_getting_own_user_if_user_is_not_authenticated_must_return_401(async_client: AsyncClient) -> None:
    response = await async_client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_getting_own_user_if_token_is_expired_must_return_403(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_getting_own_user_if_user_not_exist_must_return_404(async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_active_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    headers = get_user_token_headers(user)
    await crud.user.delete_by_id(db=db, id=user.id)
    response = await async_client.get(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion

# region update own user - PUT /users/me

@pytest.mark.asyncio
async def test_resource_users_must_accept_post_verb(async_client: AsyncClient) -> None:
    response = await async_client.put(url=f"{settings.API_V1_STR}/users/me")
    assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.asyncio
async def test_when_own_user_is_updated_must_return_200(async_client: AsyncClient, active_user:models.User) -> None:
    payload = random_user_dict()
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers, json=payload)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_when_own_user_is_updated_it_must_be_returned(async_client: AsyncClient, active_user:models.User) -> None:
    payload = {"full_name": fake.name()}
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers, json=payload)
    assert response.json().get("full_name") == payload.get("full_name")

@pytest.mark.asyncio
async def test_when_updating_own_user_if_body_has_not_valid_field_must_return_422(async_client: AsyncClient, active_user:models.User) -> None:
    payload = {"id": 1}
    headers = get_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_when_updating_own_user_if_user_is_not_authenticated_must_return_401(async_client: AsyncClient) -> None:
    response = await async_client.put(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_when_updating_own_user_if_token_is_expired_must_return_403(async_client: AsyncClient, active_user:models.User) -> None:
    headers = get_expired_user_token_headers(active_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_own_user_if_token_user_is_not_active_must_return_403(async_client: AsyncClient, inactive_user:models.User) -> None:
    headers = get_user_token_headers(inactive_user)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_when_updating_own_user_if_user_not_exist_must_return_404(async_client: AsyncClient, db: AsyncSession) -> None:
    user_dict = random_active_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    headers = get_user_token_headers(user)
    await crud.user.delete_by_id(db=db, id=user.id)
    response = await async_client.put(f"{settings.API_V1_STR}/users/me", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion