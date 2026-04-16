from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class TokenBlacklistModel(Base):
    __tablename__ = "token_blacklist"
    jti = Column(String, primary_key=True)
    revoked_at = Column(DateTime, default=datetime.utcnow)
