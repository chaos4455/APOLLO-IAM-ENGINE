from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.application.use_cases.settings.get_settings import GetSettingsUseCase
from src.application.use_cases.settings.update_settings import UpdateSettingsUseCase
from src.application.dtos.settings_dto import UpdateSettingsDTO
from src.interface.api.schemas.settings_schema import SettingsResponse, SettingsUpdate
from src.interface.api.dependencies import require_superuser
from src.infrastructure.logging import log_hooks as lh
from src.infrastructure.cache.memory_cache import invalidate_settings

router = APIRouter(prefix="/admin/settings", tags=["Admin — Settings"])


@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db), actor=Depends(require_superuser)):
    lh.log_settings_read(actor=getattr(actor, "sub", "admin"))
    return GetSettingsUseCase(db).execute().__dict__


@router.put("/", response_model=SettingsResponse)
def update_settings(body: SettingsUpdate, db: Session = Depends(get_db), actor=Depends(require_superuser)):
    dto = UpdateSettingsDTO(**body.model_dump())
    result = UpdateSettingsUseCase(db).execute(dto)
    lh.log_settings_updated(actor=getattr(actor, "sub", "admin"), fields=body.model_dump())
    invalidate_settings()
    return result.__dict__
