from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: Optional[str] = None
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    roles: list = field(default_factory=list)
    rbac_attributes: dict = field(default_factory=dict)

    def touch(self):
        self.updated_at = datetime.utcnow()
