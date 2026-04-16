from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class SettingsModel(Base):
    __tablename__ = "settings"
    id = Column(String, primary_key=True, default="singleton")
    access_token_expire_minutes = Column(Integer, default=60)
    refresh_token_expire_days = Column(Integer, default=7)
    allow_registration = Column(Boolean, default=False)
    max_login_attempts = Column(Integer, default=5)
    lockout_minutes = Column(Integer, default=15)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
