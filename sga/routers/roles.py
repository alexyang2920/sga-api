from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.role import Role as RoleSchema
from ..crud import role as roleDao
from ..dependencies import get_db, RoleChecker


router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[RoleSchema])
async def read_roles(db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
  roles = await roleDao.get_roles(db)
  return roles


@router.get("/{role_id}", response_model=RoleSchema)
async def read_roles(role_id: int, db: AsyncSession = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
  role = await roleDao.get_role(db, role_id)
  if not role:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return role
