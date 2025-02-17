from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from database import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    full_name = Column(String, unique=False, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    primary_phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.ADMIN)
