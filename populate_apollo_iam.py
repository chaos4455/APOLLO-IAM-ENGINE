"""
APOLLO-IAM-ENGINE-API-SERVICE — populate_apollo_iam.py
Popula todos os arquivos do projeto com código real.
O2 Data Solutions
"""

import os

BASE = "apollo-iam-engine-api-service"

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def w(rel: str, content: str):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ===========================================================================
# ROOT FILES
# ===========================================================================

def root_files():

    w(".env.example", """\
# Apollo IAM Engine — environment variables
SECRET_KEY=change-me-super-secret-key-32chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./data/apollo_iam.db
LOG_LEVEL=INFO
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
APP_NAME=Apollo IAM Engine
APP_VERSION=1.0.0
CORS_ORIGINS=*
""")

    w(".gitignore", """\
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
*.db
*.sqlite3
.venv/
venv/
logs/*.yaml
logs/*.json
logs/*.md
logs/yaml/
logs/json/
logs/md/
data/
.pytest_cache/
.mypy_cache/
htmlcov/
.coverage
""")

    w("requirements.txt", """\
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
jinja2>=3.1.4
itsdangerous>=2.2.0
rich>=13.7.0
colorama>=0.4.6
pyyaml>=6.0.1
httpx>=0.27.0
pytest>=8.2.0
pytest-asyncio>=0.23.0
anyio>=4.3.0
""")

    w("pyproject.toml", """\
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
""")

    w("README.md", """\
# Apollo IAM Engine API Service

Serviço centralizado de IAM + RBAC para múltiplos micro-serviços.
Criado por **O2 Data Solutions**.

## Início rápido

```bash
pip install -r requirements.txt
python -m uvicorn src.interface.api.main:app --reload --port 8000
python -m uvicorn src.interface.webapp.main:app --reload --port 8080
```

- API Docs: http://localhost:8000/docs
- ReDoc:    http://localhost:8000/redoc
- Admin UI: http://localhost:8080/admin  (admin / admin)
""")

    w("Dockerfile", """\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8080
CMD ["uvicorn", "src.interface.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

    w("docker-compose.yml", """\
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file: .env
  webapp:
    build: .
    command: uvicorn src.interface.webapp.main:app --host 0.0.0.0 --port 8080
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    env_file: .env
""")

    w("alembic.ini", """\
[alembic]
script_location = src/infrastructure/database/migrations
sqlalchemy.url = sqlite:///./data/apollo_iam.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")

# ===========================================================================
# DOMAIN
# ===========================================================================

def domain_entities():

    w("src/domain/entities/user.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: Optional[str] = None
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    roles: list = field(default_factory=list)
    rbac_attributes: dict = field(default_factory=dict)

    def touch(self):
        self.updated_at = datetime.utcnow()
''')

    w("src/domain/entities/role.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Role:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    permissions: list = field(default_factory=list)
''')

    w("src/domain/entities/permission.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Permission:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    resource: str = ""
    action: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
''')

    w("src/domain/entities/group.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Group:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
''')

    w("src/domain/entities/user_type.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class UserType:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
''')

    w("src/domain/entities/user_level.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class UserLevel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    rank: int = 0
    description: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
''')

    w("src/domain/entities/token.py", '''\
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime = None
''')

    w("src/domain/entities/audit_log.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class AuditLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    actor: str = ""
    action: str = ""
    resource: str = ""
    resource_id: Optional[str] = None
    detail: Optional[str] = None
    ip_address: Optional[str] = None
    status: str = "success"
    created_at: datetime = field(default_factory=datetime.utcnow)
''')

    w("src/domain/entities/rbac_attribute.py", '''\
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class RbacAttribute:
    """Atributo RBAC dinâmico e expansível (ex: department, cost_center, system_access)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    key: str = ""          # ex: "department"
    label: str = ""        # ex: "Departamento"
    value_type: str = "string"  # string | integer | boolean | list
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
''')


def domain_value_objects():

    w("src/domain/value_objects/username.py", '''\
import re
from dataclasses import dataclass


_PATTERNS = [
    r"^[a-zA-Z0-9_.-]{2,64}$",           # user, usuario.nome, nome.sobrenome
    r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$",   # email@email.com
]


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if not any(re.match(p, self.value) for p in _PATTERNS):
            raise ValueError(f"Username inválido: {self.value!r}")

    def __str__(self):
        return self.value
''')

    w("src/domain/value_objects/password.py", '''\
from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    """Senha em texto plano — sem restrição de tamanho ou complexidade."""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Senha não pode ser vazia.")

    def __str__(self):
        return self.value
''')

    w("src/domain/value_objects/email.py", '''\
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", self.value):
            raise ValueError(f"E-mail inválido: {self.value!r}")

    def __str__(self):
        return self.value
''')

    w("src/domain/value_objects/token_payload.py", '''\
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenPayload:
    sub: str                          # username
    user_id: str = ""
    is_superuser: bool = False
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    group: str | None = None
    user_type: str | None = None
    user_level: str | None = None
    rbac: dict[str, Any] = field(default_factory=dict)
    exp: int = 0
    iat: int = 0
    jti: str = ""
''')


def domain_events():

    for name, fields in [
        ("user_created", "user_id: str\n    username: str"),
        ("user_updated", "user_id: str\n    changes: dict"),
        ("user_deleted", "user_id: str"),
        ("login_succeeded", "user_id: str\n    username: str\n    ip: str = ''"),
        ("login_failed", "username: str\n    reason: str\n    ip: str = ''"),
    ]:
        w(f"src/domain/events/{name}.py", f'''\
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class {name.replace("_", " ").title().replace(" ", "")}Event:
    {fields}
    occurred_at: datetime = field(default_factory=datetime.utcnow)
''')


def domain_exceptions():

    w("src/domain/exceptions/auth_exceptions.py", '''\
class InvalidCredentialsError(Exception):
    """Credenciais inválidas."""

class TokenExpiredError(Exception):
    """Token expirado."""

class TokenInvalidError(Exception):
    """Token inválido ou revogado."""

class InactiveUserError(Exception):
    """Usuário inativo."""
''')

    w("src/domain/exceptions/user_exceptions.py", '''\
class UserNotFoundError(Exception):
    """Usuário não encontrado."""

class UserAlreadyExistsError(Exception):
    """Usuário já existe."""

class InvalidUsernameError(Exception):
    """Username inválido."""
''')

    w("src/domain/exceptions/rbac_exceptions.py", '''\
class RoleNotFoundError(Exception):
    """Role não encontrada."""

class PermissionNotFoundError(Exception):
    """Permissão não encontrada."""

class GroupNotFoundError(Exception):
    """Grupo não encontrado."""

class AttributeNotFoundError(Exception):
    """Atributo RBAC não encontrado."""

class InsufficientPermissionsError(Exception):
    """Permissões insuficientes."""
''')


def domain_ports():

    w("src/domain/ports/user_repository.py", '''\
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User: ...
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]: ...
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]: ...
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...
    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]: ...
    @abstractmethod
    def delete(self, user_id: str) -> None: ...
    @abstractmethod
    def count(self) -> int: ...
''')

    w("src/domain/ports/role_repository.py", '''\
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.role import Role


class RoleRepository(ABC):
    @abstractmethod
    def save(self, role: Role) -> Role: ...
    @abstractmethod
    def find_by_id(self, role_id: str) -> Optional[Role]: ...
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Role]: ...
    @abstractmethod
    def list_all(self) -> list[Role]: ...
    @abstractmethod
    def delete(self, role_id: str) -> None: ...
''')

    w("src/domain/ports/permission_repository.py", '''\
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.permission import Permission


class PermissionRepository(ABC):
    @abstractmethod
    def save(self, perm: Permission) -> Permission: ...
    @abstractmethod
    def find_by_id(self, perm_id: str) -> Optional[Permission]: ...
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Permission]: ...
    @abstractmethod
    def list_all(self) -> list[Permission]: ...
    @abstractmethod
    def delete(self, perm_id: str) -> None: ...
''')

    w("src/domain/ports/group_repository.py", '''\
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.group import Group


class GroupRepository(ABC):
    @abstractmethod
    def save(self, group: Group) -> Group: ...
    @abstractmethod
    def find_by_id(self, group_id: str) -> Optional[Group]: ...
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Group]: ...
    @abstractmethod
    def list_all(self) -> list[Group]: ...
    @abstractmethod
    def delete(self, group_id: str) -> None: ...
''')

    w("src/domain/ports/token_service.py", '''\
from abc import ABC, abstractmethod
from src.domain.value_objects.token_payload import TokenPayload


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, payload: TokenPayload) -> str: ...
    @abstractmethod
    def create_refresh_token(self, payload: TokenPayload) -> str: ...
    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload: ...
    @abstractmethod
    def revoke_token(self, jti: str) -> None: ...
    @abstractmethod
    def is_revoked(self, jti: str) -> bool: ...
''')

    w("src/domain/ports/password_hasher.py", '''\
from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, plain: str) -> str: ...
    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool: ...
''')

    w("src/domain/ports/audit_logger.py", '''\
from abc import ABC, abstractmethod
from src.domain.entities.audit_log import AuditLog


class AuditLogger(ABC):
    @abstractmethod
    def log(self, entry: AuditLog) -> None: ...
    @abstractmethod
    def list_logs(self, skip: int = 0, limit: int = 100) -> list[AuditLog]: ...
''')

    w("src/domain/ports/rbac_attribute_repository.py", '''\
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.rbac_attribute import RbacAttribute


class RbacAttributeRepository(ABC):
    @abstractmethod
    def save(self, attr: RbacAttribute) -> RbacAttribute: ...
    @abstractmethod
    def find_by_id(self, attr_id: str) -> Optional[RbacAttribute]: ...
    @abstractmethod
    def find_by_key(self, key: str) -> Optional[RbacAttribute]: ...
    @abstractmethod
    def list_all(self) -> list[RbacAttribute]: ...
    @abstractmethod
    def delete(self, attr_id: str) -> None: ...
''')


# ===========================================================================
# INFRASTRUCTURE — config
# ===========================================================================

def infra_config():

    w("src/infrastructure/config/settings.py", '''\
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

    w("src/infrastructure/config/constants.py", '''\
DEFAULT_ROLES = ["superadmin", "admin", "operator", "viewer"]
DEFAULT_PERMISSIONS = [
    ("users:read",   "users",   "read"),
    ("users:write",  "users",   "write"),
    ("users:delete", "users",   "delete"),
    ("roles:read",   "roles",   "read"),
    ("roles:write",  "roles",   "write"),
    ("perms:read",   "permissions", "read"),
    ("perms:write",  "permissions", "write"),
    ("groups:read",  "groups",  "read"),
    ("groups:write", "groups",  "write"),
    ("rbac:read",    "rbac",    "read"),
    ("rbac:write",   "rbac",    "write"),
    ("settings:read",  "settings", "read"),
    ("settings:write", "settings", "write"),
    ("audit:read",   "audit",   "read"),
]
''')


# ===========================================================================
# INFRASTRUCTURE — database
# ===========================================================================

def infra_database():

    w("src/infrastructure/database/base.py", '''\
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
''')

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


def infra_models():

    w("src/infrastructure/database/models/user_model.py", '''\
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, JSON
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


# ===========================================================================
# INFRASTRUCTURE — security
# ===========================================================================

def infra_security():

    w("src/infrastructure/security/password_hasher_impl.py", '''\
from passlib.context import CryptContext
from src.domain.ports.password_hasher import PasswordHasher

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, plain: str) -> str:
        return _ctx.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return _ctx.verify(plain, hashed)
''')

    w("src/infrastructure/security/token_blacklist.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.token_blacklist_model import TokenBlacklistModel


class SqliteTokenBlacklist:
    def __init__(self, db: Session):
        self.db = db

    def revoke(self, jti: str) -> None:
        entry = TokenBlacklistModel(jti=jti)
        self.db.merge(entry)
        self.db.commit()

    def is_revoked(self, jti: str) -> bool:
        return self.db.query(TokenBlacklistModel).filter_by(jti=jti).first() is not None
''')

    w("src/infrastructure/security/jwt_service.py", '''\
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.domain.ports.token_service import TokenService
from src.domain.value_objects.token_payload import TokenPayload
from src.domain.exceptions.auth_exceptions import TokenExpiredError, TokenInvalidError
from src.infrastructure.config.settings import get_settings

settings = get_settings()


class JwtTokenService(TokenService):
    def __init__(self, blacklist=None):
        self._blacklist = blacklist

    def _build_claims(self, payload: TokenPayload, expire_delta: timedelta) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "sub": payload.sub,
            "user_id": payload.user_id,
            "is_superuser": payload.is_superuser,
            "roles": payload.roles,
            "permissions": payload.permissions,
            "group": payload.group,
            "user_type": payload.user_type,
            "user_level": payload.user_level,
            "rbac": payload.rbac,
            "iat": int(now.timestamp()),
            "exp": int((now + expire_delta).timestamp()),
            "jti": str(uuid.uuid4()),
        }

    def create_access_token(self, payload: TokenPayload) -> str:
        claims = self._build_claims(
            payload, timedelta(minutes=settings.access_token_expire_minutes)
        )
        return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)

    def create_refresh_token(self, payload: TokenPayload) -> str:
        claims = self._build_claims(
            payload, timedelta(days=settings.refresh_token_expire_days)
        )
        claims["type"] = "refresh"
        return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except JWTError as exc:
            if "expired" in str(exc).lower():
                raise TokenExpiredError() from exc
            raise TokenInvalidError() from exc
        jti = data.get("jti", "")
        if self._blacklist and self._blacklist.is_revoked(jti):
            raise TokenInvalidError("Token revogado.")
        return TokenPayload(
            sub=data["sub"],
            user_id=data.get("user_id", ""),
            is_superuser=data.get("is_superuser", False),
            roles=data.get("roles", []),
            permissions=data.get("permissions", []),
            group=data.get("group"),
            user_type=data.get("user_type"),
            user_level=data.get("user_level"),
            rbac=data.get("rbac", {}),
            exp=data.get("exp", 0),
            iat=data.get("iat", 0),
            jti=jti,
        )

    def revoke_token(self, jti: str) -> None:
        if self._blacklist:
            self._blacklist.revoke(jti)

    def is_revoked(self, jti: str) -> bool:
        return self._blacklist.is_revoked(jti) if self._blacklist else False
''')


# ===========================================================================
# INFRASTRUCTURE — repositories
# ===========================================================================

def infra_repositories():

    w("src/infrastructure/repositories/user_repository_impl.py", '''\
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.database.models.user_model import UserModel


def _to_entity(m: UserModel) -> User:
    u = User(
        id=m.id, username=m.username, email=m.email,
        hashed_password=m.hashed_password, full_name=m.full_name,
        is_active=m.is_active, is_superuser=m.is_superuser,
        group_id=m.group_id, type_id=m.type_id, level_id=m.level_id,
        created_at=m.created_at, updated_at=m.updated_at,
        roles=[r.name for r in m.roles],
    )
    return u


def _to_model(u: User, db: Session) -> UserModel:
    m = db.query(UserModel).filter_by(id=u.id).first() or UserModel(id=u.id)
    m.username = u.username
    m.email = u.email
    m.hashed_password = u.hashed_password
    m.full_name = u.full_name
    m.is_active = u.is_active
    m.is_superuser = u.is_superuser
    m.group_id = u.group_id
    m.type_id = u.type_id
    m.level_id = u.level_id
    m.created_at = u.created_at
    m.updated_at = u.updated_at
    return m


class SqliteUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        m = _to_model(user, self.db)
        self.db.merge(m)
        self.db.commit()
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(id=user_id).first()
        return _to_entity(m) if m else None

    def find_by_username(self, username: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(username=username).first()
        return _to_entity(m) if m else None

    def find_by_email(self, email: str) -> Optional[User]:
        m = self.db.query(UserModel).filter_by(email=email).first()
        return _to_entity(m) if m else None

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        rows = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [_to_entity(r) for r in rows]

    def delete(self, user_id: str) -> None:
        m = self.db.query(UserModel).filter_by(id=user_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()

    def count(self) -> int:
        return self.db.query(UserModel).count()
''')

    w("src/infrastructure/repositories/role_repository_impl.py", '''\
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.role import Role
from src.domain.ports.role_repository import RoleRepository
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.database.models.permission_model import PermissionModel


def _to_entity(m: RoleModel) -> Role:
    return Role(
        id=m.id, name=m.name, description=m.description,
        is_active=m.is_active, created_at=m.created_at,
        permissions=[p.name for p in m.permissions],
    )


class SqliteRoleRepository(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, role: Role) -> Role:
        m = self.db.query(RoleModel).filter_by(id=role.id).first() or RoleModel(id=role.id)
        m.name = role.name
        m.description = role.description
        m.is_active = role.is_active
        self.db.merge(m)
        self.db.commit()
        return role

    def find_by_id(self, role_id: str) -> Optional[Role]:
        m = self.db.query(RoleModel).filter_by(id=role_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Role]:
        m = self.db.query(RoleModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Role]:
        return [_to_entity(r) for r in self.db.query(RoleModel).all()]

    def delete(self, role_id: str) -> None:
        m = self.db.query(RoleModel).filter_by(id=role_id).first()
        if m:
            self.db.delete(m)
            self.db.commit()

    def assign_permission(self, role_id: str, permission_id: str) -> None:
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        perm = self.db.query(PermissionModel).filter_by(id=permission_id).first()
        if role and perm and perm not in role.permissions:
            role.permissions.append(perm)
            self.db.commit()
''')

    w("src/infrastructure/repositories/permission_repository_impl.py", '''\
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.permission import Permission
from src.domain.ports.permission_repository import PermissionRepository
from src.infrastructure.database.models.permission_model import PermissionModel


def _to_entity(m: PermissionModel) -> Permission:
    return Permission(id=m.id, name=m.name, resource=m.resource,
                      action=m.action, description=m.description, created_at=m.created_at)


class SqlitePermissionRepository(PermissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, perm: Permission) -> Permission:
        m = self.db.query(PermissionModel).filter_by(id=perm.id).first() or PermissionModel(id=perm.id)
        m.name = perm.name; m.resource = perm.resource
        m.action = perm.action; m.description = perm.description
        self.db.merge(m); self.db.commit()
        return perm

    def find_by_id(self, perm_id: str) -> Optional[Permission]:
        m = self.db.query(PermissionModel).filter_by(id=perm_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Permission]:
        m = self.db.query(PermissionModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Permission]:
        return [_to_entity(r) for r in self.db.query(PermissionModel).all()]

    def delete(self, perm_id: str) -> None:
        m = self.db.query(PermissionModel).filter_by(id=perm_id).first()
        if m:
            self.db.delete(m); self.db.commit()
''')

    w("src/infrastructure/repositories/group_repository_impl.py", '''\
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.group import Group
from src.domain.ports.group_repository import GroupRepository
from src.infrastructure.database.models.group_model import GroupModel


def _to_entity(m: GroupModel) -> Group:
    return Group(id=m.id, name=m.name, description=m.description,
                 is_active=m.is_active, created_at=m.created_at)


class SqliteGroupRepository(GroupRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, group: Group) -> Group:
        m = self.db.query(GroupModel).filter_by(id=group.id).first() or GroupModel(id=group.id)
        m.name = group.name; m.description = group.description; m.is_active = group.is_active
        self.db.merge(m); self.db.commit()
        return group

    def find_by_id(self, group_id: str) -> Optional[Group]:
        m = self.db.query(GroupModel).filter_by(id=group_id).first()
        return _to_entity(m) if m else None

    def find_by_name(self, name: str) -> Optional[Group]:
        m = self.db.query(GroupModel).filter_by(name=name).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[Group]:
        return [_to_entity(r) for r in self.db.query(GroupModel).all()]

    def delete(self, group_id: str) -> None:
        m = self.db.query(GroupModel).filter_by(id=group_id).first()
        if m:
            self.db.delete(m); self.db.commit()
''')

    w("src/infrastructure/repositories/rbac_attribute_repository_impl.py", '''\
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.rbac_attribute import RbacAttribute
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel


def _to_entity(m: RbacAttributeModel) -> RbacAttribute:
    return RbacAttribute(id=m.id, key=m.key, label=m.label,
                         value_type=m.value_type, description=m.description,
                         is_active=m.is_active, created_at=m.created_at)


class SqliteRbacAttributeRepository(RbacAttributeRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, attr: RbacAttribute) -> RbacAttribute:
        m = self.db.query(RbacAttributeModel).filter_by(id=attr.id).first() or RbacAttributeModel(id=attr.id)
        m.key = attr.key; m.label = attr.label; m.value_type = attr.value_type
        m.description = attr.description; m.is_active = attr.is_active
        self.db.merge(m); self.db.commit()
        return attr

    def find_by_id(self, attr_id: str) -> Optional[RbacAttribute]:
        m = self.db.query(RbacAttributeModel).filter_by(id=attr_id).first()
        return _to_entity(m) if m else None

    def find_by_key(self, key: str) -> Optional[RbacAttribute]:
        m = self.db.query(RbacAttributeModel).filter_by(key=key).first()
        return _to_entity(m) if m else None

    def list_all(self) -> list[RbacAttribute]:
        return [_to_entity(r) for r in self.db.query(RbacAttributeModel).all()]

    def delete(self, attr_id: str) -> None:
        m = self.db.query(RbacAttributeModel).filter_by(id=attr_id).first()
        if m:
            self.db.delete(m); self.db.commit()
''')

    w("src/infrastructure/repositories/audit_log_repository_impl.py", '''\
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
''')


# ===========================================================================
# INFRASTRUCTURE — logging
# ===========================================================================

def infra_logging():

    w("src/infrastructure/logging/log_formatter.py", '''\
from datetime import datetime
import json, yaml, os


def _log_dir(fmt: str) -> str:
    d = os.path.join("logs", fmt)
    os.makedirs(d, exist_ok=True)
    return d


def append_json_log(entry: dict):
    path = os.path.join(_log_dir("json"), "apollo_iam.json")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\\n")


def append_yaml_log(entry: dict):
    path = os.path.join(_log_dir("yaml"), "apollo_iam.yaml")
    with open(path, "a", encoding="utf-8") as f:
        yaml.dump([entry], f, allow_unicode=True, default_flow_style=False)


def append_md_log(entry: dict):
    path = os.path.join(_log_dir("md"), "apollo_iam.md")
    ts = entry.get("timestamp", datetime.utcnow().isoformat())
    level = entry.get("level", "INFO")
    msg = entry.get("message", "")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"| {ts} | {level} | {msg} |\\n")
''')

    w("src/infrastructure/logging/console_logger.py", '''\
from rich.console import Console
from rich.theme import Theme
from datetime import datetime

_theme = Theme({
    "info":    "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error":   "bold red",
    "debug":   "dim white",
})

console = Console(theme=_theme)


def log(level: str, message: str, emoji: str = "📋"):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    style = level.lower()
    console.print(f"[{style}]{emoji} [{ts}] [{level.upper()}] {message}[/{style}]")


def info(msg: str):    log("info",    msg, "ℹ️ ")
def success(msg: str): log("success", msg, "✅")
def warning(msg: str): log("warning", msg, "⚠️ ")
def error(msg: str):   log("error",   msg, "❌")
def debug(msg: str):   log("debug",   msg, "🔍")
''')

    w("src/infrastructure/logging/file_logger.py", '''\
from datetime import datetime
from src.infrastructure.logging.log_formatter import append_json_log, append_yaml_log, append_md_log


def write_log(level: str, message: str, extra: dict | None = None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level.upper(),
        "message": message,
        **(extra or {}),
    }
    append_json_log(entry)
    append_yaml_log(entry)
    append_md_log(entry)
''')


# ===========================================================================
# INFRASTRUCTURE — seed
# ===========================================================================

def infra_seed():

    w("src/infrastructure/seed/seed_admin.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.config.settings import get_settings
import uuid

settings = get_settings()
hasher = BcryptPasswordHasher()


def seed_admin(db: Session):
    existing = db.query(UserModel).filter_by(username=settings.admin_username).first()
    if existing:
        return
    role = db.query(RoleModel).filter_by(name="superadmin").first()
    admin = UserModel(
        id=str(uuid.uuid4()),
        username=settings.admin_username,
        email="admin@apollo.local",
        hashed_password=hasher.hash(settings.admin_password),
        full_name="Administrator",
        is_active=True,
        is_superuser=True,
    )
    if role:
        admin.roles.append(role)
    db.add(admin)
    db.commit()
''')

    w("src/infrastructure/seed/seed_roles.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.config.constants import DEFAULT_ROLES
import uuid


def seed_roles(db: Session):
    for name in DEFAULT_ROLES:
        if not db.query(RoleModel).filter_by(name=name).first():
            db.add(RoleModel(id=str(uuid.uuid4()), name=name, description=f"Role {name}"))
    db.commit()
''')

    w("src/infrastructure/seed/seed_permissions.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.permission_model import PermissionModel
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.config.constants import DEFAULT_PERMISSIONS
import uuid


def seed_permissions(db: Session):
    for name, resource, action in DEFAULT_PERMISSIONS:
        if not db.query(PermissionModel).filter_by(name=name).first():
            db.add(PermissionModel(id=str(uuid.uuid4()), name=name,
                                   resource=resource, action=action))
    db.commit()
    # superadmin gets all permissions
    superadmin = db.query(RoleModel).filter_by(name="superadmin").first()
    if superadmin:
        all_perms = db.query(PermissionModel).all()
        for p in all_perms:
            if p not in superadmin.permissions:
                superadmin.permissions.append(p)
        db.commit()
''')


# ===========================================================================
# APPLICATION — DTOs
# ===========================================================================

def application_dtos():

    w("src/application/dtos/auth_dto.py", '''\
from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginInputDTO:
    username: str
    password: str
    ip_address: str = ""


@dataclass
class TokenOutputDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
''')

    w("src/application/dtos/user_dto.py", '''\
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CreateUserDTO:
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    role_names: list[str] = field(default_factory=list)


@dataclass
class UpdateUserDTO:
    user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None


@dataclass
class UserOutputDTO:
    id: str
    username: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    group_id: Optional[str]
    type_id: Optional[str]
    level_id: Optional[str]
    roles: list[str]
    created_at: str
    updated_at: str
''')

    w("src/application/dtos/role_dto.py", '''\
from dataclasses import dataclass


@dataclass
class CreateRoleDTO:
    name: str
    description: str = ""


@dataclass
class RoleOutputDTO:
    id: str
    name: str
    description: str
    is_active: bool
    permissions: list[str]
''')

    w("src/application/dtos/permission_dto.py", '''\
from dataclasses import dataclass


@dataclass
class CreatePermissionDTO:
    name: str
    resource: str
    action: str
    description: str = ""


@dataclass
class PermissionOutputDTO:
    id: str
    name: str
    resource: str
    action: str
    description: str
''')

    w("src/application/dtos/group_dto.py", '''\
from dataclasses import dataclass


@dataclass
class CreateGroupDTO:
    name: str
    description: str = ""


@dataclass
class GroupOutputDTO:
    id: str
    name: str
    description: str
    is_active: bool
''')

    w("src/application/dtos/rbac_dto.py", '''\
from dataclasses import dataclass


@dataclass
class CreateRbacAttributeDTO:
    key: str
    label: str
    value_type: str = "string"
    description: str = ""


@dataclass
class RbacAttributeOutputDTO:
    id: str
    key: str
    label: str
    value_type: str
    description: str
    is_active: bool


@dataclass
class AssignAttributeDTO:
    user_id: str
    attribute_key: str
    value: str
''')

    w("src/application/dtos/settings_dto.py", '''\
from dataclasses import dataclass


@dataclass
class SettingsOutputDTO:
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    allow_registration: bool
    max_login_attempts: int
    lockout_minutes: int


@dataclass
class UpdateSettingsDTO:
    access_token_expire_minutes: int | None = None
    refresh_token_expire_days: int | None = None
    allow_registration: bool | None = None
    max_login_attempts: int | None = None
    lockout_minutes: int | None = None
''')

    w("src/application/dtos/audit_dto.py", '''\
from dataclasses import dataclass
from typing import Optional


@dataclass
class AuditLogOutputDTO:
    id: str
    actor: str
    action: str
    resource: str
    resource_id: Optional[str]
    detail: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: str
''')


# ===========================================================================
# APPLICATION — use cases
# ===========================================================================

def application_use_cases():

    # ── AUTH ──────────────────────────────────────────────────────────────────
    w("src/application/use_cases/auth/login.py", '''\
from src.application.dtos.auth_dto import LoginInputDTO, TokenOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.token_service import TokenService
from src.domain.ports.audit_logger import AuditLogger
from src.domain.value_objects.token_payload import TokenPayload
from src.domain.entities.audit_log import AuditLog
from src.domain.exceptions.auth_exceptions import InvalidCredentialsError, InactiveUserError
from src.infrastructure.config.settings import get_settings
import uuid

settings = get_settings()


class LoginUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher,
                 tokens: TokenService, audit: AuditLogger):
        self._users = users
        self._hasher = hasher
        self._tokens = tokens
        self._audit = audit

    def execute(self, dto: LoginInputDTO) -> TokenOutputDTO:
        user = (self._users.find_by_username(dto.username)
                or self._users.find_by_email(dto.username))
        if not user or not self._hasher.verify(dto.password, user.hashed_password):
            self._audit.log(AuditLog(
                id=str(uuid.uuid4()), actor=dto.username, action="login_failed",
                resource="auth", detail="Invalid credentials", ip_address=dto.ip_address,
                status="failure",
            ))
            raise InvalidCredentialsError("Credenciais inválidas.")
        if not user.is_active:
            raise InactiveUserError("Usuário inativo.")

        payload = TokenPayload(
            sub=user.username,
            user_id=user.id,
            is_superuser=user.is_superuser,
            roles=user.roles,
            permissions=[],
            group=user.group_id,
            user_type=user.type_id,
            user_level=user.level_id,
            rbac=user.rbac_attributes,
        )
        access = self._tokens.create_access_token(payload)
        refresh = self._tokens.create_refresh_token(payload)
        self._audit.log(AuditLog(
            id=str(uuid.uuid4()), actor=user.username, action="login_success",
            resource="auth", ip_address=dto.ip_address,
        ))
        return TokenOutputDTO(
            access_token=access, refresh_token=refresh,
            expires_in=settings.access_token_expire_minutes * 60,
        )
''')

    w("src/application/use_cases/auth/refresh_token.py", '''\
from src.domain.ports.token_service import TokenService
from src.domain.exceptions.auth_exceptions import TokenInvalidError


class RefreshTokenUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, refresh_token: str) -> dict:
        payload = self._tokens.decode_token(refresh_token)
        new_access = self._tokens.create_access_token(payload)
        return {"access_token": new_access, "token_type": "bearer"}
''')

    w("src/application/use_cases/auth/logout.py", '''\
from src.domain.ports.token_service import TokenService


class LogoutUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, token: str) -> None:
        payload = self._tokens.decode_token(token)
        self._tokens.revoke_token(payload.jti)
''')

    w("src/application/use_cases/auth/validate_token.py", '''\
from src.domain.ports.token_service import TokenService
from src.domain.value_objects.token_payload import TokenPayload


class ValidateTokenUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, token: str) -> TokenPayload:
        return self._tokens.decode_token(token)
''')

    # ── USERS ─────────────────────────────────────────────────────────────────
    w("src/application/use_cases/users/create_user.py", '''\
from src.application.dtos.user_dto import CreateUserDTO, UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.value_objects.username import Username
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
import uuid


class CreateUserUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, dto: CreateUserDTO) -> UserOutputDTO:
        Username(dto.username)  # validates
        if self._users.find_by_username(dto.username):
            raise UserAlreadyExistsError(f"Username {dto.username!r} já existe.")
        if dto.email and self._users.find_by_email(dto.email):
            raise UserAlreadyExistsError(f"E-mail {dto.email!r} já existe.")
        user = User(
            id=str(uuid.uuid4()),
            username=dto.username,
            email=dto.email,
            hashed_password=self._hasher.hash(dto.password),
            full_name=dto.full_name,
            is_active=dto.is_active,
            is_superuser=dto.is_superuser,
            group_id=dto.group_id,
            type_id=dto.type_id,
            level_id=dto.level_id,
        )
        saved = self._users.save(user)
        return _to_output(saved)


def _to_output(u: User) -> UserOutputDTO:
    return UserOutputDTO(
        id=u.id, username=u.username, email=u.email, full_name=u.full_name,
        is_active=u.is_active, is_superuser=u.is_superuser,
        group_id=u.group_id, type_id=u.type_id, level_id=u.level_id,
        roles=u.roles, created_at=str(u.created_at), updated_at=str(u.updated_at),
    )
''')

    w("src/application/use_cases/users/update_user.py", '''\
from src.application.dtos.user_dto import UpdateUserDTO, UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class UpdateUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, dto: UpdateUserDTO) -> UserOutputDTO:
        user = self._users.find_by_id(dto.user_id)
        if not user:
            raise UserNotFoundError(dto.user_id)
        if dto.email is not None: user.email = dto.email
        if dto.full_name is not None: user.full_name = dto.full_name
        if dto.is_active is not None: user.is_active = dto.is_active
        if dto.group_id is not None: user.group_id = dto.group_id
        if dto.type_id is not None: user.type_id = dto.type_id
        if dto.level_id is not None: user.level_id = dto.level_id
        user.touch()
        saved = self._users.save(user)
        from src.application.use_cases.users.create_user import _to_output
        return _to_output(saved)
''')

    w("src/application/use_cases/users/delete_user.py", '''\
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class DeleteUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> None:
        if not self._users.find_by_id(user_id):
            raise UserNotFoundError(user_id)
        self._users.delete(user_id)
''')

    w("src/application/use_cases/users/get_user.py", '''\
from src.application.dtos.user_dto import UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError
from src.application.use_cases.users.create_user import _to_output


class GetUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> UserOutputDTO:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return _to_output(user)
''')

    w("src/application/use_cases/users/list_users.py", '''\
from src.application.dtos.user_dto import UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.application.use_cases.users.create_user import _to_output


class ListUsersUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, skip: int = 0, limit: int = 100) -> list[UserOutputDTO]:
        return [_to_output(u) for u in self._users.list_all(skip, limit)]
''')

    w("src/application/use_cases/users/change_password.py", '''\
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.exceptions.user_exceptions import UserNotFoundError
from src.domain.exceptions.auth_exceptions import InvalidCredentialsError


class ChangePasswordUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, user_id: str, old_password: str, new_password: str) -> None:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        if not self._hasher.verify(old_password, user.hashed_password):
            raise InvalidCredentialsError("Senha atual incorreta.")
        user.hashed_password = self._hasher.hash(new_password)
        user.touch()
        self._users.save(user)
''')

    w("src/application/use_cases/users/reset_password.py", '''\
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.exceptions.user_exceptions import UserNotFoundError


class ResetPasswordUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, user_id: str, new_password: str) -> None:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        user.hashed_password = self._hasher.hash(new_password)
        user.touch()
        self._users.save(user)
''')

    w("src/application/use_cases/users/toggle_user_status.py", '''\
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class ToggleUserStatusUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> bool:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        user.is_active = not user.is_active
        user.touch()
        self._users.save(user)
        return user.is_active
''')

    # ── ROLES ─────────────────────────────────────────────────────────────────
    w("src/application/use_cases/roles/create_role.py", '''\
from src.application.dtos.role_dto import CreateRoleDTO, RoleOutputDTO
from src.domain.ports.role_repository import RoleRepository
from src.domain.entities.role import Role
import uuid


class CreateRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, dto: CreateRoleDTO) -> RoleOutputDTO:
        role = Role(id=str(uuid.uuid4()), name=dto.name, description=dto.description)
        saved = self._roles.save(role)
        return RoleOutputDTO(id=saved.id, name=saved.name, description=saved.description,
                             is_active=saved.is_active, permissions=saved.permissions)
''')

    w("src/application/use_cases/roles/list_roles.py", '''\
from src.application.dtos.role_dto import RoleOutputDTO
from src.domain.ports.role_repository import RoleRepository


class ListRolesUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self) -> list[RoleOutputDTO]:
        return [RoleOutputDTO(id=r.id, name=r.name, description=r.description,
                              is_active=r.is_active, permissions=r.permissions)
                for r in self._roles.list_all()]
''')

    w("src/application/use_cases/roles/delete_role.py", '''\
from src.domain.ports.role_repository import RoleRepository
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


class DeleteRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, role_id: str) -> None:
        if not self._roles.find_by_id(role_id):
            raise RoleNotFoundError(role_id)
        self._roles.delete(role_id)
''')

    w("src/application/use_cases/roles/assign_role_to_user.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel


class AssignRoleToUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: str, role_id: str) -> None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        if user and role and role not in user.roles:
            user.roles.append(role)
            self.db.commit()
''')

    w("src/application/use_cases/roles/revoke_role_from_user.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.role_model import RoleModel


class RevokeRoleFromUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: str, role_id: str) -> None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        if user and role and role in user.roles:
            user.roles.remove(role)
            self.db.commit()
''')

    w("src/application/use_cases/roles/update_role.py", '''\
from src.domain.ports.role_repository import RoleRepository
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


class UpdateRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, role_id: str, name: str | None = None, description: str | None = None):
        role = self._roles.find_by_id(role_id)
        if not role:
            raise RoleNotFoundError(role_id)
        if name: role.name = name
        if description is not None: role.description = description
        return self._roles.save(role)
''')

    # ── PERMISSIONS ───────────────────────────────────────────────────────────
    w("src/application/use_cases/permissions/create_permission.py", '''\
from src.application.dtos.permission_dto import CreatePermissionDTO, PermissionOutputDTO
from src.domain.ports.permission_repository import PermissionRepository
from src.domain.entities.permission import Permission
import uuid


class CreatePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, dto: CreatePermissionDTO) -> PermissionOutputDTO:
        p = Permission(id=str(uuid.uuid4()), name=dto.name, resource=dto.resource,
                       action=dto.action, description=dto.description)
        saved = self._perms.save(p)
        return PermissionOutputDTO(id=saved.id, name=saved.name, resource=saved.resource,
                                   action=saved.action, description=saved.description)
''')

    w("src/application/use_cases/permissions/list_permissions.py", '''\
from src.application.dtos.permission_dto import PermissionOutputDTO
from src.domain.ports.permission_repository import PermissionRepository


class ListPermissionsUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self) -> list[PermissionOutputDTO]:
        return [PermissionOutputDTO(id=p.id, name=p.name, resource=p.resource,
                                    action=p.action, description=p.description)
                for p in self._perms.list_all()]
''')

    w("src/application/use_cases/permissions/delete_permission.py", '''\
from src.domain.ports.permission_repository import PermissionRepository
from src.domain.exceptions.rbac_exceptions import PermissionNotFoundError


class DeletePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, perm_id: str) -> None:
        if not self._perms.find_by_id(perm_id):
            raise PermissionNotFoundError(perm_id)
        self._perms.delete(perm_id)
''')

    w("src/application/use_cases/permissions/update_permission.py", '''\
from src.domain.ports.permission_repository import PermissionRepository
from src.domain.exceptions.rbac_exceptions import PermissionNotFoundError


class UpdatePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, perm_id: str, **kwargs):
        p = self._perms.find_by_id(perm_id)
        if not p:
            raise PermissionNotFoundError(perm_id)
        for k, v in kwargs.items():
            if v is not None:
                setattr(p, k, v)
        return self._perms.save(p)
''')

    w("src/application/use_cases/permissions/assign_permission_to_role.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.role_model import RoleModel
from src.infrastructure.database.models.permission_model import PermissionModel


class AssignPermissionToRoleUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, role_id: str, permission_id: str) -> None:
        role = self.db.query(RoleModel).filter_by(id=role_id).first()
        perm = self.db.query(PermissionModel).filter_by(id=permission_id).first()
        if role and perm and perm not in role.permissions:
            role.permissions.append(perm)
            self.db.commit()
''')

    # ── GROUPS ────────────────────────────────────────────────────────────────
    w("src/application/use_cases/groups/create_group.py", '''\
from src.application.dtos.group_dto import CreateGroupDTO, GroupOutputDTO
from src.domain.ports.group_repository import GroupRepository
from src.domain.entities.group import Group
import uuid


class CreateGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, dto: CreateGroupDTO) -> GroupOutputDTO:
        g = Group(id=str(uuid.uuid4()), name=dto.name, description=dto.description)
        saved = self._groups.save(g)
        return GroupOutputDTO(id=saved.id, name=saved.name,
                              description=saved.description, is_active=saved.is_active)
''')

    w("src/application/use_cases/groups/list_groups.py", '''\
from src.application.dtos.group_dto import GroupOutputDTO
from src.domain.ports.group_repository import GroupRepository


class ListGroupsUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self) -> list[GroupOutputDTO]:
        return [GroupOutputDTO(id=g.id, name=g.name, description=g.description,
                               is_active=g.is_active)
                for g in self._groups.list_all()]
''')

    w("src/application/use_cases/groups/delete_group.py", '''\
from src.domain.ports.group_repository import GroupRepository
from src.domain.exceptions.rbac_exceptions import GroupNotFoundError


class DeleteGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, group_id: str) -> None:
        if not self._groups.find_by_id(group_id):
            raise GroupNotFoundError(group_id)
        self._groups.delete(group_id)
''')

    w("src/application/use_cases/groups/update_group.py", '''\
from src.domain.ports.group_repository import GroupRepository
from src.domain.exceptions.rbac_exceptions import GroupNotFoundError


class UpdateGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, group_id: str, name: str | None = None, description: str | None = None):
        g = self._groups.find_by_id(group_id)
        if not g:
            raise GroupNotFoundError(group_id)
        if name: g.name = name
        if description is not None: g.description = description
        return self._groups.save(g)
''')

    w("src/application/use_cases/groups/assign_user_to_group.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.database.models.user_model import UserModel


class AssignUserToGroupUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, user_id: str, group_id: str) -> None:
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user:
            user.group_id = group_id
            self.db.commit()
''')

    # ── RBAC ATTRIBUTES ───────────────────────────────────────────────────────
    w("src/application/use_cases/rbac/create_attribute.py", '''\
from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, RbacAttributeOutputDTO
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.entities.rbac_attribute import RbacAttribute
import uuid


class CreateRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, dto: CreateRbacAttributeDTO) -> RbacAttributeOutputDTO:
        attr = RbacAttribute(id=str(uuid.uuid4()), key=dto.key, label=dto.label,
                             value_type=dto.value_type, description=dto.description)
        saved = self._repo.save(attr)
        return RbacAttributeOutputDTO(id=saved.id, key=saved.key, label=saved.label,
                                      value_type=saved.value_type, description=saved.description,
                                      is_active=saved.is_active)
''')

    w("src/application/use_cases/rbac/list_attributes.py", '''\
from src.application.dtos.rbac_dto import RbacAttributeOutputDTO
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository


class ListRbacAttributesUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self) -> list[RbacAttributeOutputDTO]:
        return [RbacAttributeOutputDTO(id=a.id, key=a.key, label=a.label,
                                       value_type=a.value_type, description=a.description,
                                       is_active=a.is_active)
                for a in self._repo.list_all()]
''')

    w("src/application/use_cases/rbac/delete_attribute.py", '''\
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.exceptions.rbac_exceptions import AttributeNotFoundError


class DeleteRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, attr_id: str) -> None:
        if not self._repo.find_by_id(attr_id):
            raise AttributeNotFoundError(attr_id)
        self._repo.delete(attr_id)
''')

    w("src/application/use_cases/rbac/update_attribute.py", '''\
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.exceptions.rbac_exceptions import AttributeNotFoundError


class UpdateRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, attr_id: str, **kwargs):
        attr = self._repo.find_by_id(attr_id)
        if not attr:
            raise AttributeNotFoundError(attr_id)
        for k, v in kwargs.items():
            if v is not None:
                setattr(attr, k, v)
        return self._repo.save(attr)
''')

    w("src/application/use_cases/rbac/assign_attribute_to_user.py", '''\
from sqlalchemy.orm import Session
from src.application.dtos.rbac_dto import AssignAttributeDTO
from src.infrastructure.database.models.user_model import UserModel, user_rbac_values
from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel
from sqlalchemy import insert, delete


class AssignAttributeToUserUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, dto: AssignAttributeDTO) -> None:
        attr = self.db.query(RbacAttributeModel).filter_by(key=dto.attribute_key).first()
        if not attr:
            return
        self.db.execute(
            delete(user_rbac_values).where(
                user_rbac_values.c.user_id == dto.user_id,
                user_rbac_values.c.attribute_id == attr.id,
            )
        )
        self.db.execute(
            insert(user_rbac_values).values(
                user_id=dto.user_id, attribute_id=attr.id, value=dto.value
            )
        )
        self.db.commit()
''')

    # ── SETTINGS ──────────────────────────────────────────────────────────────
    w("src/application/use_cases/settings/get_settings.py", '''\
from sqlalchemy.orm import Session
from src.application.dtos.settings_dto import SettingsOutputDTO
from src.infrastructure.database.models.settings_model import SettingsModel


class GetSettingsUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self) -> SettingsOutputDTO:
        s = self.db.query(SettingsModel).filter_by(id="singleton").first()
        if not s:
            s = SettingsModel(id="singleton")
            self.db.add(s); self.db.commit()
        return SettingsOutputDTO(
            access_token_expire_minutes=s.access_token_expire_minutes,
            refresh_token_expire_days=s.refresh_token_expire_days,
            allow_registration=s.allow_registration,
            max_login_attempts=s.max_login_attempts,
            lockout_minutes=s.lockout_minutes,
        )
''')

    w("src/application/use_cases/settings/update_settings.py", '''\
from sqlalchemy.orm import Session
from src.application.dtos.settings_dto import UpdateSettingsDTO, SettingsOutputDTO
from src.infrastructure.database.models.settings_model import SettingsModel


class UpdateSettingsUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, dto: UpdateSettingsDTO) -> SettingsOutputDTO:
        s = self.db.query(SettingsModel).filter_by(id="singleton").first()
        if not s:
            s = SettingsModel(id="singleton")
            self.db.add(s)
        if dto.access_token_expire_minutes is not None:
            s.access_token_expire_minutes = dto.access_token_expire_minutes
        if dto.refresh_token_expire_days is not None:
            s.refresh_token_expire_days = dto.refresh_token_expire_days
        if dto.allow_registration is not None:
            s.allow_registration = dto.allow_registration
        if dto.max_login_attempts is not None:
            s.max_login_attempts = dto.max_login_attempts
        if dto.lockout_minutes is not None:
            s.lockout_minutes = dto.lockout_minutes
        self.db.commit()
        from src.application.use_cases.settings.get_settings import GetSettingsUseCase
        return GetSettingsUseCase(self.db).execute()
''')


# ===========================================================================
# INTERFACE — API FastAPI
# ===========================================================================

def api_dependencies():
    w("src/interface/api/dependencies.py", '''\
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.domain.value_objects.token_payload import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_token_service(db: Session = Depends(get_db)) -> JwtTokenService:
    blacklist = SqliteTokenBlacklist(db)
    return JwtTokenService(blacklist)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    svc: JwtTokenService = Depends(get_token_service),
) -> TokenPayload:
    try:
        return svc.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token inválido ou expirado.")


def require_superuser(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if not current.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return current
''')


def api_schemas():
    w("src/interface/api/schemas/common_schema.py", '''\
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100
''')

    w("src/interface/api/schemas/auth_schema.py", '''\
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshRequest(BaseModel):
    refresh_token: str

class ValidateTokenRequest(BaseModel):
    token: str
''')

    w("src/interface/api/schemas/user_schema.py", '''\
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    role_names: list[str] = []

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    group_id: Optional[str]
    type_id: Optional[str]
    level_id: Optional[str]
    roles: list[str]
    created_at: str
    updated_at: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ResetPasswordRequest(BaseModel):
    new_password: str
''')

    w("src/interface/api/schemas/role_schema.py", '''\
from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: str = ""

class RoleResponse(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
    permissions: list[str]

class AssignRoleRequest(BaseModel):
    role_id: str
''')

    w("src/interface/api/schemas/permission_schema.py", '''\
from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    resource: str
    action: str
    description: str = ""

class PermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: str
    description: str

class AssignPermissionRequest(BaseModel):
    permission_id: str
''')

    w("src/interface/api/schemas/group_schema.py", '''\
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    description: str = ""

class GroupResponse(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
''')

    w("src/interface/api/schemas/rbac_schema.py", '''\
from pydantic import BaseModel


class RbacAttributeCreate(BaseModel):
    key: str
    label: str
    value_type: str = "string"
    description: str = ""

class RbacAttributeResponse(BaseModel):
    id: str
    key: str
    label: str
    value_type: str
    description: str
    is_active: bool

class AssignAttributeRequest(BaseModel):
    attribute_key: str
    value: str
''')

    w("src/interface/api/schemas/settings_schema.py", '''\
from pydantic import BaseModel
from typing import Optional


class SettingsResponse(BaseModel):
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    allow_registration: bool
    max_login_attempts: int
    lockout_minutes: int

class SettingsUpdate(BaseModel):
    access_token_expire_minutes: Optional[int] = None
    refresh_token_expire_days: Optional[int] = None
    allow_registration: Optional[bool] = None
    max_login_attempts: Optional[int] = None
    lockout_minutes: Optional[int] = None
''')

    w("src/interface/api/schemas/audit_schema.py", '''\
from pydantic import BaseModel
from typing import Optional


class AuditLogResponse(BaseModel):
    id: str
    actor: str
    action: str
    resource: str
    resource_id: Optional[str]
    detail: Optional[str]
    ip_address: Optional[str]
    status: str
    created_at: str
''')


def api_routes():
    w("src/interface/api/routes/auth.py", '''\
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.application.use_cases.auth.login import LoginUseCase
from src.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from src.application.use_cases.auth.logout import LogoutUseCase
from src.application.use_cases.auth.validate_token import ValidateTokenUseCase
from src.application.dtos.auth_dto import LoginInputDTO
from src.interface.api.schemas.auth_schema import TokenResponse, RefreshRequest, ValidateTokenRequest
from src.interface.api.dependencies import get_current_user, oauth2_scheme
from fastapi import Depends as D

router = APIRouter(prefix="/auth", tags=["Auth"])


def _deps(db: Session = Depends(get_db)):
    bl = SqliteTokenBlacklist(db)
    return (SqliteUserRepository(db), BcryptPasswordHasher(),
            JwtTokenService(bl), SqliteAuditLogRepository(db))


@router.post("/token", response_model=TokenResponse, summary="Login — obter token JWT")
async def login(form: OAuth2PasswordRequestForm = Depends(), request: Request = None,
                db: Session = Depends(get_db)):
    users, hasher, tokens, audit = _deps(db)
    uc = LoginUseCase(users, hasher, tokens, audit)
    ip = request.client.host if request else ""
    result = uc.execute(LoginInputDTO(username=form.username, password=form.password, ip_address=ip))
    return result.__dict__


@router.post("/refresh", summary="Renovar access token")
async def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    return RefreshTokenUseCase(tokens).execute(body.refresh_token)


@router.post("/logout", summary="Revogar token")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    LogoutUseCase(tokens).execute(token)
    return {"message": "Logout realizado."}


@router.post("/validate", summary="Validar token e retornar payload")
async def validate(body: ValidateTokenRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    payload = ValidateTokenUseCase(tokens).execute(body.token)
    return payload.__dict__
''')

    w("src/interface/api/routes/token.py", '''\
# Alias público para /token (OAuth2 padrão)
from src.interface.api.routes.auth import router
''')

    w("src/interface/api/routes/admin/users.py", '''\
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.use_cases.users.update_user import UpdateUserUseCase
from src.application.use_cases.users.delete_user import DeleteUserUseCase
from src.application.use_cases.users.get_user import GetUserUseCase
from src.application.use_cases.users.list_users import ListUsersUseCase
from src.application.use_cases.users.change_password import ChangePasswordUseCase
from src.application.use_cases.users.reset_password import ResetPasswordUseCase
from src.application.use_cases.users.toggle_user_status import ToggleUserStatusUseCase
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.interface.api.schemas.user_schema import (
    UserCreate, UserUpdate, UserResponse, ChangePasswordRequest, ResetPasswordRequest
)
from src.interface.api.dependencies import require_superuser
from src.domain.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError

router = APIRouter(prefix="/admin/users", tags=["Admin — Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               _=Depends(require_superuser)):
    return [u.__dict__ for u in ListUsersUseCase(SqliteUserRepository(db)).execute(skip, limit)]


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    try:
        dto = CreateUserDTO(**body.model_dump())
        result = CreateUserUseCase(SqliteUserRepository(db), BcryptPasswordHasher()).execute(dto)
        return result.__dict__
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    try:
        return GetUserUseCase(SqliteUserRepository(db)).execute(user_id).__dict__
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UserUpdate, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    dto = UpdateUserDTO(user_id=user_id, **body.model_dump())
    return UpdateUserUseCase(SqliteUserRepository(db)).execute(dto).__dict__


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    DeleteUserUseCase(SqliteUserRepository(db)).execute(user_id)


@router.post("/{user_id}/toggle-status")
def toggle_status(user_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    active = ToggleUserStatusUseCase(SqliteUserRepository(db)).execute(user_id)
    return {"is_active": active}


@router.post("/{user_id}/reset-password")
def reset_password(user_id: str, body: ResetPasswordRequest, db: Session = Depends(get_db),
                   _=Depends(require_superuser)):
    ResetPasswordUseCase(SqliteUserRepository(db), BcryptPasswordHasher()).execute(
        user_id, body.new_password)
    return {"message": "Senha redefinida."}
''')

    w("src/interface/api/routes/admin/roles.py", '''\
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.role_repository_impl import SqliteRoleRepository
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.list_roles import ListRolesUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.roles.assign_role_to_user import AssignRoleToUserUseCase
from src.application.use_cases.roles.revoke_role_from_user import RevokeRoleFromUserUseCase
from src.application.dtos.role_dto import CreateRoleDTO
from src.interface.api.schemas.role_schema import RoleCreate, RoleResponse, AssignRoleRequest
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/roles", tags=["Admin — Roles"])


@router.get("/", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [r.__dict__ for r in ListRolesUseCase(SqliteRoleRepository(db)).execute()]


@router.post("/", response_model=RoleResponse, status_code=201)
def create_role(body: RoleCreate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    return CreateRoleUseCase(SqliteRoleRepository(db)).execute(
        CreateRoleDTO(name=body.name, description=body.description)).__dict__


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    DeleteRoleUseCase(SqliteRoleRepository(db)).execute(role_id)


@router.post("/{role_id}/assign-user/{user_id}")
def assign_role(role_id: str, user_id: str, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    AssignRoleToUserUseCase(db).execute(user_id, role_id)
    return {"message": "Role atribuída."}


@router.delete("/{role_id}/revoke-user/{user_id}")
def revoke_role(role_id: str, user_id: str, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    RevokeRoleFromUserUseCase(db).execute(user_id, role_id)
    return {"message": "Role revogada."}
''')

    w("src/interface/api/routes/admin/permissions.py", '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.permission_repository_impl import SqlitePermissionRepository
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.permissions.list_permissions import ListPermissionsUseCase
from src.application.use_cases.permissions.delete_permission import DeletePermissionUseCase
from src.application.use_cases.permissions.assign_permission_to_role import AssignPermissionToRoleUseCase
from src.application.dtos.permission_dto import CreatePermissionDTO
from src.interface.api.schemas.permission_schema import PermissionCreate, PermissionResponse, AssignPermissionRequest
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/permissions", tags=["Admin — Permissions"])


@router.get("/", response_model=list[PermissionResponse])
def list_perms(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [p.__dict__ for p in ListPermissionsUseCase(SqlitePermissionRepository(db)).execute()]


@router.post("/", response_model=PermissionResponse, status_code=201)
def create_perm(body: PermissionCreate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    dto = CreatePermissionDTO(name=body.name, resource=body.resource,
                              action=body.action, description=body.description)
    return CreatePermissionUseCase(SqlitePermissionRepository(db)).execute(dto).__dict__


@router.delete("/{perm_id}", status_code=204)
def delete_perm(perm_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    DeletePermissionUseCase(SqlitePermissionRepository(db)).execute(perm_id)


@router.post("/{perm_id}/assign-role/{role_id}")
def assign_perm(perm_id: str, role_id: str, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    AssignPermissionToRoleUseCase(db).execute(role_id, perm_id)
    return {"message": "Permissão atribuída."}
''')

    w("src/interface/api/routes/admin/groups.py", '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.group_repository_impl import SqliteGroupRepository
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.use_cases.groups.list_groups import ListGroupsUseCase
from src.application.use_cases.groups.delete_group import DeleteGroupUseCase
from src.application.use_cases.groups.assign_user_to_group import AssignUserToGroupUseCase
from src.application.dtos.group_dto import CreateGroupDTO
from src.interface.api.schemas.group_schema import GroupCreate, GroupResponse
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/groups", tags=["Admin — Groups"])


@router.get("/", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [g.__dict__ for g in ListGroupsUseCase(SqliteGroupRepository(db)).execute()]


@router.post("/", response_model=GroupResponse, status_code=201)
def create_group(body: GroupCreate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    return CreateGroupUseCase(SqliteGroupRepository(db)).execute(
        CreateGroupDTO(name=body.name, description=body.description)).__dict__


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    DeleteGroupUseCase(SqliteGroupRepository(db)).execute(group_id)


@router.post("/{group_id}/assign-user/{user_id}")
def assign_user(group_id: str, user_id: str, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    AssignUserToGroupUseCase(db).execute(user_id, group_id)
    return {"message": "Usuário adicionado ao grupo."}
''')

    w("src/interface/api/routes/admin/rbac_attributes.py", '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.rbac_attribute_repository_impl import SqliteRbacAttributeRepository
from src.application.use_cases.rbac.create_attribute import CreateRbacAttributeUseCase
from src.application.use_cases.rbac.list_attributes import ListRbacAttributesUseCase
from src.application.use_cases.rbac.delete_attribute import DeleteRbacAttributeUseCase
from src.application.use_cases.rbac.assign_attribute_to_user import AssignAttributeToUserUseCase
from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, AssignAttributeDTO
from src.interface.api.schemas.rbac_schema import RbacAttributeCreate, RbacAttributeResponse, AssignAttributeRequest
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/rbac", tags=["Admin — RBAC Attributes"])


@router.get("/", response_model=list[RbacAttributeResponse])
def list_attrs(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return [a.__dict__ for a in ListRbacAttributesUseCase(SqliteRbacAttributeRepository(db)).execute()]


@router.post("/", response_model=RbacAttributeResponse, status_code=201)
def create_attr(body: RbacAttributeCreate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    dto = CreateRbacAttributeDTO(key=body.key, label=body.label,
                                  value_type=body.value_type, description=body.description)
    return CreateRbacAttributeUseCase(SqliteRbacAttributeRepository(db)).execute(dto).__dict__


@router.delete("/{attr_id}", status_code=204)
def delete_attr(attr_id: str, db: Session = Depends(get_db), _=Depends(require_superuser)):
    DeleteRbacAttributeUseCase(SqliteRbacAttributeRepository(db)).execute(attr_id)


@router.post("/assign/{user_id}")
def assign_attr(user_id: str, body: AssignAttributeRequest, db: Session = Depends(get_db),
                _=Depends(require_superuser)):
    AssignAttributeToUserUseCase(db).execute(
        AssignAttributeDTO(user_id=user_id, attribute_key=body.attribute_key, value=body.value))
    return {"message": "Atributo atribuído."}
''')

    w("src/interface/api/routes/admin/settings.py", '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.application.use_cases.settings.get_settings import GetSettingsUseCase
from src.application.use_cases.settings.update_settings import UpdateSettingsUseCase
from src.application.dtos.settings_dto import UpdateSettingsDTO
from src.interface.api.schemas.settings_schema import SettingsResponse, SettingsUpdate
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/settings", tags=["Admin — Settings"])


@router.get("/", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db), _=Depends(require_superuser)):
    return GetSettingsUseCase(db).execute().__dict__


@router.put("/", response_model=SettingsResponse)
def update_settings(body: SettingsUpdate, db: Session = Depends(get_db), _=Depends(require_superuser)):
    dto = UpdateSettingsDTO(**body.model_dump())
    return UpdateSettingsUseCase(db).execute(dto).__dict__
''')

    w("src/interface/api/routes/admin/audit_logs.py", '''\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.interface.api.schemas.audit_schema import AuditLogResponse
from src.interface.api.dependencies import require_superuser

router = APIRouter(prefix="/admin/audit", tags=["Admin — Audit Logs"])


@router.get("/", response_model=list[AuditLogResponse])
def list_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
              _=Depends(require_superuser)):
    repo = SqliteAuditLogRepository(db)
    return [{"id": l.id, "actor": l.actor, "action": l.action, "resource": l.resource,
             "resource_id": l.resource_id, "detail": l.detail, "ip_address": l.ip_address,
             "status": l.status, "created_at": str(l.created_at)}
            for l in repo.list_logs(skip, limit)]
''')


def api_main():
    w("src/interface/api/main.py", '''\
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.connection import init_db
from src.infrastructure.seed.seed_roles import seed_roles
from src.infrastructure.seed.seed_permissions import seed_permissions
from src.infrastructure.seed.seed_admin import seed_admin
from src.infrastructure.database.connection import SessionLocal
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

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Serviço centralizado de IAM + RBAC — O2 Data Solutions",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(perms_router)
app.include_router(groups_router)
app.include_router(rbac_router)
app.include_router(settings_router)
app.include_router(audit_router)


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_permissions(db)
        seed_admin(db)
    finally:
        db.close()
    success(f"🚀 {settings.app_name} v{settings.app_version} iniciado!")
    info("📖 Docs: http://localhost:8000/docs")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
''')


# ===========================================================================
# INTERFACE — Web App (Jinja2 + CSS + JS)
# ===========================================================================

def webapp_css():
    w("src/interface/webapp/static/css/variables.css", """\
:root {
  --primary: #f97316;
  --primary-dark: #ea580c;
  --primary-light: #fed7aa;
  --gradient: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #c2410c 100%);
  --bg: #0f172a;
  --bg-card: #1e293b;
  --bg-sidebar: #1e293b;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --border: #334155;
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #f59e0b;
  --info: #3b82f6;
  --radius: 10px;
  --shadow: 0 4px 24px rgba(0,0,0,0.4);
}
""")

    w("src/interface/webapp/static/css/main.css", """\
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import 'variables.css';

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}

/* ── Layout ── */
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 260px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; left: 0; bottom: 0;
  z-index: 100;
}

