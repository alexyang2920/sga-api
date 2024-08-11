from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List
from ..roles.schemas import RoleSchema


class UserBase(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr

    @field_validator("email")
    def to_lowercase(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value


class UserCreateSchema(UserBase):
    password: str = Field(min_length=8)


class OwnerUpdateSchema(BaseModel):
    """
    Updated fields allowed for owner.
    """
    name: str = Field(min_length=1)


class UserUpdateSchema(BaseModel):
    name: str = Field(min_length=1)
    is_active: bool


class UserSchema(UserBase):
    id: int
    is_active: bool
    roles: List[RoleSchema]

    class Config: 
        from_attributes = True