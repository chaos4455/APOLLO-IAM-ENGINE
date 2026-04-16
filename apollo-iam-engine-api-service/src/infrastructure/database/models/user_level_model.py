from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class UserLevelModel(Base):
    __tablename__ = "user_levels"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    rank = Column(Integer, default=0)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
