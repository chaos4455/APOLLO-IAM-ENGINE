from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserUpdatedEvent:
    user_id: str
    changes: dict
    occurred_at: datetime = field(default_factory=datetime.utcnow)
