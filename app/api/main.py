from enum import Enum
from typing import Any, Union, Optional
from uuid import uuid4
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, constr, UUID4

app = FastAPI()

TASKS: list[dict[str, Union[str, UUID4, TaskStates]]] = [
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
    TASKS.sort(reverse=True, key= lambda x: x["state"])
    return TASKS

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Any:
    new_task = task.dict()
    new_task["id"] = uuid4()
    TASKS.append(new_task)
    return new_task

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT) #, responses= {status.HTTP_404_NOT_FOUND:{"detail": "Task not found"}})
def delete_task(id: UUID4):
    task = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    TASKS.remove(task[0])
    return None

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: UUID4, received_task: TaskUpdate):
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

@app.get("/tasks/{id}")
def get_task_id(id:UUID4):
    task = list(filter(lambda x: x.get("id") == id, TASKS))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task[0]