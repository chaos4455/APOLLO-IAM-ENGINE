# event_logger.py
# Sistema de log incremental universal - Apollo IAM Engine v4
# Escrita em arquivo via fila assincrona (background thread) - sem bloquear requests.
# SQLite com WAL + cache 16MB + mmap 256MB para o log DB.
from __future__ import annotations

import hashlib
import json
import os
import queue
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

import yaml
from sqlalchemy import Column, Integer, String, Text, create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker

# ── paths ─────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_BASE, "..", "..", "..", ".."))

_LOG_JSON = os.path.join(_ROOT, "logs", "json", "apollo_events.json")
_LOG_YAML = os.path.join(_ROOT, "logs", "yaml", "apollo_events.yaml")
_LOG_MD   = os.path.join(_ROOT, "logs", "md",   "apollo_events.md")
_LOG_DB   = os.path.join(_ROOT, "data", "apollo_log.db")

for _d in (
    os.path.dirname(_LOG_JSON),
    os.path.dirname(_LOG_YAML),
    os.path.dirname(_LOG_MD),
    os.path.dirname(_LOG_DB),
):
    os.makedirs(_d, exist_ok=True)

# ── SQLite log DB ─────────────────────────────────────────────────────────────
_LogBase = declarative_base()


class EventLogModel(_LogBase):
    __tablename__ = "event_log"
    seq         = Column(Integer, primary_key=True, autoincrement=True)
    uid         = Column(String(36),  unique=True, nullable=False)
    hash        = Column(String(64),  nullable=False)
    timestamp   = Column(String(30),  nullable=False, index=True)
    event       = Column(String(120), nullable=False, index=True)
    actor       = Column(String(120), nullable=False, index=True)
    resource    = Column(String(120), nullable=False)
    resource_id = Column(String(120), nullable=True)
    tenant_id   = Column(String(120), nullable=True,  index=True)
    session_id  = Column(String(36),  nullable=True)
    status      = Column(String(20),  nullable=False, default="success", index=True)
    duration_ms = Column(String(20),  nullable=True)
    tags        = Column(Text,        nullable=True)
    detail      = Column(Text,        nullable=True)


class DecisionAuditModel(_LogBase):
    __tablename__ = "decision_audit"
    seq             = Column(Integer, primary_key=True, autoincrement=True)
    uid             = Column(String(36),  unique=True, nullable=False, index=True)
    timestamp       = Column(String(30),  nullable=False, index=True)
    actor           = Column(String(120), nullable=False, index=True)
    subject_id      = Column(String(120), nullable=True,  index=True)
    tenant_id       = Column(String(120), nullable=True,  index=True)
    action          = Column(String(120), nullable=False, index=True)
    resource        = Column(String(255), nullable=False)
    decision        = Column(String(20),  nullable=False, index=True)
    matched_policy  = Column(String(120), nullable=True)
    matched_rule    = Column(String(255), nullable=True)
    reason          = Column(Text,        nullable=True)
    failing_condition = Column(Text,      nullable=True)
    chain           = Column(Text,        nullable=True)
    duration_ms     = Column(String(20),  nullable=True)
    from_cache      = Column(String(5),   nullable=True, default="false")


_log_engine = create_engine(
    f"sqlite:///{_LOG_DB}",
    connect_args={"check_same_thread": False},
    echo=False,
)


@event.listens_for(_log_engine, "connect")
def _log_db_pragmas(dbapi_conn, _rec):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL")
    cur.execute("PRAGMA synchronous=NORMAL")
    cur.execute("PRAGMA cache_size=-16384")
    cur.execute("PRAGMA temp_store=MEMORY")
    cur.execute("PRAGMA mmap_size=268435456")
    cur.execute("PRAGMA wal_autocheckpoint=2000")
    cur.close()


_LogBase.metadata.create_all(bind=_log_engine)


