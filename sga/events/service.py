
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Event


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Event))
    return result.unique().scalars().all()


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar()
