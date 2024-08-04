import pytz
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

engine = create_async_engine(settings.database_url, echo=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=False)
Base = declarative_base()


def utc_now():
    return datetime.now(pytz.UTC)
