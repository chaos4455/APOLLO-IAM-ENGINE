from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.role_model import role_permissions


class PermissionModel(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        Index("ix_permissions_resource_action", "resource", "action"),
    )
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    resource = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False, index=True)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship("RoleModel", secondary=role_permissions, back_populates="permissions")
