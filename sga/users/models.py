from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from ..roles.models import user_role_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, index=True)
    name = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    # need to be eagar loading, otherwise it failed in routers.
    roles = relationship("Role", secondary=user_role_table, back_populates="users", lazy='joined')
