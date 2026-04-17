from sqlalchemy import Column, String, DateTime, Index
from datetime import datetime
from src.infrastructure.database.base import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_actor_status", "actor", "status"),
        Index("ix_audit_logs_resource_status", "resource", "status"),
        Index("ix_audit_logs_created_desc", "created_at"),
    )
    id = Column(String, primary_key=True)
    actor = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    resource = Column(String, nullable=False, index=True)
    resource_id = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(String, default="success", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
