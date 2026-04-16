from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.group_repository_impl import SqliteGroupRepository
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.use_cases.groups.list_groups import ListGroupsUseCase
from src.application.use_cases.groups.delete_group import DeleteGroupUseCase
from src.application.use_cases.groups.assign_user_to_group import AssignUserToGroupUseCase
from src.application.dtos.group_dto import CreateGroupDTO
from src.interface.api.schemas.group_schema import GroupCreate, GroupResponse
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh

router = APIRouter(prefix="/admin/groups", tags=["Admin — Groups"])


@router.get("/", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [g.__dict__ for g in ListGroupsUseCase(SqliteGroupRepository(db)).execute()]


@router.post("/", response_model=GroupResponse, status_code=201)
def create_group(body: GroupCreate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    result = CreateGroupUseCase(SqliteGroupRepository(db)).execute(
        CreateGroupDTO(name=body.name, description=body.description))
    lh.log_group_created(actor=getattr(actor, "sub", "admin"), group_id=result.id, name=result.name)
    return result.__dict__


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_group_deleted(actor=getattr(actor, "sub", "admin"), group_id=group_id)
    DeleteGroupUseCase(SqliteGroupRepository(db)).execute(group_id)


@router.post("/{group_id}/assign-user/{user_id}")
def assign_user(group_id: str, user_id: str, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    AssignUserToGroupUseCase(db).execute(user_id, group_id)
    lh.log_user_assigned_to_group(actor=getattr(actor, "sub", "admin"), user_id=user_id, group_id=group_id)
    return {"message": "Usuário adicionado ao grupo."}
