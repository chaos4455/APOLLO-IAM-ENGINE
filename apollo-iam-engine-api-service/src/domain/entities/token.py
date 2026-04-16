from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime = None
