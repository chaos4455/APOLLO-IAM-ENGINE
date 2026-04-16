from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class AuditLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    actor: str = ""
    action: str = ""
    resource: str = ""
    resource_id: Optional[str] = None
    detail: Optional[str] = None
    ip_address: Optional[str] = None
    status: str = "success"
    created_at: datetime = field(default_factory=datetime.utcnow)
