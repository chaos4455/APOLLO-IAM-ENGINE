from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.rbac_attribute_repository_impl import SqliteRbacAttributeRepository
from src.application.use_cases.rbac.create_attribute import CreateRbacAttributeUseCase
from src.application.use_cases.rbac.list_attributes import ListRbacAttributesUseCase
from src.application.use_cases.rbac.delete_attribute import DeleteRbacAttributeUseCase
from src.application.use_cases.rbac.assign_attribute_to_user import AssignAttributeToUserUseCase
from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, AssignAttributeDTO
from src.interface.api.schemas.rbac_schema import RbacAttributeCreate, RbacAttributeResponse, AssignAttributeRequest
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh
from src.infrastructure.cache.memory_cache import invalidate_user

router = APIRouter(prefix="/admin/rbac", tags=["Admin — RBAC Attributes"])


@router.get("/", response_model=list[RbacAttributeResponse])
def list_attrs(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [a.__dict__ for a in ListRbacAttributesUseCase(SqliteRbacAttributeRepository(db)).execute()]


@router.post("/", response_model=RbacAttributeResponse, status_code=201)
def create_attr(body: RbacAttributeCreate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    dto = CreateRbacAttributeDTO(key=body.key, label=body.label,
                                  value_type=body.value_type, description=body.description)
    result = CreateRbacAttributeUseCase(SqliteRbacAttributeRepository(db)).execute(dto)
    lh.log_rbac_attr_created(actor=getattr(actor, "sub", "admin"), attr_id=result.id, key=result.key)
    return result.__dict__


@router.delete("/{attr_id}", status_code=204)
def delete_attr(attr_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_rbac_attr_deleted(actor=getattr(actor, "sub", "admin"), attr_id=attr_id)
    DeleteRbacAttributeUseCase(SqliteRbacAttributeRepository(db)).execute(attr_id)


@router.post("/assign/{user_id}")
def assign_attr(user_id: str, body: AssignAttributeRequest, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    AssignAttributeToUserUseCase(db).execute(
        AssignAttributeDTO(user_id=user_id, attribute_key=body.attribute_key, value=body.value))
    lh.log_rbac_attr_assigned(actor=getattr(actor, "sub", "admin"),
                               user_id=user_id, key=body.attribute_key, value=body.value)
    invalidate_user(user_id)
    return {"message": "Atributo atribuído."}
