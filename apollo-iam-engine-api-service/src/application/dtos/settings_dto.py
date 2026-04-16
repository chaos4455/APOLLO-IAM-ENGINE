from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SettingsOutputDTO:
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    allow_registration: bool
    max_login_attempts: int
    lockout_minutes: int


@dataclass
class UpdateSettingsDTO:
    access_token_expire_minutes: int | None = None
    refresh_token_expire_days: int | None = None
    allow_registration: bool | None = None
    max_login_attempts: int | None = None
    lockout_minutes: int | None = None
