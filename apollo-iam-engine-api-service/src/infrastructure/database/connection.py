"""
connection.py
SQLAlchemy engine com otimizações para SQLite:
  - WAL mode (Write-Ahead Logging) — leituras não bloqueiam escritas
  - cache_size aumentado (32 MB)
  - synchronous=NORMAL — mais rápido que FULL, ainda seguro
  - temp_store=MEMORY — tabelas temporárias em RAM
  - mmap_size=512 MB — memory-mapped I/O
  - wal_autocheckpoint=1000 — checkpoint menos frequente
  - page_size=4096 — alinhado com filesystem moderno
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
        "timeout": 30,
    },
    pool_pre_ping=True,
    echo=False,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn, _connection_record):
    """Aplica PRAGMAs de performance em cada nova conexão SQLite."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-32768")       # 32 MB de cache de páginas
    cursor.execute("PRAGMA temp_store=MEMORY")
    cursor.execute("PRAGMA mmap_size=536870912")     # 512 MB memory-mapped I/O
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=30000")
    cursor.execute("PRAGMA wal_autocheckpoint=1000") # checkpoint a cada 1000 páginas
    cursor.execute("PRAGMA optimize")                # atualiza estatísticas do query planner
    cursor.close()


# expire_on_commit=False evita re-SELECT após commit (ganho em leituras pós-write)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                            expire_on_commit=False, bind=engine)


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
        ("policies", "scope",          "VARCHAR(20) DEFAULT 'tenant'"),
        ("policies", "subject_id",     "VARCHAR(120)"),
        ("policies", "inherits",       "TEXT DEFAULT '[]'"),
        # v3: time-based + schema + weight
        ("policies", "valid_from",     "VARCHAR(40)"),
        ("policies", "valid_until",    "VARCHAR(40)"),
        ("policies", "time_window",    "VARCHAR(20)"),
        ("policies", "context_schema", "TEXT DEFAULT '{}'"),
        ("policies", "weight",         "INTEGER DEFAULT 0"),
        # audit_logs: colunas extras para filtros frequentes
        ("audit_logs", "tenant_id",   "VARCHAR(120)"),
        ("audit_logs", "session_id",  "VARCHAR(36)"),
        ("audit_logs", "duration_ms", "INTEGER"),
    ]
    with engine.begin() as conn:
        for table, col, col_def in _migrations:
            try:
                existing = {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))}
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}"))
            except Exception:
                pass

    # índices para todas as queries frequentes
    _indexes = [
        # audit_logs — filtros mais comuns
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_created_at  ON audit_logs(created_at DESC)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_actor       ON audit_logs(actor)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_action      ON audit_logs(action)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_status      ON audit_logs(status)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_resource    ON audit_logs(resource)",
        "CREATE INDEX IF NOT EXISTS ix_audit_logs_actor_status ON audit_logs(actor, status)",
        # token_blacklist — hot path em cada request autenticado
        "CREATE INDEX IF NOT EXISTS ix_token_blacklist_jti    ON token_blacklist(jti)",
        # associações user
        "CREATE INDEX IF NOT EXISTS ix_user_rbac_values_user  ON user_rbac_values(user_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_rbac_values_attr  ON user_rbac_values(attribute_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_custom_entities_user ON user_custom_entities(user_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_custom_entities_slug ON user_custom_entities(entity_type_slug)",
        "CREATE INDEX IF NOT EXISTS ix_user_roles_user        ON user_roles(user_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_roles_role        ON user_roles(role_id)",
        # role_permissions
        "CREATE INDEX IF NOT EXISTS ix_role_permissions_role  ON role_permissions(role_id)",
        "CREATE INDEX IF NOT EXISTS ix_role_permissions_perm  ON role_permissions(permission_id)",
        # users — filtros frequentes
        "CREATE INDEX IF NOT EXISTS ix_users_is_active        ON users(is_active)",
        "CREATE INDEX IF NOT EXISTS ix_users_group_id         ON users(group_id)",
        "CREATE INDEX IF NOT EXISTS ix_users_type_id          ON users(type_id)",
        "CREATE INDEX IF NOT EXISTS ix_users_level_id         ON users(level_id)",
        # policies — query principal: tenant_id + enabled + priority
        "CREATE INDEX IF NOT EXISTS ix_policies_tenant_enabled ON policies(tenant_id, enabled)",
        "CREATE INDEX IF NOT EXISTS ix_policies_enabled_prio   ON policies(enabled, priority)",
        "CREATE INDEX IF NOT EXISTS ix_policies_scope          ON policies(scope)",
        # custom entities
        "CREATE INDEX IF NOT EXISTS ix_custom_entity_values_slug ON custom_entity_values(entity_type_slug)",
        "CREATE INDEX IF NOT EXISTS ix_custom_entity_values_active ON custom_entity_values(entity_type_slug, is_active)",
        # permissions — resource+action lookup
        "CREATE INDEX IF NOT EXISTS ix_permissions_resource_action ON permissions(resource, action)",
    ]
    with engine.begin() as conn:
        for idx in _indexes:
            try:
                conn.execute(text(idx))
            except Exception:
                pass

    # ANALYZE após criar índices — atualiza estatísticas do planner
    with engine.begin() as conn:
        try:
            conn.execute(text("ANALYZE"))
        except Exception:
            pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
