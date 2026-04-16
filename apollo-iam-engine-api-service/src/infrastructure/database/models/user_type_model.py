from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class UserTypeModel(Base):
    __tablename__ = "user_types"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
