from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.rbac_attribute import RbacAttribute
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel


def _to_entity(m: RbacAttributeModel) -> RbacAttribute:
    return RbacAttribute(id=m.id, key=m.key, label=m.label,
                         value_type=m.value_type, description=m.description,
                         is_active=m.is_active, created_at=m.created_at)


class SqliteRbacAttributeRepository(RbacAttributeRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, attr: RbacAttribute) -> RbacAttribute:
        # upsert por key — evita UNIQUE constraint ao recriar com novo uuid
        existing = self.db.query(RbacAttributeModel).filter_by(key=attr.key).first()
        if existing:
            existing.label = attr.label
            existing.value_type = attr.value_type
            existing.description = attr.description
            existing.is_active = attr.is_active
            self.db.commit()
            return _to_entity(existing)
        m = self.db.query(RbacAttributeModel).filter_by(id=attr.id).first() or RbacAttributeModel(id=attr.id)
        m.key = attr.key
        m.label = attr.label
        m.value_type = attr.value_type
        m.description = attr.description
        m.is_active = attr.is_active
        self.db.merge(m)
        self.db.commit()
        return attr

    def find_by_id(self, attr_id: str) -> Optional[RbacAttribute]:
        m = self.db.query(RbacAttributeModel).filter_by(id=attr_id).first()
        return _to_entity(m) if m else None

    def find_by_key(self, key: str) -> Optional[RbacAttribute]:
        m = self.db.query(RbacAttributeModel).filter_by(key=key).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[RbacAttribute]:
        return [_to_entity(r) for r in self.db.query(RbacAttributeModel).all()]

    def delete(self, attr_id: str) -> None:
        m = self.db.query(RbacAttributeModel).filter_by(id=attr_id).first()
        if m:
            from sqlalchemy import text
            self.db.execute(text("DELETE FROM user_rbac_values WHERE attribute_id = :id"), {"id": attr_id})
            self.db.delete(m)
            self.db.commit()
