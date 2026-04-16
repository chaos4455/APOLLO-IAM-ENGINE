from sqlalchemy.orm import Session
from src.application.use_cases.settings.get_settings import GetSettingsUseCase
from src.application.use_cases.settings.update_settings import UpdateSettingsUseCase
from src.application.dtos.settings_dto import SettingsOutputDTO, UpdateSettingsDTO


class SettingsService:
    def __init__(self, db: Session):
        self._db = db

    def get(self) -> SettingsOutputDTO:
        return GetSettingsUseCase(self._db).execute()

    def update(self, dto: UpdateSettingsDTO) -> SettingsOutputDTO:
        return UpdateSettingsUseCase(self._db).execute(dto)
