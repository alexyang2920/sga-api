from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..roles.service import get_role
from ..dependencies import get_db, get_current_active_user, transactional_context, RoleChecker
from ..utils import get_password_hash

from .service import get_users, get_user, get_user_by_email
from .models import User
from .schemas import UserSchema, UserCreateSchema, OwnerUpdateSchema, UserUpdateSchema


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create new user. anyone could do that.
    """
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    db_user = User(name=user.name, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)

    async with transactional_context(db, to_refresh=[db_user]):
        pass

    return db_user


@router.get("/me", response_model=UserSchema)
async def read_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Read the current user by the logged in user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user(
    update_user: OwnerUpdateSchema,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_db)):
    """
    Update the current user by the logged in user.
    """
    current_user.name = update_user.name
    async with transactional_context(db, to_refresh=[current_user]):
        pass
    return current_user


@router.get("/", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
    """
    Read all users, should only allowed for admin.
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
    """
    Read a specific user with given user id, should only allowed for admin.
    """
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    update_user: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
    """
    Update user, allowed for admin only.
    """
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = update_user.name
    db_user.is_active = update_user.is_active

    async with transactional_context(db, to_refresh=[db_user]):
        pass
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
    """
    Delete a user with given user id, should only allowed for admin.
    """
    db_user = await get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    async with transactional_context(db):
        pass


@router.post("/{user_id}/roles/{role_id}", response_model=UserSchema)
async def add_user_to_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
    """
    Assign a role to a user. should only allowed for admin.
    """
    user = await get_user(db, user_id=user_id)
    role = await get_role(db, role_id=role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="User or Role not found")

    user.roles.append(role)
    async with transactional_context(db, to_refresh=[user]):
        pass

    return user
