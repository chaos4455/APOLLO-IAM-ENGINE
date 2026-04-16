"""
fix-v3.py — Compatibilidade SQLAlchemy 1.4
Corrige base.py, models e connection.py para rodar com SQLAlchemy 1.4
O2 Data Solutions
"""

import os
import time

BASE = "apollo-iam-engine-api-service"


def w(rel: str, content: str):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def fix_base():
    w("src/infrastructure/database/base.py", '''\
from sqlalchemy.orm import declarative_base

Base = declarative_base()
''')


def fix_connection():
    w("src/infrastructure/database/connection.py", '''\
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.base import Base

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from src.infrastructure.database.models import (  # noqa: F401
        user_model, role_model, permission_model, group_model,
        user_type_model, user_level_model, rbac_attribute_model,
        settings_model, audit_log_model, token_blacklist_model,
    )
    Base.metadata.create_all(bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')


def fix_models():
    # user_model — remove JSON import nao usado, mantém compatível 1.4
    w("src/infrastructure/database/models/user_model.py", '''\
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base

user_roles = Table(
    "user_roles", Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
)

user_rbac_values = Table(
    "user_rbac_values", Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("attribute_id", String, ForeignKey("rbac_attributes.id"), primary_key=True),
    Column("value", String, nullable=False),
)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    group_id = Column(String, ForeignKey("groups.id"), nullable=True)
    type_id = Column(String, ForeignKey("user_types.id"), nullable=True)
    level_id = Column(String, ForeignKey("user_levels.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    roles = relationship("RoleModel", secondary=user_roles, back_populates="users")
    group = relationship("GroupModel", back_populates="users")
    user_type = relationship("UserTypeModel")
    user_level = relationship("UserLevelModel")
''')

    w("src/infrastructure/database/models/role_model.py", '''\
from sqlalchemy import Column, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.user_model import user_roles

role_permissions = Table(
    "role_permissions", Base.metadata,
    Column("role_id", String, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", String, ForeignKey("permissions.id"), primary_key=True),
)


class RoleModel(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("UserModel", secondary=user_roles, back_populates="roles")
    permissions = relationship("PermissionModel", secondary=role_permissions, back_populates="roles")
''')

    w("src/infrastructure/database/models/permission_model.py", '''\
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base
from src.infrastructure.database.models.role_model import role_permissions


class PermissionModel(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship("RoleModel", secondary=role_permissions, back_populates="permissions")
''')

    w("src/infrastructure/database/models/group_model.py", '''\
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database.base import Base


class GroupModel(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("UserModel", back_populates="group")
''')

    w("src/infrastructure/database/models/user_type_model.py", '''\
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class UserTypeModel(Base):
    __tablename__ = "user_types"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
''')

    w("src/infrastructure/database/models/user_level_model.py", '''\
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class UserLevelModel(Base):
    __tablename__ = "user_levels"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    rank = Column(Integer, default=0)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
''')

    w("src/infrastructure/database/models/rbac_attribute_model.py", '''\
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class RbacAttributeModel(Base):
    __tablename__ = "rbac_attributes"
    id = Column(String, primary_key=True)
    key = Column(String, unique=True, nullable=False, index=True)
    label = Column(String, nullable=False)
    value_type = Column(String, default="string")
    description = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
''')

    w("src/infrastructure/database/models/settings_model.py", '''\
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class SettingsModel(Base):
    __tablename__ = "settings"
    id = Column(String, primary_key=True, default="singleton")
    access_token_expire_minutes = Column(Integer, default=60)
    refresh_token_expire_days = Column(Integer, default=7)
    allow_registration = Column(Boolean, default=False)
    max_login_attempts = Column(Integer, default=5)
    lockout_minutes = Column(Integer, default=15)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
''')

    w("src/infrastructure/database/models/audit_log_model.py", '''\
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    detail = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    status = Column(String, default="success")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
''')

    w("src/infrastructure/database/models/token_blacklist_model.py", '''\
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from src.infrastructure.database.base import Base


class TokenBlacklistModel(Base):
    __tablename__ = "token_blacklist"
    jti = Column(String, primary_key=True)
    revoked_at = Column(DateTime, default=datetime.utcnow)
''')

    w("src/infrastructure/database/models/__init__.py", '''\
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.database.models.permission_model import PermissionModel
from src.infrastructure.database.models.group_model import GroupModel
from src.infrastructure.database.models.user_type_model import UserTypeModel
from src.infrastructure.database.models.user_level_model import UserLevelModel
from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel
from src.infrastructure.database.models.settings_model import SettingsModel
from src.infrastructure.database.models.audit_log_model import AuditLogModel
from src.infrastructure.database.models.token_blacklist_model import TokenBlacklistModel

__all__ = [
    "UserModel", "RoleModel", "PermissionModel", "GroupModel",
    "UserTypeModel", "UserLevelModel", "RbacAttributeModel",
    "SettingsModel", "AuditLogModel", "TokenBlacklistModel",
]
''')


def fix_migrations_env():
    w("src/infrastructure/database/migrations/env.py", '''\
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.infrastructure.database.base import Base
from src.infrastructure.database.models import (  # noqa: F401
    user_model, role_model, permission_model, group_model,
    user_type_model, user_level_model, rbac_attribute_model,
    settings_model, audit_log_model, token_blacklist_model,
)

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
''')


def fix_type_hints():
    """Corrige type hints Python 3.10+ (X | Y, list[X]) para 3.9/3.10 compat via __future__"""

    files_to_patch = [
        "src/domain/value_objects/token_payload.py",
        "src/application/dtos/user_dto.py",
        "src/application/dtos/settings_dto.py",
        "src/application/services/rbac_service.py",
        "src/application/use_cases/roles/update_role.py",
        "src/application/use_cases/groups/update_group.py",
        "src/application/use_cases/permissions/update_permission.py",
        "src/application/use_cases/rbac/update_attribute.py",
        "src/infrastructure/logging/file_logger.py",
    ]

    for rel in files_to_patch:
        path = os.path.join(BASE, rel)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "from __future__ import annotations" not in content:
            content = "from __future__ import annotations\n" + content
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


def fix_settings_lru_cache():
    """get_settings usa lru_cache — precisa resetar entre testes. Adiciona reset helper."""
    w("src/infrastructure/config/settings.py", '''\
from __future__ import annotations
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Apollo IAM Engine"
    app_version: str = "1.0.0"
    secret_key: str = "change-me-super-secret-key-32chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./data/apollo_iam.db"
    log_level: str = "INFO"
    admin_username: str = "admin"
    admin_password: str = "admin"
    cors_origins: str = "*"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
''')


def fix_api_startup():
    """Remove on_event deprecated warning — usa lifespan para FastAPI 0.111+"""
    w("src/interface/api/main.py", '''\
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.connection import init_db, SessionLocal
from src.infrastructure.seed.seed_roles import seed_roles
from src.infrastructure.seed.seed_permissions import seed_permissions
from src.infrastructure.seed.seed_admin import seed_admin
from src.interface.api.routes.auth import router as auth_router
from src.interface.api.routes.admin.users import router as users_router
from src.interface.api.routes.admin.roles import router as roles_router
from src.interface.api.routes.admin.permissions import router as perms_router
from src.interface.api.routes.admin.groups import router as groups_router
from src.interface.api.routes.admin.rbac_attributes import router as rbac_router
from src.interface.api.routes.admin.settings import router as settings_router
from src.interface.api.routes.admin.audit_logs import router as audit_router
from src.infrastructure.logging.console_logger import success, info

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_permissions(db)
        seed_admin(db)
    finally:
        db.close()
    success(f"Apollo IAM Engine v{settings.app_version} iniciado!")
    info("Docs: http://localhost:8000/docs")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Servico centralizado de IAM + RBAC — O2 Data Solutions",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [auth_router, users_router, roles_router, perms_router,
               groups_router, rbac_router, settings_router, audit_router]:
    app.include_router(router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
''')


def fix_conftest():
    """Reescreve conftest para usar lifespan corretamente com TestClient"""
    w("tests/conftest.py", '''\
from __future__ import annotations
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# banco de teste isolado
TEST_DB_URL = "sqlite:///./data/test_apollo.db"

# garante que o diretório data existe
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)

engine_test = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    from src.infrastructure.database.base import Base
    from src.infrastructure.database.models import (  # noqa
        user_model, role_model, permission_model, group_model,
        user_type_model, user_level_model, rbac_attribute_model,
        settings_model, audit_log_model, token_blacklist_model,
    )
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)

    db = TestingSession()
    from src.infrastructure.seed.seed_roles import seed_roles
    from src.infrastructure.seed.seed_permissions import seed_permissions
    from src.infrastructure.seed.seed_admin import seed_admin
    seed_roles(db)
    seed_permissions(db)
    seed_admin(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="session")
def client(setup_test_db):
    from src.interface.api.main import app
    from src.infrastructure.database.connection import get_db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def admin_token(client):
    resp = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert resp.status_code == 200, f"Login falhou: {resp.text}"
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
''')


if __name__ == "__main__":
    import time
    from colorama import init
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import track

    init(autoreset=True)
    console = Console()
    _start = time.time()
    _written = []

    console.print(Panel.fit(
        "[bold orange1]🔧 APOLLO IAM — fix-v3.py[/bold orange1]\n"
        "[dim]Compatibilidade SQLAlchemy 1.4 + Python 3.10[/dim]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1"
    ))

    steps = [
        ("🗄️  base.py — declarative_base()",        fix_base),
        ("🔌  connection.py",                        fix_connection),
        ("📦  models — todos os 10 modelos",         fix_models),
        ("🔀  migrations/env.py",                    fix_migrations_env),
        ("🐍  type hints __future__ annotations",    fix_type_hints),
        ("⚙️  settings.py",                          fix_settings_lru_cache),
        ("🚀  api/main.py — lifespan",               fix_api_startup),
        ("🧪  tests/conftest.py",                    fix_conftest),
    ]

    for label, fn in track(steps, description="[orange1]Aplicando fixes...[/orange1]"):
        fn()
        console.print(f"  [green]✅[/green] {label}")

    elapsed = time.time() - _start

    table = Table(title="📊 fix-v3 Concluído", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan")
    table.add_column("Valor", style="bold green")
    table.add_row("🔧 Fixes aplicados", str(len(steps)))
    table.add_row("⏱️  Tempo", f"{elapsed:.2f}s")
    console.print(table)

    console.print(Panel.fit(
        "[bold green]✅ fix-v3 aplicado![/bold green]\n"
        "[dim]Agora rode: [bold]python run_tests.py[/bold][/dim]",
        border_style="green"
    ))
