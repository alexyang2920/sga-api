from pydantic import BaseModel
from typing import List
from .role import Role


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    roles: List[Role]

    class Config: 
        from_attributes = True

