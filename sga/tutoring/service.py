
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select
from .models import TutoringProgram


async def get_total_count(db: AsyncSession, search: str=''):
    query = select(func.count(TutoringProgram.id));
    if search != '':
        query = query.filter(TutoringProgram.title.ilike(f"%{search}%"))

    result = await db.execute(query)
    return result.scalar()


async def get_tutoring_programs(db: AsyncSession, skip: int = 0, limit: int = 20, sort_by: str = "id", sort_order: str = 'desc', search: str=''):
    query = select(TutoringProgram)

    if search != '':
        query = query.filter(TutoringProgram.title.ilike(f"%{search}%"))

    order_by = getattr(TutoringProgram, sort_by).asc() if sort_order == "asc" else getattr(TutoringProgram, sort_by).desc()

    result = await db.execute(query.order_by(order_by).offset(skip).limit(limit))
    return result.scalars().all()


async def get_tutoring_program(db: AsyncSession, id: int):
    result = await db.execute(select(TutoringProgram).where(TutoringProgram.id == id))
    return result.scalar()
