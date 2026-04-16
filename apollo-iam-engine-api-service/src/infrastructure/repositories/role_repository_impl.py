from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.role import Role
from src.domain.ports.role_repository import RoleRepository
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.database.models.permission_model import PermissionModel


def _to_entity(m: RoleModel) -> Role:
    return Role(
        id=m.id, name=m.name, description=m.description,
        is_active=m.is_active, created_at=m.created_at,
        permissions=[p.name for p in m.permissions],
    )


class SqliteRoleRepository(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, role: Role) -> Role:
        # upsert por name — evita UNIQUE constraint ao recriar com novo uuid
        existing = self.db.query(RoleModel).filter_by(name=role.name).first()
        if existing:
            existing.description = role.description
            existing.is_active = role.is_active
            self.db.commit()
            return _to_entity(existing)
        m = self.db.query(RoleModel).filter_by(id=role.id).first() or RoleModel(id=role.id)
        m.name = role.name
        m.description = role.description
        m.is_active = role.is_active
        self.db.merge(m)
        self.db.commit()
        return role

    def find_by_id(self, role_id: str) -> Optional[Role]:
        m = self.db.query(RoleModel).filter_by(id=role_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Role]:
        m = self.db.query(RoleModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Role]:
        return [_to_entity(r) for r in self.db.query(RoleModel).all()]

    def delete(self, role_id: str) -> None:
        m = self.db.query(RoleModel).filter_by(id=role_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()

    def assign_permission(self, role_id: str, permission_id: str) -> None:
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        perm = self.db.query(PermissionModel).filter_by(id=permission_id).first()
        if role and perm and perm not in role.permissions:
            role.permissions.append(perm)
            self.db.commit()
