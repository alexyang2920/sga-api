from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import user as userDao
from ..crud import role as roleDao
from ..dependencies import get_db, get_current_active_user
from .. import models


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=schemas.User)
def read_root(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return current_user


@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  users = userDao.get_users(db, skip=skip, limit=limit)
  return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userDao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = userDao.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return userDao.create_user(db=db, user=user)


@router.post("/{user_id}/roles/{role_id}", response_model=schemas.User)
async def add_user_to_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = userDao.get_user(db, user_id=user_id)
    role = roleDao.get_role(db, role_id=role_id)
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
