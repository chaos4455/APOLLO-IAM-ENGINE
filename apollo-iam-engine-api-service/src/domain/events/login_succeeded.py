from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LoginSucceededEvent:
    user_id: str
    username: str
    ip: str = ''
    occurred_at: datetime = field(default_factory=datetime.utcnow)
