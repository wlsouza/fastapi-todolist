from pydantic import BaseModel, constr, UUID4
from enum import Enum

class TaskStates(str, Enum):
    done = "done"
    not_done = "not-done"

# Shared properties
class TaskBase(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=140)
    state: TaskStates = TaskStates.not_done

# Properties to receive on item creation
class TaskCreate(TaskBase):
    pass

# Properties to receive on item update
class TaskUpdate(TaskBase):
    pass

# Properties to return to client
class Task(TaskBase):
    id: UUID4


