import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.database.session import async_session
from app.main import app


@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url=settings.BASE_URL
    ) as async_client:
        yield async_client


@pytest.fixture(scope="session")
async def db() -> AsyncGenerator:
    async with async_session() as db:
        yield db


# to correct the error "RuntimeError: Task attached to a different loop"
# https://github.com/pytest-dev/pytest-asyncio/issues/38#issuecomment-264418154
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
