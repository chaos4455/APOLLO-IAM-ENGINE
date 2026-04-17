from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base

user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
    Index("ix_user_roles_user_id", "user_id"),
    Index("ix_user_roles_role_id", "role_id"),
)

user_rbac_values = Table(
    "user_rbac_values", Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("attribute_id", String, ForeignKey("rbac_attributes.id"), primary_key=True),
    Column("value", String, nullable=False),
    Index("ix_user_rbac_values_user_id", "user_id"),
    Index("ix_user_rbac_values_attr_id", "attribute_id"),
)


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_is_active", "is_active"),
        Index("ix_users_group_id", "group_id"),
        Index("ix_users_type_level", "type_id", "level_id"),
    )
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False, index=True)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    type_id = Column(String, ForeignKey("user_types.id"), nullable=True)
    level_id = Column(String, ForeignKey("user_levels.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    roles = relationship("RoleModel", secondary=user_roles, back_populates="users",
                         lazy="select")
    group = relationship("GroupModel", back_populates="users", lazy="select")
    user_type = relationship("UserTypeModel", lazy="select")
    user_level = relationship("UserLevelModel", lazy="select")
