from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db, transactional_context, RoleChecker
from ..roles.models import RoleEnum

from .schemas import TutoringProgramSchema, TutoringProgramCreateSchema, TutoringProgramUpdateSchema, PaginatedTutoringPrograms, update_to_model, new_to_model
from .service import get_tutoring_programs, get_tutoring_program, get_total_count
from .models import TutoringProgram

router = APIRouter(
    prefix="/tutoring-programs",
    tags=["Tutoring Programs"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=TutoringProgramSchema)
async def add_tutoring_program(to_create: TutoringProgramCreateSchema, db: AsyncSession = Depends(get_db),
                    _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
    db_tutoring_program = new_to_model(to_create);
    db.add(db_tutoring_program)
    async with transactional_context(db, to_refresh=[db_tutoring_program]):
        pass

    return db_tutoring_program


@router.get("", response_model=PaginatedTutoringPrograms)
async def read_tutoring_programs(page_number: int = 1, page_size: int = 20, sort_by = "id", sort_order: str = 'desc', search: str = '', db: AsyncSession = Depends(get_db)):
    if page_number <= 0 or page_size <= 0:
        raise ValueError("Invalid page_number or page_size. Must be greater than 0.")

    if sort_order not in {"asc", "desc"}:
        raise ValueError("Invalid sort_order. Must be 'asc' or 'desc'.")

    total_count = await get_total_count(db, search.strip());
    items = await get_tutoring_programs(db, (page_number - 1) * page_size, page_size, sort_by, sort_order, search.strip())
    return {
        "total_count" : total_count,
        "items": items,
        "page_number": page_number,
        "page_size": page_size
    }


@router.get("/{tutoring_program_id}", response_model=TutoringProgramSchema)
async def read_tutoring_program(tutoring_program_id: int, db: AsyncSession = Depends(get_db)):
    db_program = await get_tutoring_program(db, id=tutoring_program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Tutoring program not found")
    return db_program


@router.put("/{tutoring_program_id}", response_model=TutoringProgramSchema)
async def update_tutoring_program(tutoring_program_id: int, to_update: TutoringProgramUpdateSchema, db: AsyncSession = Depends(get_db),
                       _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
    db_program = await get_tutoring_program(db, id=tutoring_program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Tutoring program not found")

    db_program = update_to_model(to_update, db_program)
    db.add(db_program)

    async with transactional_context(db, to_refresh=[db_program]):
        pass

    return db_program


@router.delete("/{tutoring_program_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tutoring_program(tutoring_program_id: int, db: AsyncSession = Depends(get_db),
                       _: bool = Depends(RoleChecker(allowed_roles=[RoleEnum.Admin]))):
    db_program = await get_tutoring_program(db, id=tutoring_program_id)
    if db_program is None:
        raise HTTPException(status_code=404, detail="Tutoring program not found")

    await db.delete(db_program)
    async with transactional_context(db):
        pass
