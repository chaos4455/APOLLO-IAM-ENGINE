from sqlalchemy import Column, String, Boolean, DateTime, Table, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.user_model import user_roles

role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", String, ForeignKey("permissions.id"), primary_key=True),
    Index("ix_role_permissions_role_id", "role_id"),
    Index("ix_role_permissions_perm_id", "permission_id"),
)


class RoleModel(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, default="")
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("UserModel", secondary=user_roles, back_populates="roles",
                         lazy="select")
    permissions = relationship("PermissionModel", secondary=role_permissions,
                               back_populates="roles", lazy="select")
