import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_v1_router
from app.core.config import settings


app = FastAPI()

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
# TASKS: list[dict[str, Union[str, UUID4, TaskStates]]] = [
#     {
#         "id": UUID4("020f5896-4bfa-4017-8d83-19a6eb489895"),
#         "title": "Take a shower",
#         "description": "Take a shower to go to work.",
#         "state": TaskStates.not_done,
#     },{
#         "id": UUID4("11455eca-8f56-403b-a257-485ee61a2d80"),
#         "title": "Fuel the car",
#         "description": "fuel the car because it is out of gas.",
#         "state": TaskStates.done,
#     },{
#         "id": UUID4("48312036-71a4-44be-9d90-17ab1adaefea"),
#         "title": "Feed the dog",
#         "description": "Feed the dog tonight.",
#         "state": TaskStates.not_done
#     },
# ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)