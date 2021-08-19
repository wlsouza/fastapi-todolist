from enum import Enum
from typing import Any, Union, Optional
from uuid import uuid4
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, constr, UUID4

app = FastAPI()


class TaskStates(str, Enum):
    done = "done"
    not_done = "not-done"

class TaskBase(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    state: TaskStates = TaskStates.not_done

class Task(TaskBase):
    id: Union[UUID4, int, str]

class TaskCreate(TaskBase):
    pass

TASKS: list[dict[str, Union[int, str, UUID4, TaskStates]]] = [
    {
        "id": UUID4("020f5896-4bfa-4017-8d83-19a6eb489895"),
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": TaskStates.not_done,
    },{
        "id": UUID4("11455eca-8f56-403b-a257-485ee61a2d80"),
        "title": "Fuel the car",
        "description": "fuel the car because it is out of gas.",
        "state": TaskStates.done,
    },{
        "id": UUID4("48312036-71a4-44be-9d90-17ab1adaefea"),
        "title": "Feed the dog",
        "description": "Feed the dog tonight.",
        "state": TaskStates.not_done
    },
]

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> Any:
    return TASKS

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Any:
    new_task = task.dict()
    new_task["id"] = uuid4()
    TASKS.append(new_task)
    return new_task

@app.delete("/tasks/{id}")
def delete_task(id: UUID4):
    task = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    TASKS.remove(task[0])