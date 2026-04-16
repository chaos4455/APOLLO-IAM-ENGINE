from pydantic import BaseModel
from typing import Optional


class AuditLogResponse(BaseModel):
    id: str
    actor: str
    action: str
    resource: str
    resource_id: Optional[str]
    detail: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: str
