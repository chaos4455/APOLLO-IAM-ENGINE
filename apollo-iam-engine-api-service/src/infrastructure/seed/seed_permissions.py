from sqlalchemy.orm import Session
from src.infrastructure.database.models.permission_model import PermissionModel
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.config.constants import DEFAULT_PERMISSIONS
import uuid


def seed_permissions(db: Session):
    for name, resource, action in DEFAULT_PERMISSIONS:
        if not db.query(PermissionModel).filter_by(name=name).first():
            db.add(PermissionModel(id=str(uuid.uuid4()), name=name,
                                   resource=resource, action=action))
    db.commit()
    # superadmin gets all permissions
    superadmin = db.query(RoleModel).filter_by(name="superadmin").first()
    if superadmin:
        all_perms = db.query(PermissionModel).all()
        for p in all_perms:
            if p not in superadmin.permissions:
                superadmin.permissions.append(p)
        db.commit()
