from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Role

async def get_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    return result.scalars().all()


async def get_role(db: AsyncSession, role_id: int):
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalar()

