from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from .. import model, schemas

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(model.User).where(model.User.id == user_id))
    return result.scalar()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(model.User).where(model.User.email == email))
    return result.scalar()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(model.User))
    return result.unique().scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    try:
      db_user = model.User(name=user.name, email=user.email, hashed_password=get_password_hash(user.password))
      db.add(db_user)
      await db.commit()
      await db.refresh(db_user)
      return db_user
    except Exception as e:
        await db.rollback()
        raise e


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
