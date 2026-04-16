from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Group:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
