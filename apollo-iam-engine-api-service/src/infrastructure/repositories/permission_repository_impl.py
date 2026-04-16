from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.permission import Permission
from src.domain.ports.permission_repository import PermissionRepository
from src.infrastructure.database.models.permission_model import PermissionModel


def _to_entity(m: PermissionModel) -> Permission:
    return Permission(id=m.id, name=m.name, resource=m.resource,
                      action=m.action, description=m.description, created_at=m.created_at)


class SqlitePermissionRepository(PermissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, perm: Permission) -> Permission:
        # upsert por name — evita UNIQUE constraint ao recriar com novo uuid
        existing = self.db.query(PermissionModel).filter_by(name=perm.name).first()
        if existing:
            existing.resource = perm.resource
            existing.action = perm.action
            existing.description = perm.description
            self.db.commit()
            return _to_entity(existing)
        m = self.db.query(PermissionModel).filter_by(id=perm.id).first() or PermissionModel(id=perm.id)
        m.name = perm.name
        m.resource = perm.resource
        m.action = perm.action
        m.description = perm.description
        self.db.merge(m)
        self.db.commit()
        return perm

    def find_by_id(self, perm_id: str) -> Optional[Permission]:
        m = self.db.query(PermissionModel).filter_by(id=perm_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Permission]:
        m = self.db.query(PermissionModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Permission]:
        return [_to_entity(r) for r in self.db.query(PermissionModel).all()]

    def delete(self, perm_id: str) -> None:
        m = self.db.query(PermissionModel).filter_by(id=perm_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()
