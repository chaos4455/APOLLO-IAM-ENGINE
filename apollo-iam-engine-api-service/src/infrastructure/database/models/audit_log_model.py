from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(String, default="success")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
