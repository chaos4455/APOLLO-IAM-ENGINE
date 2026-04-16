from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LoginFailedEvent:
    username: str
    reason: str
    ip: str = ''
    occurred_at: datetime = field(default_factory=datetime.utcnow)
