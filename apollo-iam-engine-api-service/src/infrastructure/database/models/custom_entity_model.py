from __future__ import annotations
from sqlalchemy import Column, String, Boolean, DateTime, Text, UniqueConstraint, Index
from datetime import datetime
from src.infrastructure.database.base import Base


class CustomEntityTypeModel(Base):
    __tablename__ = "custom_entity_types"
    id          = Column(String, primary_key=True)
    slug        = Column(String, unique=True, nullable=False, index=True)
    label       = Column(String, nullable=False)
    description = Column(String, default="")
    is_active   = Column(Boolean, default=True, index=True)
    created_at  = Column(DateTime, default=datetime.utcnow)


class CustomEntityValueModel(Base):
    __tablename__ = "custom_entity_values"
    __table_args__ = (
        UniqueConstraint("entity_type_slug", "name", name="uq_entity_type_name"),
        Index("ix_custom_entity_values_slug_active", "entity_type_slug", "is_active"),
    )
    id               = Column(String, primary_key=True)
    entity_type_slug = Column(String, nullable=False, index=True)
    name             = Column(String, nullable=False)
    description      = Column(String, default="")
    metadata_json    = Column(Text, default="{}")
    is_active        = Column(Boolean, default=True)
    created_at       = Column(DateTime, default=datetime.utcnow)


class UserCustomEntityModel(Base):
    __tablename__ = "user_custom_entities"
    __table_args__ = (
        UniqueConstraint("user_id", "entity_type_slug", name="uq_user_entity_type"),
        Index("ix_user_custom_entities_user_slug", "user_id", "entity_type_slug"),
    )
    id               = Column(String, primary_key=True)
    user_id          = Column(String, nullable=False, index=True)
    entity_type_slug = Column(String, nullable=False, index=True)
    entity_value_id  = Column(String, nullable=False)
    assigned_at      = Column(DateTime, default=datetime.utcnow)
