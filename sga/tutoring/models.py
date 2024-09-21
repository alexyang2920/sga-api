from sqlalchemy import DateTime, Column, Integer, String, Boolean, func

from ..database import Base


class TutoringProgram(Base):
    __tablename__ = "tutoring_program"

    id = Column(Integer, primary_key=True, autoincrement='auto')
    title = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
