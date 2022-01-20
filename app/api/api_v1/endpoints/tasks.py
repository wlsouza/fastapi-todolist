from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Task],
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if not token_user.is_superuser:
        # return own user tasks
        return await crud.task.get_multi_by_owner_id(
            db=db, owner_id=token_user.id, skip=skip, limit=limit
        )
    # return all tasks
    tasks = await crud.task.get_multi(db=db, skip=skip, limit=limit)
    return tasks


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Task,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def create_task(
    task_in: schemas.TaskCreate = Body(
        ..., examples=schemas.task.TASKCREATE_EXAMPLES
    ),
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    # when the user is not specified the task is generated for the requestor.
    if not task_in.owner_id:
        task_in.owner_id = token_user.id

    if task_in.owner_id == token_user.id:
        task = await crud.task.create(db=db, task_in=task_in)
        return task
    # tasks for other users can only be registered by a superuser.
    if not token_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )

    user = await crud.user.get_by_id(db=db, id=task_in.owner_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner user not found",
        )

    task = await crud.task.create(db=db, task_in=task_in)
    return task


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Task,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def get_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(deps.get_db),
    token_user: models.User = Depends(deps.get_token_active_user),
) -> Any:
    task = await crud.task.get_by_id(db=db, id=task_id)
    if not task:
        # returns error according to user privileges
        if not token_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if not token_user.is_superuser and task.owner_id != token_user.id:
        # another user task
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Task,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(deps.get_db),
    token_user: models.User = Depends(deps.get_token_active_user),
) -> Any:
    task = await crud.task.get_by_id(db=db, id=task_id)
    if not task:
        # returns error according to user privileges
        if not token_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if not token_user.is_superuser and task.owner_id != token_user.id:
        # another user task
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    await crud.task.delete_by_id(db=db, id=task_id)
    return task


# @router.put("/tasks/{id}", response_model=schemas.Task)
# def update_task(id: UUID4, received_task: schemas.TaskUpdate):
#     task_to_update = list(filter(lambda x: x.get("id") == id, TASKS))
#     if not task_to_update:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
#         )
#     updated_task = task_to_update[0]
#     for attribute, value in received_task:
#         updated_task[attribute] = value
#     return updated_task
