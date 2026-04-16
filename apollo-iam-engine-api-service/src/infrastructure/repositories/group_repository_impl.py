from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.group import Group
from src.domain.ports.group_repository import GroupRepository
from src.infrastructure.database.models.group_model import GroupModel


def _to_entity(m: GroupModel) -> Group:
    return Group(id=m.id, name=m.name, description=m.description,
                 is_active=m.is_active, created_at=m.created_at)


class SqliteGroupRepository(GroupRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, group: Group) -> Group:
        # upsert por name — evita UNIQUE constraint ao recriar com novo uuid
        existing = self.db.query(GroupModel).filter_by(name=group.name).first()
        if existing:
            existing.description = group.description
            existing.is_active = group.is_active
            self.db.commit()
            return _to_entity(existing)
        m = self.db.query(GroupModel).filter_by(id=group.id).first() or GroupModel(id=group.id)
        m.name = group.name
        m.description = group.description
        m.is_active = group.is_active
        self.db.merge(m)
        self.db.commit()
        return group

    def find_by_id(self, group_id: str) -> Optional[Group]:
        m = self.db.query(GroupModel).filter_by(id=group_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Group]:
        m = self.db.query(GroupModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Group]:
        return [_to_entity(r) for r in self.db.query(GroupModel).all()]

    def delete(self, group_id: str) -> None:
        m = self.db.query(GroupModel).filter_by(id=group_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()
