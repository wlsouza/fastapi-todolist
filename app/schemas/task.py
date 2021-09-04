from pydantic import BaseModel, Field, UUID4

# Shared properties
class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(max_length=140)
    is_done: bool

# Properties to receive on item creation
class TaskCreate(TaskBase):
    pass

# Properties to receive on item update
class TaskUpdate(TaskBase):
    pass

# Properties shared by models stored in DB
class TaskInDBBase():
    external_id: UUID4
    title: str
    description: str
    is_done: bool
    owner_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Task(TaskInDBBase):
    external_id: UUID4 = Field(alias="id")
    is_done: bool = Field(alias="done")


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass

