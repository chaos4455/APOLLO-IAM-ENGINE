from sqlalchemy.orm import Session
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.config.constants import DEFAULT_ROLES
import uuid


def seed_roles(db: Session):
    for name in DEFAULT_ROLES:
        if not db.query(RoleModel).filter_by(name=name).first():
            db.add(RoleModel(id=str(uuid.uuid4()), name=name, description=f"Role {name}"))
    db.commit()
