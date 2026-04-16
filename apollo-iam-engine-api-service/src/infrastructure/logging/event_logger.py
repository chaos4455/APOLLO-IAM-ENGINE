"""
event_logger.py
Sistema de log incremental universal — 100% dos eventos do Apollo IAM Engine.

Cada entrada tem:
  - uid:       UUID4 único por entrada
  - seq:       sequência incremental global (nunca reseta)
  - hash:      SHA-1 do conteúdo serializado (integridade simples)
  - timestamp: ISO-8601 UTC
  - event:     tipo do evento (ex: user.created, auth.login_success)
  - actor:     quem disparou
  - resource:  entidade afetada
  - resource_id
  - detail:    dados extras (dict)
  - status:    success | failure | warning

Saídas simultâneas:
  - logs/json/apollo_events.json   (NDJSON — uma linha por entrada)
  - logs/yaml/apollo_events.yaml   (documentos YAML separados por ---)
  - logs/md/apollo_events.md       (tabela Markdown incremental)
  - data/apollo_log.db             (SQLite dedicado — tabela event_log)
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
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
    seq        = Column(Integer, primary_key=True, autoincrement=True)
    uid        = Column(String(36), unique=True, nullable=False)
    hash       = Column(String(40), nullable=False)
    timestamp  = Column(String(30), nullable=False, index=True)
    event      = Column(String(120), nullable=False, index=True)
    actor      = Column(String(120), nullable=False, index=True)
    resource   = Column(String(120), nullable=False)
    resource_id= Column(String(120), nullable=True)
    status     = Column(String(20),  nullable=False, default="success")
    detail     = Column(Text,        nullable=True)


_log_engine = create_engine(
    f"sqlite:///{_LOG_DB}",
    connect_args={"check_same_thread": False},
    echo=False,
)
_LogBase.metadata.create_all(bind=_log_engine)
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
            f.write("| seq | uid | timestamp | event | actor | resource | resource_id | status | detail |\n")
            f.write("|-----|-----|-----------|-------|-------|----------|-------------|--------|--------|\n")


_ensure_md_header()


# ── função principal ──────────────────────────────────────────────────────────

def log_event(
    event: str,
    actor: str = "system",
    resource: str = "",
    resource_id: str | None = None,
    status: str = "success",
    detail: dict[str, Any] | None = None,
) -> dict:
    """
    Registra um evento em todas as saídas (JSON, YAML, MD, DB).
    Retorna o dict da entrada criada.
    """
    uid = str(uuid.uuid4())
    ts  = datetime.now(timezone.utc).isoformat()
    detail_str = json.dumps(detail or {}, ensure_ascii=False, default=str)

    # hash simples do conteúdo
    raw = f"{uid}{ts}{event}{actor}{resource}{resource_id}{status}{detail_str}"
    entry_hash = hashlib.sha1(raw.encode()).hexdigest()

    with _seq_lock:
        db = _LogSession()
        try:
            seq = _next_seq(db)
            m = EventLogModel(
                uid=uid, hash=entry_hash, timestamp=ts,
                event=event, actor=actor, resource=resource,
                resource_id=resource_id, status=status,
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
        "status":      status,
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
    with open(_LOG_MD, "a", encoding="utf-8") as f:
        f.write(
            f"| {seq} | `{uid[:8]}` | {ts} | `{event}` | {actor} "
            f"| {resource} | {resource_id or '—'} | {status} | {detail_md} |\n"
        )

    return entry
