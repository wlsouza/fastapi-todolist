from typing import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()