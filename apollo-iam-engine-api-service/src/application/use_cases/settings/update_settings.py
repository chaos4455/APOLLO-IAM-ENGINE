from sqlalchemy.orm import Session
from src.application.dtos.settings_dto import UpdateSettingsDTO, SettingsOutputDTO
from src.infrastructure.database.models.settings_model import SettingsModel


class UpdateSettingsUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, dto: UpdateSettingsDTO) -> SettingsOutputDTO:
        s = self.db.query(SettingsModel).filter_by(id="singleton").first()
        if not s:
            s = SettingsModel(id="singleton")
            self.db.add(s)
        if dto.access_token_expire_minutes is not None:
            s.access_token_expire_minutes = dto.access_token_expire_minutes
        if dto.refresh_token_expire_days is not None:
            s.refresh_token_expire_days = dto.refresh_token_expire_days
        if dto.allow_registration is not None:
            s.allow_registration = dto.allow_registration
        if dto.max_login_attempts is not None:
            s.max_login_attempts = dto.max_login_attempts
        if dto.lockout_minutes is not None:
            s.lockout_minutes = dto.lockout_minutes
        self.db.commit()
        from src.application.use_cases.settings.get_settings import GetSettingsUseCase
        return GetSettingsUseCase(self.db).execute()