.sidebar-logo {
  padding: 24px 20px;
  background: var(--gradient);
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-logo span { font-size: 1.1rem; font-weight: 700; color: #fff; }

.sidebar-nav { flex: 1; padding: 16px 0; overflow-y: auto; }

.nav-section { padding: 8px 20px 4px; font-size: .7rem; font-weight: 600;
  color: var(--text-muted); text-transform: uppercase; letter-spacing: .08em; }

.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 20px; color: var(--text-muted);
  text-decoration: none; font-size: .9rem; transition: all .2s;
  border-left: 3px solid transparent;
}

.nav-item:hover, .nav-item.active {
  color: var(--primary); background: rgba(249,115,22,.08);
  border-left-color: var(--primary);
}

.main-content {
  margin-left: 260px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Navbar ── */
.navbar {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky; top: 0; z-index: 50;
}

.navbar-title { font-size: 1.1rem; font-weight: 600; }

.navbar-user {
  display: flex; align-items: center; gap: 10px;
  font-size: .9rem; color: var(--text-muted);
}

.avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--gradient);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: #fff; font-size: .85rem;
}

/* ── Page ── */
.page { padding: 28px 32px; flex: 1; }

.page-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 24px;
}

.page-title { font-size: 1.5rem; font-weight: 700; }

