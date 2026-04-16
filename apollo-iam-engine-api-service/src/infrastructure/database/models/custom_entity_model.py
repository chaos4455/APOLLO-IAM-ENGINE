from __future__ import annotations
from sqlalchemy import Column, String, Boolean, DateTime, Text, UniqueConstraint
from datetime import datetime
from src.infrastructure.database.base import Base


class CustomEntityTypeModel(Base):
    """Define um tipo de entidade customizada. Ex: 'cargo', 'setor', 'contrato'."""
    __tablename__ = "custom_entity_types"
    id          = Column(String, primary_key=True)
    slug        = Column(String, unique=True, nullable=False, index=True)  # ex: "cargo"
    label       = Column(String, nullable=False)                           # ex: "Cargo"
    description = Column(String, default="")
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)


class CustomEntityValueModel(Base):
    """Valor de uma entidade customizada. Ex: tipo='cargo', value='Analista'."""
    __tablename__ = "custom_entity_values"
    __table_args__ = (
        UniqueConstraint("entity_type_slug", "name", name="uq_entity_type_name"),
    )
    id               = Column(String, primary_key=True)
    entity_type_slug = Column(String, nullable=False, index=True)
    name             = Column(String, nullable=False)
    description      = Column(String, default="")
    metadata_json    = Column(Text, default="{}")   # JSON livre para dados extras
    is_active        = Column(Boolean, default=True)
    created_at       = Column(DateTime, default=datetime.utcnow)


class UserCustomEntityModel(Base):
    """Associa um usuario a um valor de entidade customizada."""
    __tablename__ = "user_custom_entities"
    __table_args__ = (
        UniqueConstraint("user_id", "entity_type_slug", name="uq_user_entity_type"),
    )
    id               = Column(String, primary_key=True)
    user_id          = Column(String, nullable=False, index=True)
    entity_type_slug = Column(String, nullable=False)
    entity_value_id  = Column(String, nullable=False)
    assigned_at      = Column(DateTime, default=datetime.utcnow)
