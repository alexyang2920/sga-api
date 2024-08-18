
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from .models import Event


async def get_total_count(db: AsyncSession):
    result = await db.execute(select(func.count(Event.id)))
    return result.scalar()


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 20, order_by = Event.id.desc()):
    result = await db.execute(select(Event).order_by(order_by).offset(skip).limit(limit))
    return result.scalars().all()


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar()