/* ── Cards ── */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
}

.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap: 16px; margin-bottom: 28px; }

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  display: flex; align-items: center; gap: 16px;
}

.stat-icon {
  width: 48px; height: 48px; border-radius: 12px;
  background: var(--gradient);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.4rem;
}

.stat-value { font-size: 1.8rem; font-weight: 700; }
.stat-label { font-size: .8rem; color: var(--text-muted); }

/* ── Table ── */
.table-wrap { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; font-size: .9rem; }

th {
  text-align: left; padding: 12px 16px;
  background: rgba(255,255,255,.04);
  color: var(--text-muted); font-weight: 600;
  border-bottom: 1px solid var(--border);
  font-size: .8rem; text-transform: uppercase; letter-spacing: .05em;
}

td { padding: 12px 16px; border-bottom: 1px solid var(--border); vertical-align: middle; }

tr:hover td { background: rgba(249,115,22,.04); }

/* ── Badges ── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 20px; font-size: .75rem; font-weight: 600;
}
.badge-success { background: rgba(34,197,94,.15); color: var(--success); }
.badge-danger  { background: rgba(239,68,68,.15);  color: var(--danger); }
.badge-info    { background: rgba(59,130,246,.15);  color: var(--info); }
.badge-warning { background: rgba(245,158,11,.15);  color: var(--warning); }
.badge-primary { background: rgba(249,115,22,.15);  color: var(--primary); }

/* ── Buttons ── */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 18px; border-radius: 8px; font-size: .875rem;
  font-weight: 500; cursor: pointer; border: none; transition: all .2s;
  text-decoration: none;
}
.btn-primary { background: var(--gradient); color: #fff; }
.btn-primary:hover { opacity: .9; transform: translateY(-1px); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { border-color: var(--primary); color: var(--primary); }
.btn-danger { background: rgba(239,68,68,.15); color: var(--danger); border: 1px solid rgba(239,68,68,.3); }
.btn-danger:hover { background: var(--danger); color: #fff; }
.btn-sm { padding: 5px 12px; font-size: .8rem; }

/* ── Forms ── */
.form-group { margin-bottom: 18px; }
.form-label { display: block; margin-bottom: 6px; font-size: .875rem; font-weight: 500; color: var(--text-muted); }
.form-control {
  width: 100%; padding: 10px 14px;
  background: rgba(255,255,255,.05);
  border: 1px solid var(--border);
  border-radius: 8px; color: var(--text); font-size: .9rem;
  transition: border-color .2s;
}
.form-control:focus { outline: none; border-color: var(--primary); }
.form-control option { background: var(--bg-card); }

/* ── Login ── */
.login-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex; align-items: center; justify-content: center;
}

.login-card {
  width: 100%; max-width: 420px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  box-shadow: var(--shadow);
}

.login-logo {
  text-align: center; margin-bottom: 32px;
}

.login-logo .logo-icon {
  width: 64px; height: 64px; border-radius: 16px;
  background: var(--gradient);
  display: flex; align-items: center; justify-content: center;
  font-size: 2rem; margin: 0 auto 12px;
}

.login-logo h1 { font-size: 1.4rem; font-weight: 700; }
.login-logo p  { font-size: .85rem; color: var(--text-muted); margin-top: 4px; }

/* ── Footer ── */
.footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  padding: 16px 32px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: .8rem; color: var(--text-muted);
}

.footer-brand { display: flex; align-items: center; gap: 6px; }
.footer-brand span { color: var(--primary); font-weight: 600; }

/* ── Alerts ── */
.alert {
  padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px; font-size: .875rem;
}
.alert-error   { background: rgba(239,68,68,.1);  border: 1px solid rgba(239,68,68,.3);  color: #fca5a5; }
.alert-success { background: rgba(34,197,94,.1);  border: 1px solid rgba(34,197,94,.3);  color: #86efac; }
.alert-info    { background: rgba(59,130,246,.1); border: 1px solid rgba(59,130,246,.3); color: #93c5fd; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
""")


def webapp_js():
    w("src/interface/webapp/static/js/api.js", """\
const API_BASE = 'http://localhost:8000';

async function apiRequest(method, path, body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API_BASE + path, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Erro na requisição');
  }
  return res.status === 204 ? null : res.json();
}

function getToken() { return localStorage.getItem('apollo_token'); }
function setToken(t) { localStorage.setItem('apollo_token', t); }
function clearToken() { localStorage.removeItem('apollo_token'); }
""")

    w("src/interface/webapp/static/js/main.js", """\
document.addEventListener('DOMContentLoaded', () => {
  // highlight active nav item
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.getAttribute('href') && path.startsWith(el.getAttribute('href'))) {
      el.classList.add('active');
    }
  });

  // auto-dismiss alerts
  document.querySelectorAll('.alert[data-dismiss]').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });

  // confirm delete
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });
});
""")




# ===========================================================================
# RELATÓRIO FINAL
# ===========================================================================

def _report(files_written: list, start: float):
    import time
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    init(autoreset=True)
    console = Console()
    elapsed = time.time() - start

    total_bytes = sum(os.path.getsize(f) for f in files_written if os.path.exists(f))

    table = Table(title="🚀 Populate Concluído", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan")
    table.add_column("Valor", style="bold green")
    table.add_row("📄 Arquivos populados", str(len(files_written)))
    table.add_row("💾 Bytes escritos", f"{total_bytes / 1024:.1f} KB")
    table.add_row("⏱️  Tempo de execução", f"{elapsed:.2f}s")
    console.print(table)

    console.print(Panel.fit(
        "[bold green]✅ Todos os arquivos foram populados![/bold green]\n"
        "[dim]Próximo passo: execute [bold]python fix-v1.py[/bold] e depois [bold]python fix-v2.py[/bold][/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    import time
    _start = time.time()
    _written = []

    def w_tracked(rel, content):
        full_path = os.path.join(BASE, rel)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        _written.append(full_path)

    # replace w globally for tracking
    import sys
    sys.modules[__name__].__dict__["w"] = w_tracked

    root_files()
    domain_entities()
    domain_value_objects()
    domain_events()
    domain_exceptions()
    domain_ports()
    infra_config()
    infra_database()
    infra_models()
    infra_security()
    infra_repositories()
    infra_logging()
    infra_seed()
    application_dtos()
    application_use_cases()
    api_dependencies()
    api_schemas()
    api_routes()

    _report(_written, _start)
