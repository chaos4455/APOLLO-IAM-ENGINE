from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserCreatedEvent:
    user_id: str
    username: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)
