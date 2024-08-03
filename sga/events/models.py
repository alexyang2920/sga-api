from sqlalchemy import DateTime, Column, Integer, String, TEXT, func

from ..database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement='auto')
    title = Column(String(200), nullable=False)
    location = Column(String(100), nullable=False)
    image = Column(String(200))
    content = Column(TEXT)
    start_date_time = Column(DateTime(timezone=True))
    end_date_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
