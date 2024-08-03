from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db, RoleChecker

from .schemas import RoleSchema
from .service import get_roles, get_role


router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[RoleSchema])
async def read_roles(db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
  roles = await get_roles(db)
  return roles


@router.get("/{role_id}", response_model=RoleSchema)
async def read_roles(role_id: int, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
  role = await get_role(db, role_id)
  if not role:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return role
