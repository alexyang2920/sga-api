from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..roles.service import get_role
from ..dependencies import get_db, get_current_active_user

from .service import get_users, get_user, get_user_by_email, create_user
from .models import User
from .schemas import UserSchema, UserCreateSchema


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=UserSchema)
async def read_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.get("/", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
  users = await get_users(db, skip=skip, limit=limit)
  return users


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await create_user(db=db, user=user)


@router.post("/{user_id}/roles/{role_id}", response_model=UserSchema)
async def add_user_to_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    role = get_role(db, role_id=role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")
    
    try:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise e

    return user
