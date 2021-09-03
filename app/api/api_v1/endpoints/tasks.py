from typing import Any

from fastapi import APIRouter, status, HTTPException
from pydantic import UUID4

from app import schemas

router = APIRouter()

@router.get("/tasks", response_model=list[schemas.Task])
def list_tasks() -> Any:
    TASKS.sort(reverse=True, key= lambda x: x["state"])
    return TASKS

@router.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate) -> Any:
    new_task = task.dict()
    new_task["id"] = uuid4()
    TASKS.append(new_task)
    return new_task

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT) #, responses= {status.HTTP_404_NOT_FOUND:{"detail": "Task not found"}})
def delete_task(id: UUID4):
    task = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    TASKS.remove(task[0])
    return None

@router.put("/tasks/{id}", response_model=schemas.Task)
def update_task(id: UUID4, received_task: schemas.TaskUpdate):
    task_to_update = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    updated_task = task_to_update[0]
    for attribute, value in received_task:
        updated_task[attribute] = value
    return updated_task

@router.get("/tasks/{id}")
def get_task_id(id:UUID4):
    task = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task[0]