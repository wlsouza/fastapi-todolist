from typing import Dict, Union

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models

fake = Faker()


def random_task_dict() -> Dict[str, Union[str, int, bool]]:
    task_dict = {
        "title": fake.text(max_nb_chars=80),
        "description": fake.paragraph(),
        "is_done": False,
    }
    return task_dict


async def create_random_task_in_db(
    db: AsyncSession, owner_user: models.User = None
) -> models.Task:
    task_dict = random_task_dict()
    if owner_user:
        task_dict["owner_id"] = owner_user.id
    return await crud.task.create(db=db, task_in=task_dict)
