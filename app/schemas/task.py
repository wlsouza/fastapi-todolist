from typing import Optional

from pydantic import BaseModel


# Shared properties
class TaskBase(BaseModel):
    title: str
    description: str 
    is_done: bool


# Properties to receive on item creation
class TaskCreate(TaskBase):
    pass

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
    title: str
    description: str
    is_done: bool
    owner_id: int

    class Config:
        extra = "forbid"

# Properties shared by models stored in DB
class TaskInDBBase:
    id: str
    title: str
    description: str
    is_done: bool
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Task(TaskInDBBase):
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
