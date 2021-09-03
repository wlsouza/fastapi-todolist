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

