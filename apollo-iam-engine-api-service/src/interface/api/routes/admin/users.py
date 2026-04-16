from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.use_cases.users.update_user import UpdateUserUseCase
from src.application.use_cases.users.delete_user import DeleteUserUseCase
from src.application.use_cases.users.get_user import GetUserUseCase
from src.application.use_cases.users.list_users import ListUsersUseCase
from src.application.use_cases.users.reset_password import ResetPasswordUseCase
from src.application.use_cases.users.toggle_user_status import ToggleUserStatusUseCase
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.interface.api.schemas.user_schema import (
    UserCreate, UserUpdate, UserResponse, ChangePasswordRequest, ResetPasswordRequest
)
from src.interface.api.dependencies import require_superuser
from src.domain.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from src.infrastructure.logging import log_hooks as lh
from src.infrastructure.cache.memory_cache import invalidate_user, db_kpis_cache

router = APIRouter(prefix="/admin/users", tags=["Admin — Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               _=Depends(require_superuser)):
    return [u.__dict__ for u in ListUsersUseCase(SqliteUserRepository(db)).execute(skip, limit)]


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    try:
        dto = CreateUserDTO(**body.model_dump())
        result = CreateUserUseCase(SqliteUserRepository(db), BcryptPasswordHasher()).execute(dto)
        lh.log_user_created(actor=getattr(actor, "sub", "admin"),
                             user_id=result.id, username=result.username)
        db_kpis_cache.clear()
        return result.__dict__
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    try:
        return GetUserUseCase(SqliteUserRepository(db)).execute(user_id).__dict__
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UserUpdate, db: Session = Depends(get_db),
                actor=Depends(require_superuser)):
    dto = UpdateUserDTO(user_id=user_id, **body.model_dump())
    result = UpdateUserUseCase(SqliteUserRepository(db)).execute(dto)
    lh.log_user_updated(actor=getattr(actor, "sub", "admin"),
                         user_id=user_id, fields=list(body.model_dump().keys()))
    invalidate_user(user_id)
    return result.__dict__


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_user_deleted(actor=getattr(actor, "sub", "admin"), user_id=user_id)
    DeleteUserUseCase(SqliteUserRepository(db)).execute(user_id)
    invalidate_user(user_id)
    db_kpis_cache.clear()


@router.post("/{user_id}/toggle-status")
def toggle_status(user_id: str, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    active = ToggleUserStatusUseCase(SqliteUserRepository(db)).execute(user_id)
    lh.log_user_toggled(actor=getattr(actor, "sub", "admin"), user_id=user_id, new_status=active)
    invalidate_user(user_id)
    return {"is_active": active}


@router.post("/{user_id}/reset-password")
def reset_password(user_id: str, body: ResetPasswordRequest, db: Session = Depends(get_db),
                   actor=Depends(require_superuser)):
    ResetPasswordUseCase(SqliteUserRepository(db), BcryptPasswordHasher()).execute(
        user_id, body.new_password)
    lh.log_password_reset(actor=getattr(actor, "sub", "admin"), user_id=user_id)
    invalidate_user(user_id)
    return {"message": "Senha redefinida."}
