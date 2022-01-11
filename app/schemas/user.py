from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False

    class Config:
        extra = "forbid"


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: Optional[int]
    is_active: Optional[bool] = False
    is_superuser: bool = False

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
