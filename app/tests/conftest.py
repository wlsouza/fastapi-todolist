from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database.session import SessionLocal

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
    # with SessionLocal() as db:
    #     yield db
