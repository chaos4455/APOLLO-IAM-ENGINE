from sqlalchemy.orm import Session
from src.application.dtos.settings_dto import SettingsOutputDTO
from src.infrastructure.database.models.settings_model import SettingsModel


class GetSettingsUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self) -> SettingsOutputDTO:
        s = self.db.query(SettingsModel).filter_by(id="singleton").first()
        if not s:
            s = SettingsModel(id="singleton")
            self.db.add(s); self.db.commit()
        return SettingsOutputDTO(
            access_token_expire_minutes=s.access_token_expire_minutes,
            refresh_token_expire_days=s.refresh_token_expire_days,
            allow_registration=s.allow_registration,
            max_login_attempts=s.max_login_attempts,
            lockout_minutes=s.lockout_minutes,
        )
