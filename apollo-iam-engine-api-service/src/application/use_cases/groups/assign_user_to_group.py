from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel


class AssignUserToGroupUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: str, group_id: str) -> None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user:
            user.group_id = group_id
            self.db.commit()
