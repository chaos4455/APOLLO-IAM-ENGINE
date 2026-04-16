from dataclasses import dataclass
from typing import Optional


@dataclass
class AuditLogOutputDTO:
    id: str
    actor: str
    action: str
    resource: str
    resource_id: Optional[str]
    detail: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: str
