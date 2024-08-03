from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from contextlib import asynccontextmanager
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .users.models import User
from .users.service import get_user_by_email
from .database import SessionLocal
from .utils import parse_access_token

# declare that the token url is '/api/auth/token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


async def get_db():
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def transactional_session():
    async with get_db() as session:
        async with session.begin():
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=500, detail=str(e))


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    payload = parse_access_token(token)
    username = payload.get("sub") if payload else None
    user = await get_user_by_email(db, username) if username else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class AuthenticatedChecker:

    def __call__(self, _: User = Depends(get_current_active_user)) -> bool:
        return True;


class RoleChecker:

    def __init__(self, allowed_roles: list[str] | None = None) -> None:
        self.allowed_roles = allowed_roles
    
    def __call__(self, user: User = Depends(get_current_active_user)) -> bool:
        if not self.allowed_roles:
            return True

        if user.roles:
            role_names = set([role.name for role in user.roles])
            for role in self.allowed_roles:
                if role in role_names:
                    return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="403 Forbiden")
