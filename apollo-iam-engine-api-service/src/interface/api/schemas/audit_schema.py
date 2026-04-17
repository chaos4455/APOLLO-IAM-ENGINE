from pydantic import BaseModel
from typing import Optional


class AuditLogResponse(BaseModel):
    id: str
    actor: str
    action: str
    resource: str
    resource_id: Optional[str] = None
    detail: Optional[str] = None
    ip_address: Optional[str] = None
    status: str
    created_at: str
    # campos extras do event_log (presentes quando lendo do apollo_log.db)
    uid: Optional[str] = None
    tenant_id: Optional[str] = None
    session_id: Optional[str] = None
    duration_ms: Optional[str] = None
    tags: Optional[str] = None
