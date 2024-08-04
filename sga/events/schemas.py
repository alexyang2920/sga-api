from pydantic import BaseModel
from datetime import datetime

from .models import Event


class EventBase(BaseModel):
    title: str
    location: str
    image: str
    content: str
    start_date_time: datetime | None
    end_date_time: datetime | None


class EventCreateSchema(EventBase):
    pass


class EventUpdateSchema(EventBase):
    pass


class EventSchema(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


def update_to_model(event_update: EventUpdateSchema, event: Event) -> Event:
    event.title = event_update.title
    event.location = event_update.location
    event.image = event_update.image
    event.content = event_update.content
    event.start_date_time = event_update.start_date_time
    event.end_date_time = event_update.end_date_time
    return event
