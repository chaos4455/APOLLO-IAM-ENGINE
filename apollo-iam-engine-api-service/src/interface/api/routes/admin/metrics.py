"""
metrics.py
Rota /admin/metrics — KPIs, métricas de sistema e logs recentes.
"""
from __future__ import annotations
import os, time, platform
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.interface.api.dependencies import require_superuser

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False

router = APIRouter(prefix="/admin/metrics", tags=["Admin — Metrics"])

_START_TIME = time.time()


def _cpu() -> dict:
    if not _HAS_PSUTIL:
        return {"percent": 0, "count_logical": os.cpu_count() or 1, "count_physical": 0}
    return {
        "percent":        psutil.cpu_percent(interval=0.1),
        "count_logical":  psutil.cpu_count(logical=True),
        "count_physical": psutil.cpu_count(logical=False) or 0,
        "freq_mhz":       round(psutil.cpu_freq().current, 1) if psutil.cpu_freq() else 0,
        "per_core":       psutil.cpu_percent(interval=0.1, percpu=True),
    }


def _memory() -> dict:
    if not _HAS_PSUTIL:
        return {}
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "total_mb":     round(vm.total / 1024**2, 1),
        "used_mb":      round(vm.used  / 1024**2, 1),
        "available_mb": round(vm.available / 1024**2, 1),
        "percent":      vm.percent,
        "swap_total_mb": round(sw.total / 1024**2, 1),
        "swap_used_mb":  round(sw.used  / 1024**2, 1),
        "swap_percent":  sw.percent,
    }


def _disk() -> dict:
    if not _HAS_PSUTIL:
        return {}
    try:
        d = psutil.disk_usage(".")
        io = psutil.disk_io_counters()
        return {
            "total_gb":   round(d.total / 1024**3, 2),
            "used_gb":    round(d.used  / 1024**3, 2),
            "free_gb":    round(d.free  / 1024**3, 2),
            "percent":    d.percent,
            "read_mb":    round(io.read_bytes  / 1024**2, 1) if io else 0,
            "write_mb":   round(io.write_bytes / 1024**2, 1) if io else 0,
            "read_count": io.read_count  if io else 0,
            "write_count":io.write_count if io else 0,
        }
    except Exception:
        return {}


def _network() -> dict:
    if not _HAS_PSUTIL:
        return {}
    try:
        net = psutil.net_io_counters()
        conns = psutil.net_connections()
        return {
            "bytes_sent_mb":   round(net.bytes_sent / 1024**2, 2),
            "bytes_recv_mb":   round(net.bytes_recv / 1024**2, 2),
            "packets_sent":    net.packets_sent,
            "packets_recv":    net.packets_recv,
            "errors_in":       net.errin,
            "errors_out":      net.errout,
            "drop_in":         net.dropin,
            "drop_out":        net.dropout,
            "active_connections": len([c for c in conns if c.status == "ESTABLISHED"]),
            "total_connections":  len(conns),
        }
    except Exception:
        return {}


def _process() -> dict:
    if not _HAS_PSUTIL:
        return {}
    try:
        p = psutil.Process(os.getpid())
        with p.oneshot():
            return {
                "pid":          p.pid,
                "cpu_percent":  p.cpu_percent(interval=0.1),
                "mem_rss_mb":   round(p.memory_info().rss / 1024**2, 2),
                "mem_vms_mb":   round(p.memory_info().vms / 1024**2, 2),
                "threads":      p.num_threads(),
                "open_files":   len(p.open_files()),
                "connections":  len(p.connections()),
                "status":       p.status(),
            }
    except Exception:
        return {}


def _db_kpis(db: Session) -> dict:
    from sqlalchemy import text
    def _count(table: str) -> int:
        try:
            return db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0
        except Exception:
            return 0
    return {
        "users":        _count("users"),
        "roles":        _count("roles"),
        "permissions":  _count("permissions"),
        "groups":       _count("groups"),
        "rbac_attrs":   _count("rbac_attributes"),
        "audit_logs":   _count("audit_logs"),
        "user_types":   _count("user_types"),
        "user_levels":  _count("user_levels"),
        "token_blacklist": _count("token_blacklist"),
    }


def _log_kpis(db: Session) -> dict:
    from sqlalchemy import text
    try:
        total = db.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar() or 0
        success = db.execute(text("SELECT COUNT(*) FROM audit_logs WHERE status='success'")).scalar() or 0
        failure = db.execute(text("SELECT COUNT(*) FROM audit_logs WHERE status='failure'")).scalar() or 0
        logins  = db.execute(text("SELECT COUNT(*) FROM audit_logs WHERE action='login_success'")).scalar() or 0
        recent  = db.execute(text(
            "SELECT actor, action, resource, status, created_at FROM audit_logs "
            "ORDER BY created_at DESC LIMIT 10"
        )).fetchall()
        return {
            "total": total, "success": success, "failure": failure,
            "logins": logins,
            "recent": [
                {"actor": r[0], "action": r[1], "resource": r[2],
                 "status": r[3], "created_at": str(r[4])}
                for r in recent
            ],
        }
    except Exception:
        return {"total": 0, "success": 0, "failure": 0, "logins": 0, "recent": []}


@router.get("/")
def get_metrics(db: Session = Depends(get_db), _=Depends(require_superuser)):
    uptime_s = round(time.time() - _START_TIME)
    return {
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "uptime_s":   uptime_s,
        "uptime_fmt": f"{uptime_s//3600}h {(uptime_s%3600)//60}m {uptime_s%60}s",
        "platform":   platform.system(),
        "python":     platform.python_version(),
        "psutil":     _HAS_PSUTIL,
        "cpu":        _cpu(),
        "memory":     _memory(),
        "disk":       _disk(),
        "network":    _network(),
        "process":    _process(),
        "db":         _db_kpis(db),
        "logs":       _log_kpis(db),
    }


@router.get("/logs")
def get_logs(
    skip: int = 0, limit: int = 200,
    db: Session = Depends(get_db),
    _=Depends(require_superuser),
):
    from sqlalchemy import text
    try:
        rows = db.execute(text(
            "SELECT id, actor, action, resource, resource_id, detail, "
            "ip_address, status, created_at FROM audit_logs "
            "ORDER BY created_at DESC LIMIT :limit OFFSET :skip"
        ), {"limit": limit, "skip": skip}).fetchall()
        total = db.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar() or 0
        return {
            "total": total, "skip": skip, "limit": limit,
            "logs": [
                {"id": r[0], "actor": r[1], "action": r[2], "resource": r[3],
                 "resource_id": r[4], "detail": r[5], "ip_address": r[6],
                 "status": r[7], "created_at": str(r[8])}
                for r in rows
            ],
        }
    except Exception as e:
        return {"total": 0, "skip": skip, "limit": limit, "logs": [], "error": str(e)}
