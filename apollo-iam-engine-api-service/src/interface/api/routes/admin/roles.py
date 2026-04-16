from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.role_repository_impl import SqliteRoleRepository
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.list_roles import ListRolesUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.roles.assign_role_to_user import AssignRoleToUserUseCase
from src.application.use_cases.roles.revoke_role_from_user import RevokeRoleFromUserUseCase
from src.application.dtos.role_dto import CreateRoleDTO
from src.interface.api.schemas.role_schema import RoleCreate, RoleResponse, AssignRoleRequest
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh
from src.infrastructure.cache.memory_cache import invalidate_user, user_enrichment_cache

router = APIRouter(prefix="/admin/roles", tags=["Admin — Roles"])


@router.get("/", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db), actor=Depends(require_superuser)):
    return [r.__dict__ for r in ListRolesUseCase(SqliteRoleRepository(db)).execute()]


@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(body: RoleCreate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    result = CreateRoleUseCase(SqliteRoleRepository(db)).execute(
        CreateRoleDTO(name=body.name, description=body.description))
    lh.log_role_created(actor=getattr(actor, "sub", "admin"), role_id=result.id, name=result.name)
    return result.__dict__


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_role_deleted(actor=getattr(actor, "sub", "admin"), role_id=role_id)
    DeleteRoleUseCase(SqliteRoleRepository(db)).execute(role_id)


@router.post("/{role_id}/assign-user/{user_id}")
def assign_role(role_id: str, user_id: str, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    AssignRoleToUserUseCase(db).execute(user_id, role_id)
    lh.log_role_assigned(actor=getattr(actor, "sub", "admin"), user_id=user_id, role_id=role_id)
    invalidate_user(user_id)  # invalida cache de enriquecimento
    return {"message": "Role atribuída."}


@router.delete("/{role_id}/revoke-user/{user_id}")
def revoke_role(role_id: str, user_id: str, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    RevokeRoleFromUserUseCase(db).execute(user_id, role_id)
    lh.log_role_revoked(actor=getattr(actor, "sub", "admin"), user_id=user_id, role_id=role_id)
    invalidate_user(user_id)  # invalida cache de enriquecimento
    return {"message": "Role revogada."}
