from typing import Generator

from app.database.session import async_session


async def get_db() -> Generator:
    async with async_session() as db:
        yield db