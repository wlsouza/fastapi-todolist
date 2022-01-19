from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class TaskBase(BaseModel):
    title: str
    description: str 
    is_done: bool
    owner_id : int


# Properties to receive on item creation
class TaskCreate(TaskBase):
    owner_id: Optional[int]

    # OpenAPI does not support this way of declaring examples yet, for more
    # information read the following documentation
    # https://fastapi.tiangolo.com/tutorial/schema-extra-example/
    # class Config:
    #     schema_extra = {
    #         "examples" : [
    #             {
    #                 "summary": "Task for own user",
    #                 "description": "A task for **own** user .",
    #                 "value": {
    #                     "title": "Wash the car",
    #                     "description": "Wash the car",
    #                     "is_done": False
    #                 }
    #             },
    #             {
    #                 "summary": "Task for another user",
    #                 "description": "A task for the user with **id equal to 1**",
    #                 "value": {
    #                     "title": "Wash the car",
    #                     "description": "Wash the car",
    #                     "is_done": False,
    #                     "owner_id": 1,
    #                 }
    #             },
    #         ]
    #     }

# Properties to receive via API on update -- PATCH (allows not filling all fields)
class TaskUpdatePATCH(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: bool = False
    owner_id: Optional[int] = None

    class Config:
        extra = "forbid"


# Properties to receive via API on update -- PUT (force fill all fields)
class TaskUpdatePUT(TaskBase):
    pass

    class Config:
        extra = "forbid"

# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Task(TaskInDBBase):
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass



TASKCREATE_EXAMPLES = {
            "own user" : {
                "summary": "Task for own user",
                "description": "A task for **own** user.",
                "value": {
                    "title": "Wash the car",
                    "description": "Wash the car",
                    "is_done": False
                }
            },
            "another user": {
                "summary": "Task for another user",
                "description": "A task for the user with id equal to 1. (**superuser privileges required**) ",
                "value": {
                    "title": "Wash the car",
                    "description": "Wash the car",
                    "is_done": False,
                    "owner_id": 1,
                }
            },
        }