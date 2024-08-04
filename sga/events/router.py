from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db, transactional_context
from .schemas import EventSchema, EventCreateSchema, EventUpdateSchema, update_to_model
from .service import get_events, get_event
from .models import Event

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=EventSchema)
async def add_event(event: EventCreateSchema, db: AsyncSession = Depends(get_db)):
    db_event = Event(
        title=event.title,
        location=event.location,
        image=event.image,
        content=event.content,
        start_date_time=event.start_date_time,
        end_date_time=event.end_date_time
    )
    db.add(db_event)
    async with transactional_context(db, to_refresh=[db_event]):
        pass

    return db_event


@router.get("/", response_model=list[EventSchema])
async def read_events(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
  events = await get_events(db, skip, limit)
  return events


@router.get("/{event_id}", response_model=EventSchema)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventSchema)
async def read_event(event_id: int, event_update: EventUpdateSchema, db: AsyncSession = Depends(get_db)):
    event = await get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event = update_to_model(event_update, event)
    db.add(event)

    async with transactional_context(db, to_refresh=[event]):
        pass

    return event
