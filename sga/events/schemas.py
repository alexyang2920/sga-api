from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title: str
    location: str
    image: str
    content: str
    start_date_time: datetime | None
    end_date_time: datetime | None


class EventCreateSchema(EventBase):
    pass


class EventSchema(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True