def _migrate_event_log():
    expected = {
        "tenant_id":   "VARCHAR(120)",
        "session_id":  "VARCHAR(36)",
        "duration_ms": "VARCHAR(20)",
        "tags":        "TEXT",
    }
    with _log_engine.begin() as conn:
        existing = {row[1] for row in conn.execute(text("PRAGMA table_info(event_log)"))}
        for col, col_type in expected.items():
            if col not in existing:
                conn.execute(text(f"ALTER TABLE event_log ADD COLUMN {col} {col_type}"))

    _log_indexes = [
        "CREATE INDEX IF NOT EXISTS ix_event_log_actor_status ON event_log(actor, status)",
        "CREATE INDEX IF NOT EXISTS ix_event_log_tenant_event ON event_log(tenant_id, event)",
        "CREATE INDEX IF NOT EXISTS ix_decision_audit_tenant_decision ON decision_audit(tenant_id, decision)",
        "CREATE INDEX IF NOT EXISTS ix_decision_audit_subject_action ON decision_audit(subject_id, action)",
    ]
    with _log_engine.begin() as conn:
        for idx in _log_indexes:
            try:
                conn.execute(text(idx))
            except Exception:
                pass


_migrate_event_log()
_LogSession = sessionmaker(bind=_log_engine, autocommit=False, autoflush=False,
                           expire_on_commit=False)

# ── fila assincrona para file I/O ─────────────────────────────────────────────
_file_queue: queue.Queue = queue.Queue(maxsize=10000)
_db_lock = threading.Lock()


def _file_writer():
    while True:
        try:
            item = _file_queue.get(timeout=1.0)
            if item is None:
                break
            kind, payload = item
            if kind == "event":
                _write_event_files(payload)
            _file_queue.task_done()
        except queue.Empty:
            continue
        except Exception:
            pass


