from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.role_model import role_permissions


class PermissionModel(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship("RoleModel", secondary=role_permissions, back_populates="permissions")
