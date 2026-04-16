from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class UserType:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
