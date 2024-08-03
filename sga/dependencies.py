from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .models.user import User
from .models.meta import SessionLocal
from .security import oauth2_scheme, parse_access_token
from .crud import user as userDao


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    payload = parse_access_token(token)
    username = payload.get("sub") if payload else None
    user = userDao.get_user_by_email(db, username) if username else None
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
