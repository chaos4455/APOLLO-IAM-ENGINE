from sqlalchemy.orm import Session
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.application.dtos.audit_dto import AuditLogOutputDTO


class AuditService:
    def __init__(self, db: Session):
        self._repo = SqliteAuditLogRepository(db)

    def list_logs(self, skip: int = 0, limit: int = 100) -> list[AuditLogOutputDTO]:
        return [
            AuditLogOutputDTO(
                id=l.id, actor=l.actor, action=l.action, resource=l.resource,
                resource_id=l.resource_id, detail=l.detail, ip_address=l.ip_address,
                status=l.status, created_at=str(l.created_at),
            )
            for l in self._repo.list_logs(skip, limit)
        ]
