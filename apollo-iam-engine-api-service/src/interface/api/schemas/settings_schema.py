from pydantic import BaseModel
from typing import Optional


class SettingsResponse(BaseModel):
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    allow_registration: bool
    max_login_attempts: int
    lockout_minutes: int

class SettingsUpdate(BaseModel):
    access_token_expire_minutes: Optional[int] = None
    refresh_token_expire_days: Optional[int] = None
    allow_registration: Optional[bool] = None
    max_login_attempts: Optional[int] = None
    lockout_minutes: Optional[int] = None
