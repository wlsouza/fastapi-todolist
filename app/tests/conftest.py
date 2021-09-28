from typing import Generator

import pytest
from httpx import AsyncClient

from app.main import app
from app.database.session import async_session

@pytest.fixture(scope="module")
async def async_client() -> Generator:
    async with AsyncClient(app=app) as async_client:
        yield async_client

@pytest.fixture()
async def db() -> Generator:
    async with async_session() as db:
        yield db
