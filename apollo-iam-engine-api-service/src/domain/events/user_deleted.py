from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserDeletedEvent:
    user_id: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)
