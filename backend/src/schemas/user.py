from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass


class UserList(BaseModel):
    users: list[User]
