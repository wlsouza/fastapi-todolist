from typing import Any, Dict, List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


class CrudTask:
    async def get_by_id(
        self, db: AsyncSession, id: Union[int, str]
    ) -> Optional[models.Task]:
        result = await db.execute(
            select(models.Task).where(models.Task.id == id)
        )
        return result.scalar()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Optional[List[models.Task]]:
        result = await db.execute(
            select(models.Task).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        task_in: Union[schemas.TaskCreate, Dict[str, Any]]
    ) -> models.Task:
        if isinstance(task_in, dict):
            task_data = task_in.copy()
        else:
            task_data = task_in.dict()
        db_task = models.Task(**task_data)
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    async def update(
        self,
        db: AsyncSession,
        db_task: models.Task,
        task_in: Union[
            schemas.TaskUpdatePUT, schemas.TaskUpdatePATCH, Dict[str, Any]
        ],
    ) -> models.Task:
        if isinstance(task_in, dict):
            update_data = task_in.copy()
        elif isinstance(task_in, schemas.TaskUpdatePUT):
            update_data = task_in.dict()
        else:
            update_data = task_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_task, field):
                setattr(db_task, field, value)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    async def delete_by_id(
        self, db: AsyncSession, id: Union[int, str]
    ) -> Optional[models.Task]:
        task = await self.get_by_id(db=db, id=id)
        await db.delete(task)
        await db.commit()
        return task


task = CrudTask()
