from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel


class AssignRoleToUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: str, role_id: str) -> None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        if user and role and role not in user.roles:
            user.roles.append(role)
            self.db.commit()
