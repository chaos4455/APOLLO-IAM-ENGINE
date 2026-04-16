from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.permission_repository_impl import SqlitePermissionRepository
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.permissions.list_permissions import ListPermissionsUseCase
from src.application.use_cases.permissions.delete_permission import DeletePermissionUseCase
from src.application.use_cases.permissions.assign_permission_to_role import AssignPermissionToRoleUseCase
from src.application.dtos.permission_dto import CreatePermissionDTO
from src.interface.api.schemas.permission_schema import PermissionCreate, PermissionResponse, AssignPermissionRequest
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh

router = APIRouter(prefix="/admin/permissions", tags=["Admin — Permissions"])


@router.get("/", response_model=list[PermissionResponse])
def list_perms(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [p.__dict__ for p in ListPermissionsUseCase(SqlitePermissionRepository(db)).execute()]


@router.post("/", response_model=PermissionResponse, status_code=201)
def create_perm(body: PermissionCreate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    dto = CreatePermissionDTO(name=body.name, resource=body.resource,
                              action=body.action, description=body.description)
    result = CreatePermissionUseCase(SqlitePermissionRepository(db)).execute(dto)
    lh.log_permission_created(actor=getattr(actor, "sub", "admin"), perm_id=result.id, name=result.name)
    return result.__dict__


@router.delete("/{perm_id}", status_code=204)
def delete_perm(perm_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_permission_deleted(actor=getattr(actor, "sub", "admin"), perm_id=perm_id)
    DeletePermissionUseCase(SqlitePermissionRepository(db)).execute(perm_id)


@router.post("/{perm_id}/assign-role/{role_id}")
def assign_perm(perm_id: str, role_id: str, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    AssignPermissionToRoleUseCase(db).execute(role_id, perm_id)
    lh.log_permission_assigned_to_role(actor=getattr(actor, "sub", "admin"), perm_id=perm_id, role_id=role_id)
    return {"message": "Permissão atribuída."}
