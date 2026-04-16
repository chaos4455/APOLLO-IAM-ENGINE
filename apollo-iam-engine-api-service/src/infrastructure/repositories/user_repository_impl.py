from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.database.models.user_model import UserModel


def _to_entity(m: UserModel) -> User:
    u = User(
        id=m.id, username=m.username, email=m.email,
        hashed_password=m.hashed_password, full_name=m.full_name,
        is_active=m.is_active, is_superuser=m.is_superuser,
        group_id=m.group_id, type_id=m.type_id, level_id=m.level_id,
        created_at=m.created_at, updated_at=m.updated_at,
        roles=[r.name for r in m.roles],
    )
    return u


def _to_model(u: User, db: Session) -> UserModel:
    m = db.query(UserModel).filter_by(id=u.id).first() or UserModel(id=u.id)
    m.username = u.username
    m.email = u.email
    m.hashed_password = u.hashed_password
    m.full_name = u.full_name
    m.is_active = u.is_active
    m.is_superuser = u.is_superuser
    m.group_id = u.group_id
    m.type_id = u.type_id
    m.level_id = u.level_id
    m.created_at = u.created_at
    m.updated_at = u.updated_at
    return m


class SqliteUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        m = _to_model(user, self.db)
        self.db.merge(m)
        self.db.commit()
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(id=user_id).first()
        return _to_entity(m) if m else None

    def find_by_username(self, username: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(username=username).first()
        return _to_entity(m) if m else None

    def find_by_email(self, email: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(email=email).first()
        return _to_entity(m) if m else None

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        rows = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [_to_entity(r) for r in rows]

    def delete(self, user_id: str) -> None:
        m = self.db.query(UserModel).filter_by(id=user_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()

    def count(self) -> int:
        return self.db.query(UserModel).count()
