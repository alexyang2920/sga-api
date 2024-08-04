from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ..database import Base


class RoleEnum(PyEnum):
    Admin = "Admin"
    User = "User"
    Mentor = "Mentor"
    Volunteer = "Volunteer"


user_role_table = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(RoleEnum), nullable=False, unique=True)
    users = relationship('User', secondary=user_role_table, back_populates='roles')