def _write_event_files(entry: dict):
    try:
        with open(_LOG_JSON, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    except Exception:
        pass
    try:
        with open(_LOG_YAML, "a", encoding="utf-8") as f:
            yaml.dump([entry], f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            f.write("---\n")
    except Exception:
        pass
    try:
        detail_str = json.dumps(entry.get("detail") or {}, ensure_ascii=False, default=str)
        detail_md = detail_str.replace("|", "\\|")[:80]
        dur = entry.get("duration_ms")
        dur_md = f"{round(dur, 1)}ms" if dur is not None else "-"
        with open(_LOG_MD, "a", encoding="utf-8") as f:
            f.write(
                f"| {entry.get('seq', '?')} | `{entry['uid'][:8]}` | {entry['timestamp']} "
                f"| `{entry['event']}` | {entry['actor']} | {entry['resource']} "
                f"| {entry.get('resource_id') or '-'} | {entry.get('tenant_id') or '-'} "
                f"| {entry['status']} | {dur_md} | {detail_md} |\n"
            )
    except Exception:
        pass


_writer_thread = threading.Thread(target=_file_writer, daemon=True, name="log-file-writer")
_writer_thread.start()


def _ensure_md_header():
    if not os.path.exists(_LOG_MD) or os.path.getsize(_LOG_MD) == 0:
        with open(_LOG_MD, "w", encoding="utf-8") as f:
            f.write("# Apollo IAM Engine - Event Log\n\n")
            f.write("| seq | uid | timestamp | event | actor | resource | resource_id | tenant | status | duration_ms | detail |\n")
            f.write("|-----|-----|-----------|-------|-------|----------|-------------|--------|--------|-------------|--------|\n")


_ensure_md_header()


# ── funcao principal ──────────────────────────────────────────────────────────

def log_event(
    event: str,
    actor: str = "system",
    resource: str = "",
    resource_id: str | None = None,
    status: str = "success",
    detail: dict[str, Any] | None = None,
    tenant_id: str | None = None,
    session_id: str | None = None,
    duration_ms: float | None = None,
    tags: list[str] | None = None,
) -> dict:
    uid = str(uuid.uuid4())
    ts  = datetime.now(timezone.utc).isoformat()
    detail_str = json.dumps(detail or {}, ensure_ascii=False, default=str)
    tags_str   = json.dumps(tags or [], ensure_ascii=False)

    raw = f"{uid}{ts}{event}{actor}{resource}{resource_id}{status}{detail_str}"
    entry_hash = hashlib.sha256(raw.encode()).hexdigest()
    dur_str = str(round(duration_ms, 2)) if duration_ms is not None else None

    seq = 0
    with _db_lock:
        db = _LogSession()
        try:
            m = EventLogModel(
                uid=uid, hash=entry_hash, timestamp=ts,
                event=event, actor=actor, resource=resource,
                resource_id=resource_id, tenant_id=tenant_id,
                session_id=session_id, status=status,
                duration_ms=dur_str, tags=tags_str,
                detail=detail_str,
            )
            db.add(m)
            db.commit()
            seq = m.seq or 0
        finally:
            db.close()

    entry = {
        "seq":         seq,
        "uid":         uid,
        "hash":        entry_hash,
        "timestamp":   ts,
        "event":       event,
        "actor":       actor,
        "resource":    resource,
        "resource_id": resource_id,
        "tenant_id":   tenant_id,
        "session_id":  session_id,
        "status":      status,
        "duration_ms": duration_ms,
        "tags":        tags or [],
        "detail":      detail or {},
    }

    try:
        _file_queue.put_nowait(("event", entry))
    except queue.Full:
        pass

    return entry


# ── audit de decisoes de policy ───────────────────────────────────────────────

def log_decision(
    actor: str,
    subject_id: str,
    tenant_id: str | None,
    action: str,
    resource: str,
    decision: str,
    matched_policy: str | None = None,
    matched_rule: str | None = None,
    reason: str = "",
    failing_condition: str | None = None,
    chain: list[str] | None = None,
    duration_ms: float | None = None,
    from_cache: bool = False,
) -> str:
    uid = str(uuid.uuid4())
    ts  = datetime.now(timezone.utc).isoformat()
    dur_str = str(round(duration_ms, 2)) if duration_ms is not None else None

    with _db_lock:
        db = _LogSession()
        try:
            m = DecisionAuditModel(
                uid=uid, timestamp=ts, actor=actor,
                subject_id=subject_id or "", tenant_id=tenant_id,
                action=action, resource=resource, decision=decision,
                matched_policy=matched_policy, matched_rule=matched_rule,
                reason=reason, failing_condition=failing_condition,
                chain=json.dumps(chain or []),
                duration_ms=dur_str,
                from_cache="true" if from_cache else "false",
            )
            db.add(m)
            db.commit()
        finally:
            db.close()

    return uid


def query_decisions(
    tenant_id: str | None = None,
    subject_id: str | None = None,
    decision: str | None = None,
    action: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    with _log_engine.connect() as conn:
        wheres = []
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if tenant_id:
            wheres.append("tenant_id = :tenant_id")
            params["tenant_id"] = tenant_id
        if subject_id:
            wheres.append("subject_id = :subject_id")
            params["subject_id"] = subject_id
        if decision:
            wheres.append("decision = :decision")
            params["decision"] = decision
        if action:
            wheres.append("action = :action")
            params["action"] = action

        where_clause = f"WHERE {' AND '.join(wheres)}" if wheres else ""
        sql = text(
            f"SELECT seq, uid, timestamp, actor, subject_id, tenant_id, "
            f"action, resource, decision, matched_policy, matched_rule, "
            f"reason, failing_condition, chain, duration_ms, from_cache "
            f"FROM decision_audit {where_clause} "
            f"ORDER BY seq DESC LIMIT :limit OFFSET :offset"
        )
        rows = conn.execute(sql, params).fetchall()

    return [
        {
            "seq":               r[0],
            "uid":               r[1],
            "timestamp":         r[2],
            "actor":             r[3],
            "subject_id":        r[4],
            "tenant_id":         r[5],
            "action":            r[6],
            "resource":          r[7],
            "decision":          r[8],
            "matched_policy":    r[9],
            "matched_rule":      r[10],
            "reason":            r[11],
            "failing_condition": r[12],
            "chain":             json.loads(r[13]) if r[13] else [],
            "duration_ms":       r[14],
            "from_cache":        r[15] == "true",
        }
        for r in rows
    ]
