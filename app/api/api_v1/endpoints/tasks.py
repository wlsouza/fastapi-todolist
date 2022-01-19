from typing import Any

from fastapi import APIRouter, Depends,HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models, crud
from app.api import deps

router = APIRouter()


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Task,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES
)
async def create_task(
    task_in: schemas.TaskCreate = Body(
        ..., 
        examples=schemas.task.TASKCREATE_EXAMPLES
    ),
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    if not task_in.owner_id:
        task_in.owner_id = token_user.id

    if task_in.owner_id == token_user.id:
        task = await crud.task.create(db=db, task_in=task_in)
        return task

    if not token_user.is_superuser:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )

    user = await crud.user.get_by_id(db=db, id=task_in.owner_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner user not found"
        )
    
    task = await crud.task.create(db=db, task_in=task_in)
    return task


# @router.get("/tasks", response_model=list[schemas.Task])
# def list_tasks() -> Any:
#     TASKS.sort(reverse=True, key=lambda x: x["state"])
#     return TASKS


# @router.delete(
#     "/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT
# )  # , responses= {status.HTTP_404_NOT_FOUND:{"detail": "Task not found"}})
# def delete_task(id: UUID4):
#     task = list(filter(lambda x: x.get("id") == id, TASKS))
#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
#         )
#     TASKS.remove(task[0])
#     return None


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


# @router.get("/tasks/{id}")
# def get_task_id(id: UUID4):
#     task = list(filter(lambda x: x.get("id") == id, TASKS))
#     if not task:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
#         )
#     return task[0]
