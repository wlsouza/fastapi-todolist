import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.tests.utils.user import (
    random_active_superuser_dict,
    random_active_user_dict,
    random_user_dict,
)

@pytest.fixture()
async def active_user(db: AsyncSession) -> models.User:
    user_dict = random_active_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user


@pytest.fixture()
async def inactive_user(db: AsyncSession) -> models.User:
    user_dict = random_user_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user


@pytest.fixture()
async def active_superuser(db: AsyncSession) -> models.User:
    user_dict = random_active_superuser_dict()
    user = await crud.user.create(db=db, user_in=user_dict)
    return user