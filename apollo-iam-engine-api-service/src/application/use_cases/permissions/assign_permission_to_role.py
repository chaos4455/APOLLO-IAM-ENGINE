from sqlalchemy.orm import Session
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.database.models.permission_model import PermissionModel


class AssignPermissionToRoleUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, role_id: str, permission_id: str) -> None:
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        perm = self.db.query(PermissionModel).filter_by(id=permission_id).first()
        if role and perm and perm not in role.permissions:
            role.permissions.append(perm)
            self.db.commit()
