from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class UserLevel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    rank: int = 0
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
