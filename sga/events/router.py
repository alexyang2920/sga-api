from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db
from .schemas import EventSchema, EventCreateSchema
from .service import get_events, get_event, create_event

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=EventSchema)
async def add_event(event: EventCreateSchema, db: AsyncSession = Depends(get_db)):    
    return await create_event(db=db, event=event)


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
