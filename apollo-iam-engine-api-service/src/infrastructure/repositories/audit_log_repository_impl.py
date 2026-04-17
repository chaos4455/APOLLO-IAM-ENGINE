from sqlalchemy.orm import Session
from sqlalchemy import text
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
        self.db.add(m)
        # flush sem commit — o commit é feito pelo caller ou no fechamento da sessão
        # isso evita um commit por evento em fluxos de múltiplos logs
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def list_logs(self, skip: int = 0, limit: int = 100,
                  actor: str | None = None, status: str | None = None) -> list[AuditLog]:
        # usa SQL direto para evitar ORM overhead em queries de listagem
        wheres = []
        params: dict = {"limit": limit, "skip": skip}
        if actor:
            wheres.append("actor = :actor")
            params["actor"] = actor
        if status:
            wheres.append("status = :status")
            params["status"] = status
        where_clause = f"WHERE {' AND '.join(wheres)}" if wheres else ""
        rows = self.db.execute(text(
            f"SELECT id, actor, action, resource, resource_id, detail, "
            f"ip_address, status, created_at FROM audit_logs "
            f"{where_clause} ORDER BY created_at DESC LIMIT :limit OFFSET :skip"
        ), params).fetchall()
        return [
            AuditLog(id=r[0], actor=r[1], action=r[2], resource=r[3],
                     resource_id=r[4], detail=r[5], ip_address=r[6],
                     status=r[7], created_at=r[8])
            for r in rows
        ]

    def count(self, actor: str | None = None, status: str | None = None) -> int:
        wheres = []
        params: dict = {}
        if actor:
            wheres.append("actor = :actor")
            params["actor"] = actor
        if status:
            wheres.append("status = :status")
            params["status"] = status
        where_clause = f"WHERE {' AND '.join(wheres)}" if wheres else ""
        return self.db.execute(
            text(f"SELECT COUNT(*) FROM audit_logs {where_clause}"), params
        ).scalar() or 0
