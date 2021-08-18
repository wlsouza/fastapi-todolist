from typing import Union
from fastapi import FastAPI

app = FastAPI()

TASKS: list[dict[str, Union[str, int]]] = [
    {
        "id": 1,
        "title": "Take a shower",
        "description": "Take a shower to go to work.",
        "state": "not-done",
    },{
        "id": 2,
        "title": "Fuel the car",
        "description": "fuel the car because it is out of gas.",
        "state": "done",
    },{
        "id": 3,
        "title": "Feed the dog",
        "description": "Feed the dog tonight.",
        "state": "not-done",
    },
]

@app.get("/tasks")
def list_tasks():
    return TASKS