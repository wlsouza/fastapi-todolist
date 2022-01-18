import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.tests.utils.task import random_task_dict

@pytest.mark.asyncio
async def test_create_task_by_schema(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    task_in = schemas.TaskCreate(**task_dict)
    new_task = await crud.task.create(db=db, task_in=task_in)
    assert new_task.title == task_in.title


@pytest.mark.asyncio
async def test_create_task_by_dict(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    assert new_task.title == task_dict.get("title")


@pytest.mark.asyncio
async def test_when_create_task_if_owner_id_is_not_set_it_must_be_none(
    db: AsyncSession,
) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    assert new_task.owner_id is None


@pytest.mark.asyncio
async def test_if_get_by_id_return_correct_task(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    returned_task = await crud.task.get_by_id(db=db, id=new_task.id)
    assert returned_task.title == task_dict.get("title")


@pytest.mark.asyncio
async def test_if_delete_by_id_really_delete_the_task(db: AsyncSession):
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    await crud.task.delete_by_id(db=db, id=new_task.id)
    returned_task = await crud.task.get_by_id(db=db, id=new_task.id)
    assert returned_task is None


@pytest.mark.asyncio
async def test_update_user_by_taskupdateput_schema(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    task_update_in = schemas.TaskUpdatePUT(**random_task_dict(), owner_id = 0)
    updated_task = await crud.task.update(
        db=db, db_task=new_task, task_in=task_update_in
    )
    assert updated_task.title == task_update_in.title


@pytest.mark.asyncio
async def test_update_user_by_taskupdatepatch_schema(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    task_update_in = schemas.TaskUpdatePATCH(**random_task_dict())
    updated_task = await crud.task.update(
        db=db, db_task=new_task, task_in=task_update_in
    )
    assert updated_task.title == task_update_in.title


@pytest.mark.asyncio
async def test_update_task_by_dict(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    task_update_in = random_task_dict()
    updated_task = await crud.task.update(
        db=db, db_task=new_task, task_in=task_update_in
    )
    assert updated_task.title == task_update_in.get("title")


@pytest.mark.asyncio
async def test_if_get_multi_return_a_list_of_task(db: AsyncSession) -> None:
    task_dict = random_task_dict()
    new_task = await crud.task.create(db=db, task_in=task_dict)
    tasks = await crud.task.get_multi(db=db, limit=1)
    assert isinstance(tasks, list)


@pytest.mark.asyncio
async def test_if_get_multi_return_the_correct_quantity_of_task(
    db: AsyncSession,
) -> None:
    for _ in range(3):
        await crud.task.create(db=db, task_in=random_task_dict())
    tasks = await crud.task.get_multi(db=db, limit=2)
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_if_get_multi_skip_the_correct_quantity_of_task(
    db: AsyncSession,
) -> None:
    for _ in range(3):
        await crud.task.create(db=db, task_in=random_task_dict())
    tasks = await crud.task.get_multi(db=db, skip=2, limit=1)
    assert tasks[0].id == 3
