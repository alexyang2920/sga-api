from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.role import Role as RoleSchema
from ..crud import role as roleDao
from ..dependencies import get_db, RoleChecker


router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[RoleSchema])
async def read_roles(db: Session = Depends(get_db), _: bool = Depends(RoleChecker(allowed_roles=['Admin']))):
  roles = roleDao.get_roles(db)
  return roles
