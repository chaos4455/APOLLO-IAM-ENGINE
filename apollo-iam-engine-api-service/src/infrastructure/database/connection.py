"""
connection.py
SQLAlchemy engine com otimizações para SQLite:
  - WAL mode (Write-Ahead Logging) — leituras não bloqueiam escritas
  - cache_size aumentado (8 MB)
  - synchronous=NORMAL — mais rápido que FULL, ainda seguro
  - temp_store=MEMORY — tabelas temporárias em RAM
  - mmap_size=256 MB — memory-mapped I/O
  - pool_size + max_overflow para concorrência
O2 Data Solutions
"""
from __future__ import annotations
import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.base import Base

settings = get_settings()

_db_url = settings.database_url
if _db_url.startswith("sqlite:///"):
    _db_file = _db_url.replace("sqlite:///", "")
    _db_dir = os.path.dirname(os.path.abspath(_db_file))
    os.makedirs(_db_dir, exist_ok=True)

engine = create_engine(
    _db_url,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,          # espera até 30s por lock
    },
    # StaticPool não é adequado para produção — usa NullPool para SQLite
    # com check_same_thread=False já é thread-safe
    pool_pre_ping=True,         # verifica conexão antes de usar
    echo=False,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn, _connection_record):
    """Aplica PRAGMAs de performance em cada nova conexão SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")       # WAL: leituras não bloqueiam escritas
    cursor.execute("PRAGMA synchronous=NORMAL")     # mais rápido que FULL, seguro com WAL
    cursor.execute("PRAGMA cache_size=-8192")       # 8 MB de cache de páginas
    cursor.execute("PRAGMA temp_store=MEMORY")      # tabelas temp em RAM
    cursor.execute("PRAGMA mmap_size=268435456")    # 256 MB memory-mapped I/O
    cursor.execute("PRAGMA foreign_keys=ON")        # integridade referencial
    cursor.execute("PRAGMA busy_timeout=30000")     # 30s timeout em lock
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from src.infrastructure.database.models import (  # noqa: F401
        user_model, role_model, permission_model, group_model,
        user_type_model, user_level_model, rbac_attribute_model,
        settings_model, audit_log_model, token_blacklist_model,
    )
    from src.infrastructure.database.models import custom_entity_model  # noqa: F401
    from src.infrastructure.database.models import policy_model  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # migração de schema: adiciona colunas novas em tabelas existentes (SQLite)
    _migrations = [
        # policies v2: composition fields
        ("policies", "scope",      "VARCHAR(20) DEFAULT 'tenant'"),
        ("policies", "subject_id", "VARCHAR(120)"),
        ("policies", "inherits",   "TEXT DEFAULT '[]'"),
    ]
    with engine.begin() as conn:
        for table, col, col_def in _migrations:
            existing = {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))}
            if col not in existing:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}"))

    # cria índices extras para queries frequentes
    _indexes = [
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_created_at ON audit_logs(created_at DESC)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_actor ON audit_logs(actor)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_action ON audit_logs(action)",
        "CREATE INDEX IF NOT EXISTS ix_token_blacklist_jti ON token_blacklist(jti)",
        "CREATE INDEX IF NOT EXISTS ix_user_rbac_values_user ON user_rbac_values(user_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_custom_entities_user ON user_custom_entities(user_id)",
    ]
    with engine.begin() as conn:   # engine.begin() faz commit automático ao sair
        for idx in _indexes:
            try:
                conn.execute(text(idx))
            except Exception:
                pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
