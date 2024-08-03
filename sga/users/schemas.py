from pydantic import BaseModel
from typing import List
from ..roles.schemas import RoleSchema


class UserBase(BaseModel):
    name: str
    email: str


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool
    roles: List[RoleSchema]

    class Config: 
        from_attributes = True