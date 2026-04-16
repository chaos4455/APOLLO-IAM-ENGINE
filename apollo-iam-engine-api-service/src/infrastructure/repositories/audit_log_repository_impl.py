from sqlalchemy.orm import Session
from src.domain.entities.audit_log import AuditLog
from src.domain.ports.audit_logger import AuditLogger
from src.infrastructure.database.models.audit_log_model import AuditLogModel


def _to_entity(m: AuditLogModel) -> AuditLog:
    return AuditLog(id=m.id, actor=m.actor, action=m.action, resource=m.resource,
                    resource_id=m.resource_id, detail=m.detail, ip_address=m.ip_address,
                    status=m.status, created_at=m.created_at)


class SqliteAuditLogRepository(AuditLogger):
    def __init__(self, db: Session):
        self.db = db

    def log(self, entry: AuditLog) -> None:
        m = AuditLogModel(
            id=entry.id, actor=entry.actor, action=entry.action,
            resource=entry.resource, resource_id=entry.resource_id,
            detail=entry.detail, ip_address=entry.ip_address,
            status=entry.status, created_at=entry.created_at,
        )
        self.db.add(m); self.db.commit()

    def list_logs(self, skip: int = 0, limit: int = 100) -> list[AuditLog]:
        rows = (self.db.query(AuditLogModel)
                .order_by(AuditLogModel.created_at.desc())
                .offset(skip).limit(limit).all())
        return [_to_entity(r) for r in rows]
