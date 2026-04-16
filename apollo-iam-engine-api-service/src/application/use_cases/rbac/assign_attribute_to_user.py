from sqlalchemy.orm import Session
from src.application.dtos.rbac_dto import AssignAttributeDTO
from src.infrastructure.database.models.user_model import UserModel, user_rbac_values
from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel
from sqlalchemy import insert, delete


class AssignAttributeToUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, dto: AssignAttributeDTO) -> None:
        attr = self.db.query(RbacAttributeModel).filter_by(key=dto.attribute_key).first()
        if not attr:
            return
        self.db.execute(
            delete(user_rbac_values).where(
                user_rbac_values.c.user_id == dto.user_id,
                user_rbac_values.c.attribute_id == attr.id,
            )
        )
        self.db.execute(
            insert(user_rbac_values).values(
                user_id=dto.user_id, attribute_id=attr.id, value=dto.value
            )
        )
        self.db.commit()
