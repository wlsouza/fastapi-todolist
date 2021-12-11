from typing import AsyncGenerator

from app.database.session import async_session


async def get_db() -> AsyncGenerator:
    async with async_session() as db:
        yield db