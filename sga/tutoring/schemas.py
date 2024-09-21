from pydantic import BaseModel, Field
from datetime import datetime

from .models import TutoringProgram


class TutoringProgramBase(BaseModel):
    title: str = Field(min_length=1)
    is_active: bool


class TutoringProgramCreateSchema(TutoringProgramBase):
    pass


class TutoringProgramUpdateSchema(TutoringProgramBase):
    pass


class TutoringProgramSchema(TutoringProgramBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config: 
        from_attributes = True


class PaginatedTutoringPrograms(BaseModel):
    items: list[TutoringProgramSchema]
    total_count: int
    page_number: int
    page_size: int


def new_to_model(to_create: TutoringProgramCreateSchema) -> TutoringProgram:
    return TutoringProgram(
        title=to_create.title,
        is_active=to_create.is_active
    )


def update_to_model(to_update: TutoringProgramUpdateSchema, model: TutoringProgram) -> TutoringProgram:
    model.title = to_update.title
    model.is_active = to_update.is_active
    return model
