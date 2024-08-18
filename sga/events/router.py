from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db, transactional_context, RoleChecker
from ..roles.models import RoleEnum

from .schemas import EventSchema, EventCreateSchema, EventUpdateSchema, PaginatedEvents, update_to_model
from .service import get_events, get_event, get_total_count
from .models import Event

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=EventSchema)
async def add_event(event: EventCreateSchema, db: AsyncSession = Depends(get_db),
                    _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
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


@router.get("", response_model=PaginatedEvents)
async def read_events(page_number: int = 1, page_size: int = 20, sort_by = "id", sort_order: str = 'desc', db: AsyncSession = Depends(get_db)):
    if page_number <= 0 or page_size <= 0:
        raise ValueError("Invalid page_number or page_size. Must be greater than 0.")

    if sort_order not in {"asc", "desc"}:
        raise ValueError("Invalid sort_order. Must be 'asc' or 'desc'.")

    total_count = await get_total_count(db)
    events = await get_events(db, (page_number - 1) * page_size, page_size, sort_by, sort_order)
    return {
        "total_count" : total_count,
        "items": events,
        "page_number": page_number,
        "page_size": page_size
    }


@router.get("/{event_id}", response_model=EventSchema)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventSchema)
async def update_event(event_id: int, event_update: EventUpdateSchema, db: AsyncSession = Depends(get_db),
                       _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
    event = await get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event = update_to_model(event_update, event)
    db.add(event)

    async with transactional_context(db, to_refresh=[event]):
        pass

    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db),
                       _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
    """
    Delete a event with given event id, should only allowed for admin.
    """
    event = await get_event(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    await db.delete(event)
    async with transactional_context(db):
        pass
