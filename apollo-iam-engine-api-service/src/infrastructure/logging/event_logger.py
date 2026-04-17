"""
event_logger.py
Sistema de log incremental universal — 100% dos eventos do Apollo IAM Engine.
v3: tabela decision_audit dedicada para auditoria de decisões de policy.

Cada entrada de evento tem:
  uid, seq, hash (SHA-256), timestamp, event, actor, resource,
  resource_id, tenant_id, session_id, status, duration_ms, tags, detail

Tabela decision_audit (nova):
  uid, timestamp, subject_id, tenant_id, action, resource,
  decision (allow|deny|no_match), matched_policy, matched_rule,
  reason, failing_condition, chain (JSON), duration_ms, actor

Saídas simultâneas:
  - logs/json/apollo_events.json   (NDJSON)
  - logs/yaml/apollo_events.yaml   (YAML docs)
  - logs/md/apollo_events.md       (Markdown table)
  - data/apollo_log.db             (SQLite — event_log + decision_audit)
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import yaml
from sqlalchemy import Column, Integer, String, Text, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# ── paths ─────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
# sobe até a raiz do projeto (src/infrastructure/logging → raiz)
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
    status      = Column(String(20),  nullable=False, default="success")
    duration_ms = Column(String(20),  nullable=True)
    tags        = Column(Text,        nullable=True)
    detail      = Column(Text,        nullable=True)


class DecisionAuditModel(_LogBase):
    """
    Tabela dedicada para auditoria de decisões de policy.
    Cada avaliação de policy gera uma entrada aqui — imutável, auditável.
    """
    __tablename__ = "decision_audit"
    seq             = Column(Integer, primary_key=True, autoincrement=True)
    uid             = Column(String(36),  unique=True, nullable=False, index=True)
    timestamp       = Column(String(30),  nullable=False, index=True)
    actor           = Column(String(120), nullable=False, index=True)
    subject_id      = Column(String(120), nullable=True,  index=True)
    tenant_id       = Column(String(120), nullable=True,  index=True)
    action          = Column(String(120), nullable=False, index=True)
    resource        = Column(String(255), nullable=False)
    decision        = Column(String(20),  nullable=False, index=True)  # allow|deny|no_match
    matched_policy  = Column(String(120), nullable=True)
    matched_rule    = Column(String(255), nullable=True)
    reason          = Column(Text,        nullable=True)
    failing_condition = Column(Text,      nullable=True)
    chain           = Column(Text,        nullable=True)   # JSON list
    duration_ms     = Column(String(20),  nullable=True)
    from_cache      = Column(String(5),   nullable=True, default="false")


_log_engine = create_engine(
    f"sqlite:///{_LOG_DB}",
    connect_args={"check_same_thread": False},
    echo=False,
)
_LogBase.metadata.create_all(bind=_log_engine)


def _migrate_event_log():
    """Add any missing columns to event_log (handles schema drift on existing DBs)."""
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


_migrate_event_log()
_LogSession = sessionmaker(bind=_log_engine, autocommit=False, autoflush=False)

# ── sequência global thread-safe ──────────────────────────────────────────────
_seq_lock = threading.Lock()


def _next_seq(db) -> int:
    row = db.execute(text("SELECT MAX(seq) FROM event_log")).fetchone()
    return (row[0] or 0) + 1


# ── MD header (escrito uma vez) ───────────────────────────────────────────────
def _ensure_md_header():
    if not os.path.exists(_LOG_MD) or os.path.getsize(_LOG_MD) == 0:
        with open(_LOG_MD, "w", encoding="utf-8") as f:
            f.write("# Apollo IAM Engine — Event Log\n\n")
            f.write("| seq | uid | timestamp | event | actor | resource | resource_id | tenant | status | duration_ms | detail |\n")
            f.write("|-----|-----|-----------|-------|-------|----------|-------------|--------|--------|-------------|--------|\n")


_ensure_md_header()


# ── função principal ──────────────────────────────────────────────────────────

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
    """
    Registra um evento em todas as saídas (JSON, YAML, MD, DB).
    Retorna o dict da entrada criada.
    """
    uid = str(uuid.uuid4())
    ts  = datetime.now(timezone.utc).isoformat()
    detail_str = json.dumps(detail or {}, ensure_ascii=False, default=str)
    tags_str   = json.dumps(tags or [], ensure_ascii=False)

    # SHA-256 do conteúdo para integridade
    raw = f"{uid}{ts}{event}{actor}{resource}{resource_id}{status}{detail_str}"
    entry_hash = hashlib.sha256(raw.encode()).hexdigest()

    dur_str = str(round(duration_ms, 2)) if duration_ms is not None else None

    with _seq_lock:
        db = _LogSession()
        try:
            seq = _next_seq(db)
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

    # JSON (NDJSON)
    with open(_LOG_JSON, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

    # YAML
    with open(_LOG_YAML, "a", encoding="utf-8") as f:
        yaml.dump([entry], f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.write("---\n")

    # MD
    detail_md = detail_str.replace("|", "\\|")[:80]
    dur_md    = f"{round(duration_ms, 1)}ms" if duration_ms is not None else "—"
    with open(_LOG_MD, "a", encoding="utf-8") as f:
        f.write(
            f"| {seq} | `{uid[:8]}` | {ts} | `{event}` | {actor} "
            f"| {resource} | {resource_id or '—'} | {tenant_id or '—'} "
            f"| {status} | {dur_md} | {detail_md} |\n"
        )

    return entry


# ── audit de decisões de policy ───────────────────────────────────────────────

def log_decision(
    actor: str,
    subject_id: str,
    tenant_id: str | None,
    action: str,
    resource: str,
    decision: str,                    # "allow" | "deny" | "no_match"
    matched_policy: str | None = None,
    matched_rule: str | None = None,
    reason: str = "",
    failing_condition: str | None = None,
    chain: list[str] | None = None,
    duration_ms: float | None = None,
    from_cache: bool = False,
) -> str:
    """
    Registra uma decisão de policy no audit trail dedicado.
    Retorna o uid da entrada criada.

    Cada chamada a /admin/policies/evaluate deve chamar esta função.
    Imutável — nunca atualiza, só insere.
    """
    uid = str(uuid.uuid4())
    ts  = datetime.now(timezone.utc).isoformat()
    dur_str = str(round(duration_ms, 2)) if duration_ms is not None else None

    with _seq_lock:
        db = _LogSession()
        try:
            m = DecisionAuditModel(
                uid=uid,
                timestamp=ts,
                actor=actor,
                subject_id=subject_id or "",
                tenant_id=tenant_id,
                action=action,
                resource=resource,
                decision=decision,
                matched_policy=matched_policy,
                matched_rule=matched_rule,
                reason=reason,
                failing_condition=failing_condition,
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
    decision: str | None = None,      # "allow" | "deny" | "no_match"
    action: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    """
    Consulta o audit trail de decisões com filtros opcionais.
    Retorna lista de dicts ordenada por timestamp DESC.
    """
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
