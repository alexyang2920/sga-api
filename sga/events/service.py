
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Event
from .schemas import EventSchema


async def create_event(db: AsyncSession, event: EventSchema):
    try:
      db_event = Event(
          title=event.title,
          location=event.location,
          image=event.image,
          content=event.content,
          start_date_time=event.start_date_time,
          end_date_time=event.end_date_time
      )
      db.add(db_event)
      await db.commit()
      await db.refresh(db_event)
      return db_event
    except Exception as e:
        await db.rollback()
        raise e


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Event))
    return result.unique().scalars().all()


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar()
