from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.infrastructure.database.connection import get_db
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/audit", tags=["Admin — Audit Logs"])


@router.get("/")
def list_logs(
    skip: int = 0,
    limit: int = 100,
    actor: str = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
    _=Depends(require_superuser),
):
    """
    Lista logs de auditoria. Lê preferencialmente do event_log (apollo_log.db)
    com fallback para audit_logs (banco principal).
    Suporta filtros por actor e status.
    """
    from src.infrastructure.logging.event_logger import _log_engine

    try:
        wheres = []
        params: dict = {"limit": limit, "skip": skip}
        if actor:
            wheres.append("actor = :actor")
            params["actor"] = actor
        if status:
            wheres.append("status = :status")
            params["status"] = status
        where_clause = f"WHERE {' AND '.join(wheres)}" if wheres else ""

        with _log_engine.connect() as conn:
            total = conn.execute(
                text(f"SELECT COUNT(*) FROM event_log {where_clause}"), params
            ).scalar() or 0
            rows = conn.execute(text(
                f"SELECT seq, uid, timestamp, event, actor, resource, resource_id, "
                f"tenant_id, session_id, status, duration_ms, tags, detail "
                f"FROM event_log {where_clause} ORDER BY seq DESC LIMIT :limit OFFSET :skip"
            ), params).fetchall()

        return [
            {
                "id":          str(r[0]),
                "actor":       r[4],
                "action":      r[3],
                "resource":    r[5],
                "resource_id": r[6],
                "ip_address":  None,
                "status":      r[9],
                "created_at":  r[2],
                "detail":      r[12],
                "uid":         r[1],
                "tenant_id":   r[7],
                "session_id":  r[8],
                "duration_ms": r[10],
                "tags":        r[11],
            }
            for r in rows
        ]
    except Exception:
        # fallback para audit_logs do banco principal
        wheres = []
        params = {"limit": limit, "skip": skip}
        if actor:
            wheres.append("actor = :actor")
            params["actor"] = actor
        if status:
            wheres.append("status = :status")
            params["status"] = status
        where_clause = f"WHERE {' AND '.join(wheres)}" if wheres else ""

        rows = db.execute(text(
            f"SELECT id, actor, action, resource, resource_id, detail, "
            f"ip_address, status, created_at FROM audit_logs "
            f"{where_clause} ORDER BY created_at DESC LIMIT :limit OFFSET :skip"
        ), params).fetchall()
        return [
            {"id": r[0], "actor": r[1], "action": r[2], "resource": r[3],
             "resource_id": r[4], "detail": r[5], "ip_address": r[6],
             "status": r[7], "created_at": str(r[8])}
            for r in rows
        ]
