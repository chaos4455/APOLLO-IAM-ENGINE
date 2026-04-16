from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.interface.api.schemas.audit_schema import AuditLogResponse
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/audit", tags=["Admin — Audit Logs"])


@router.get("/", response_model=list[AuditLogResponse])
def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
              _=Depends(require_superuser)):
    repo = SqliteAuditLogRepository(db)
    return [{"id": l.id, "actor": l.actor, "action": l.action, "resource": l.resource,
             "resource_id": l.resource_id, "detail": l.detail, "ip_address": l.ip_address,
             "status": l.status, "created_at": str(l.created_at)}
            for l in repo.list_logs(skip, limit)]
