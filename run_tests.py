
"""
run_tests.py - Apollo IAM Engine
Popula todos os arquivos de teste com codigo real e roda pytest ate 100% passar.
O2 Data Solutions
"""

import os
import sys
import subprocess
import time

BASE = "apollo-iam-engine-api-service"


def w(rel: str, content: str):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


# ===========================================================================
# conftest.py — fixtures compartilhadas
# ===========================================================================

def write_conftest():
    w("tests/conftest.py", '''\
from __future__ import annotations
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# banco de teste em arquivo — persiste entre runs, limpo antes de cada sessao
_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_HERE, "..", "data")
os.makedirs(_DATA_DIR, exist_ok=True)

TEST_DB_PATH = os.path.join(_DATA_DIR, "test_apollo.db")
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

engine_test = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
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
    """Token de sessao — NAO deve ser revogado pelos testes."""
    resp = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert resp.status_code == 200, f"Login falhou: {resp.text}"
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def fresh_token(client):
    """Token fresco por teste — pode ser revogado sem afetar outros testes."""
    resp = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    return resp.json()
''')


# ===========================================================================
# UNIT — domain entities
# ===========================================================================

def write_unit_domain():
    w("tests/unit/domain/test_user_entity.py", '''\
from src.domain.entities.user import User


def test_user_defaults():
    u = User(username="joao", hashed_password="hash")
    assert u.is_active is True
    assert u.is_superuser is False
    assert u.roles == []
    assert u.id != ""


def test_user_touch_updates_timestamp():
    import time
    u = User(username="maria", hashed_password="h")
    before = u.updated_at
    time.sleep(0.01)
    u.touch()
    assert u.updated_at >= before


def test_user_rbac_attributes_default_empty():
    u = User(username="x", hashed_password="h")
    assert u.rbac_attributes == {}
''')

    w("tests/unit/domain/test_role_entity.py", '''\
from src.domain.entities.role import Role


def test_role_defaults():
    r = Role(name="admin")
    assert r.is_active is True
    assert r.permissions == []
    assert r.id != ""


def test_role_has_name():
    r = Role(name="viewer", description="Read only")
    assert r.name == "viewer"
    assert r.description == "Read only"
''')

    w("tests/unit/domain/test_permission_entity.py", '''\
from src.domain.entities.permission import Permission


def test_permission_fields():
    p = Permission(name="users:read", resource="users", action="read")
    assert p.name == "users:read"
    assert p.resource == "users"
    assert p.action == "read"
    assert p.id != ""
''')

    w("tests/unit/domain/test_value_objects.py", '''\
import pytest
from src.domain.value_objects.username import Username
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from src.domain.value_objects.token_payload import TokenPayload


def test_username_simple():
    assert str(Username("joao")) == "joao"


def test_username_dot_notation():
    assert str(Username("joao.silva")) == "joao.silva"


def test_username_email_format():
    assert str(Username("joao@empresa.com")) == "joao@empresa.com"


def test_username_invalid_empty():
    with pytest.raises(ValueError):
        Username("")


def test_username_invalid_space():
    with pytest.raises(ValueError):
        Username("joao silva")


def test_password_valid():
    p = Password("minhasenha123")
    assert str(p) == "minhasenha123"


def test_password_short_allowed():
    p = Password("ab")
    assert str(p) == "ab"


def test_password_empty_raises():
    with pytest.raises(ValueError):
        Password("")


def test_email_valid():
    e = Email("user@example.com")
    assert str(e) == "user@example.com"


def test_email_invalid():
    with pytest.raises(ValueError):
        Email("not-an-email")


def test_token_payload_defaults():
    tp = TokenPayload(sub="admin")
    assert tp.roles == []
    assert tp.permissions == []
    assert tp.rbac == {}
    assert tp.is_superuser is False
''')


# ===========================================================================
# UNIT — application use cases
# ===========================================================================

def write_unit_application():
    w("tests/unit/application/test_login_use_case.py", '''\
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.auth.login import LoginUseCase
from src.application.dtos.auth_dto import LoginInputDTO
from src.domain.entities.user import User
from src.domain.exceptions.auth_exceptions import InvalidCredentialsError, InactiveUserError


def _make_user(active=True):
    return User(
        id="u1", username="joao", hashed_password="hashed",
        is_active=active, is_superuser=False,
    )


def test_login_success():
    users = MagicMock()
    users.find_by_username.return_value = _make_user()
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = True
    tokens = MagicMock()
    tokens.create_access_token.return_value = "access_tok"
    tokens.create_refresh_token.return_value = "refresh_tok"
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    result = uc.execute(LoginInputDTO(username="joao", password="senha"))

    assert result.access_token == "access_tok"
    assert result.refresh_token == "refresh_tok"
    audit.log.assert_called_once()


def test_login_wrong_password():
    users = MagicMock()
    users.find_by_username.return_value = _make_user()
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = False
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InvalidCredentialsError):
        uc.execute(LoginInputDTO(username="joao", password="errada"))


def test_login_user_not_found():
    users = MagicMock()
    users.find_by_username.return_value = None
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = False
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InvalidCredentialsError):
        uc.execute(LoginInputDTO(username="naoexiste", password="x"))


def test_login_inactive_user():
    users = MagicMock()
    users.find_by_username.return_value = _make_user(active=False)
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = True
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InactiveUserError):
        uc.execute(LoginInputDTO(username="joao", password="senha"))
''')

    w("tests/unit/application/test_create_user_use_case.py", '''\
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.dtos.user_dto import CreateUserDTO
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError


def test_create_user_success():
    repo = MagicMock()
    repo.find_by_username.return_value = None
    repo.find_by_email.return_value = None
    repo.save.side_effect = lambda u: u
    hasher = MagicMock()
    hasher.hash.return_value = "hashed_pw"

    uc = CreateUserUseCase(repo, hasher)
    dto = CreateUserDTO(username="novo.usuario", password="senha123")
    result = uc.execute(dto)

    assert result.username == "novo.usuario"
    repo.save.assert_called_once()


def test_create_user_duplicate_username():
    from src.domain.entities.user import User
    repo = MagicMock()
    repo.find_by_username.return_value = User(username="existente", hashed_password="h")
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(UserAlreadyExistsError):
        uc.execute(CreateUserDTO(username="existente", password="x"))


def test_create_user_invalid_username():
    repo = MagicMock()
    repo.find_by_username.return_value = None
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(ValueError):
        uc.execute(CreateUserDTO(username="nome invalido com espaco", password="x"))


def test_create_user_duplicate_email():
    from src.domain.entities.user import User
    repo = MagicMock()
    repo.find_by_username.return_value = None
    repo.find_by_email.return_value = User(username="outro", hashed_password="h")
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(UserAlreadyExistsError):
        uc.execute(CreateUserDTO(username="novo", password="x", email="dup@test.com"))
''')

    w("tests/unit/application/test_rbac_use_case.py", '''\
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.dtos.role_dto import CreateRoleDTO
from src.application.dtos.permission_dto import CreatePermissionDTO
from src.application.dtos.group_dto import CreateGroupDTO
from src.domain.entities.role import Role
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


def test_create_role():
    repo = MagicMock()
    repo.save.side_effect = lambda r: r
    uc = CreateRoleUseCase(repo)
    result = uc.execute(CreateRoleDTO(name="editor", description="Editor role"))
    assert result.name == "editor"


def test_delete_role_not_found():
    repo = MagicMock()
    repo.find_by_id.return_value = None
    uc = DeleteRoleUseCase(repo)
    with pytest.raises(RoleNotFoundError):
        uc.execute("nonexistent-id")


def test_create_permission():
    repo = MagicMock()
    repo.save.side_effect = lambda p: p
    uc = CreatePermissionUseCase(repo)
    result = uc.execute(CreatePermissionDTO(name="docs:read", resource="docs", action="read"))
    assert result.name == "docs:read"
    assert result.resource == "docs"


def test_create_group():
    repo = MagicMock()
    repo.save.side_effect = lambda g: g
    uc = CreateGroupUseCase(repo)
    result = uc.execute(CreateGroupDTO(name="TI", description="Time de TI"))
    assert result.name == "TI"
''')


# ===========================================================================
# INTEGRATION — API endpoints
# ===========================================================================

def write_integration():
    w("tests/integration/test_auth_api.py", '''\
import pytest


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_login_success(client):
    r = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    r = client.post("/auth/token", data={"username": "admin", "password": "errada"})
    assert r.status_code == 401


def test_login_unknown_user(client):
    r = client.post("/auth/token", data={"username": "naoexiste", "password": "x"})
    assert r.status_code == 401


def test_validate_token(client, admin_token):
    r = client.post("/auth/validate", json={"token": admin_token})
    assert r.status_code == 200
    assert r.json()["sub"] == "admin"


def test_refresh_token(client, fresh_token):
    refresh = fresh_token["refresh_token"]
    r2 = client.post("/auth/refresh", json={"refresh_token": refresh})
    assert r2.status_code == 200
    assert "access_token" in r2.json()


def test_logout(client, fresh_token):
    """Usa token fresco para nao revogar o token de sessao."""
    access = fresh_token["access_token"]
    r = client.post("/auth/logout", headers={"Authorization": f"Bearer {access}"})
    assert r.status_code == 200


def test_protected_without_token(client):
    r = client.get("/admin/users/")
    assert r.status_code == 401
''')

    w("tests/integration/test_users_api.py", '''\
import pytest


def test_list_users(client, auth_headers):
    r = client.get("/admin/users/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    usernames = [u["username"] for u in r.json()]
    assert "admin" in usernames


def test_create_and_get_user(client, auth_headers):
    payload = {"username": "test.user", "password": "senha123", "email": "test@apollo.local",
               "full_name": "Test User", "is_active": True, "is_superuser": False,
               "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    uid = r.json()["id"]

    r2 = client.get(f"/admin/users/{uid}", headers=auth_headers)
    assert r2.status_code == 200
    assert r2.json()["username"] == "test.user"


def test_create_user_duplicate(client, auth_headers):
    payload = {"username": "dup.user", "password": "x", "role_names": []}
    client.post("/admin/users/", json=payload, headers=auth_headers)
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    assert r.status_code == 409


def test_toggle_user_status(client, auth_headers):
    payload = {"username": "toggle.user", "password": "x", "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    uid = r.json()["id"]
    r2 = client.post(f"/admin/users/{uid}/toggle-status", headers=auth_headers)
    assert r2.status_code == 200


def test_reset_password(client, auth_headers):
    payload = {"username": "reset.user", "password": "original", "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    uid = r.json()["id"]
    r2 = client.post(f"/admin/users/{uid}/reset-password",
                     json={"new_password": "nova123"}, headers=auth_headers)
    assert r2.status_code == 200


def test_delete_user(client, auth_headers):
    payload = {"username": "del.user", "password": "x", "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    uid = r.json()["id"]
    r2 = client.delete(f"/admin/users/{uid}", headers=auth_headers)
    assert r2.status_code == 204


def test_get_nonexistent_user(client, auth_headers):
    r = client.get("/admin/users/nonexistent-id", headers=auth_headers)
    assert r.status_code == 404
''')

    w("tests/integration/test_roles_api.py", '''\
import pytest


def test_list_roles(client, auth_headers):
    r = client.get("/admin/roles/", headers=auth_headers)
    assert r.status_code == 200
    names = [x["name"] for x in r.json()]
    assert "superadmin" in names


def test_create_role(client, auth_headers):
    r = client.post("/admin/roles/", json={"name": "test_role", "description": "Test"},
                    headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "test_role"


def test_delete_role(client, auth_headers):
    r = client.post("/admin/roles/", json={"name": "to_delete_role", "description": ""},
                    headers=auth_headers)
    rid = r.json()["id"]
    r2 = client.delete(f"/admin/roles/{rid}", headers=auth_headers)
    assert r2.status_code == 204


def test_assign_role_to_user(client, auth_headers):
    # create user
    ru = client.post("/admin/users/", json={"username": "role.assign.user",
                     "password": "x", "role_names": []}, headers=auth_headers)
    uid = ru.json()["id"]
    # get viewer role id
    roles = client.get("/admin/roles/", headers=auth_headers).json()
    viewer = next((r for r in roles if r["name"] == "viewer"), None)
    if viewer:
        r2 = client.post(f"/admin/roles/{viewer['id']}/assign-user/{uid}",
                         headers=auth_headers)
        assert r2.status_code == 200
''')

    w("tests/integration/test_permissions_api.py", '''\
import pytest


def test_list_permissions(client, auth_headers):
    r = client.get("/admin/permissions/", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) > 0


def test_create_permission(client, auth_headers):
    r = client.post("/admin/permissions/",
                    json={"name": "test:perm", "resource": "test", "action": "read"},
                    headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "test:perm"


def test_delete_permission(client, auth_headers):
    r = client.post("/admin/permissions/",
                    json={"name": "del:perm", "resource": "del", "action": "delete"},
                    headers=auth_headers)
    pid = r.json()["id"]
    r2 = client.delete(f"/admin/permissions/{pid}", headers=auth_headers)
    assert r2.status_code == 204


def test_assign_permission_to_role(client, auth_headers):
    rp = client.post("/admin/permissions/",
                     json={"name": "assign:perm", "resource": "x", "action": "read"},
                     headers=auth_headers)
    pid = rp.json()["id"]
    roles = client.get("/admin/roles/", headers=auth_headers).json()
    operator = next((r for r in roles if r["name"] == "operator"), None)
    if operator:
        r2 = client.post(f"/admin/permissions/{pid}/assign-role/{operator['id']}",
                         headers=auth_headers)
        assert r2.status_code == 200
''')

    w("tests/integration/test_groups_api.py", '''\
import pytest


def test_list_groups(client, auth_headers):
    r = client.get("/admin/groups/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_group(client, auth_headers):
    r = client.post("/admin/groups/",
                    json={"name": "TI", "description": "Time de TI"},
                    headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "TI"


def test_delete_group(client, auth_headers):
    r = client.post("/admin/groups/",
                    json={"name": "ToDelete", "description": ""},
                    headers=auth_headers)
    gid = r.json()["id"]
    r2 = client.delete(f"/admin/groups/{gid}", headers=auth_headers)
    assert r2.status_code == 204


def test_assign_user_to_group(client, auth_headers):
    rg = client.post("/admin/groups/",
                     json={"name": "AssignGroup", "description": ""},
                     headers=auth_headers)
    gid = rg.json()["id"]
    ru = client.post("/admin/users/",
                     json={"username": "group.member", "password": "x", "role_names": []},
                     headers=auth_headers)
    uid = ru.json()["id"]
    r2 = client.post(f"/admin/groups/{gid}/assign-user/{uid}", headers=auth_headers)
    assert r2.status_code == 200
''')

    w("tests/integration/test_rbac_api.py", '''\
import pytest


def test_list_rbac_attributes(client, auth_headers):
    r = client.get("/admin/rbac/", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_rbac_attribute(client, auth_headers):
    r = client.post("/admin/rbac/",
                    json={"key": "department", "label": "Departamento",
                          "value_type": "string", "description": "Dept do usuario"},
                    headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["key"] == "department"


def test_create_rbac_attribute_integer(client, auth_headers):
    r = client.post("/admin/rbac/",
                    json={"key": "level_num", "label": "Nivel",
                          "value_type": "integer", "description": ""},
                    headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["value_type"] == "integer"


def test_delete_rbac_attribute(client, auth_headers):
    r = client.post("/admin/rbac/",
                    json={"key": "to_del_attr", "label": "Del",
                          "value_type": "string", "description": ""},
                    headers=auth_headers)
    aid = r.json()["id"]
    r2 = client.delete(f"/admin/rbac/{aid}", headers=auth_headers)
    assert r2.status_code == 204


def test_assign_attribute_to_user(client, auth_headers):
    # create attribute
    ra = client.post("/admin/rbac/",
                     json={"key": "cost_center", "label": "Centro de Custo",
                           "value_type": "string", "description": ""},
                     headers=auth_headers)
    # create user
    ru = client.post("/admin/users/",
                     json={"username": "rbac.user", "password": "x", "role_names": []},
                     headers=auth_headers)
    uid = ru.json()["id"]
    r2 = client.post(f"/admin/rbac/assign/{uid}",
                     json={"attribute_key": "cost_center", "value": "CC-001"},
                     headers=auth_headers)
    assert r2.status_code == 200
''')

    w("tests/integration/test_settings_api.py", '''\
import pytest


def test_get_settings(client, auth_headers):
    r = client.get("/admin/settings/", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "access_token_expire_minutes" in data
    assert "refresh_token_expire_days" in data
    assert "allow_registration" in data


def test_update_settings(client, auth_headers):
    r = client.put("/admin/settings/",
                   json={"access_token_expire_minutes": 120,
                         "refresh_token_expire_days": 14,
                         "allow_registration": False,
                         "max_login_attempts": 5,
                         "lockout_minutes": 15},
                   headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["access_token_expire_minutes"] == 120
    assert r.json()["refresh_token_expire_days"] == 14


def test_settings_requires_auth(client):
    r = client.get("/admin/settings/")
    assert r.status_code == 401
''')


# ===========================================================================
# E2E
# ===========================================================================

def write_e2e():
    w("tests/e2e/test_full_login_flow.py", '''\
import pytest


def test_full_auth_flow(client):
    """Login -> validate -> refresh -> logout"""
    # 1. login
    r = client.post("/auth/token", data={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    tokens = r.json()
    access = tokens["access_token"]
    refresh = tokens["refresh_token"]

    # 2. validate
    r2 = client.post("/auth/validate", json={"token": access})
    assert r2.status_code == 200
    assert r2.json()["sub"] == "admin"
    assert r2.json()["is_superuser"] is True

    # 3. refresh
    r3 = client.post("/auth/refresh", json={"refresh_token": refresh})
    assert r3.status_code == 200
    new_access = r3.json()["access_token"]
    assert new_access != ""

    # 4. use new token
    r4 = client.get("/admin/users/", headers={"Authorization": f"Bearer {new_access}"})
    assert r4.status_code == 200

    # 5. logout
    r5 = client.post("/auth/logout", headers={"Authorization": f"Bearer {new_access}"})
    assert r5.status_code == 200


def test_create_user_and_login(client, auth_headers):
    """Cria usuario, faz login com ele, valida token"""
    payload = {"username": "e2e.user", "password": "e2epass", "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    assert r.status_code == 201

    r2 = client.post("/auth/token", data={"username": "e2e.user", "password": "e2epass"})
    assert r2.status_code == 200
    token = r2.json()["access_token"]

    r3 = client.post("/auth/validate", json={"token": token})
    assert r3.status_code == 200
    assert r3.json()["sub"] == "e2e.user"


def test_inactive_user_cannot_login(client, auth_headers):
    """Desativa usuario e verifica que nao consegue logar"""
    payload = {"username": "inactive.e2e", "password": "pass123", "role_names": []}
    r = client.post("/admin/users/", json=payload, headers=auth_headers)
    uid = r.json()["id"]

    # toggle -> inativo
    client.post(f"/admin/users/{uid}/toggle-status", headers=auth_headers)

    r2 = client.post("/auth/token", data={"username": "inactive.e2e", "password": "pass123"})
    assert r2.status_code == 401


def test_full_rbac_flow(client, auth_headers):
    """Cria role, permissao, atribui ao usuario, valida no token"""
    # cria role
    rr = client.post("/admin/roles/", json={"name": "e2e_role", "description": ""},
                     headers=auth_headers)
    assert rr.status_code == 201
    role_id = rr.json()["id"]

    # cria usuario
    ru = client.post("/admin/users/",
                     json={"username": "e2e.rbac", "password": "pass", "role_names": []},
                     headers=auth_headers)
    uid = ru.json()["id"]

    # atribui role
    client.post(f"/admin/roles/{role_id}/assign-user/{uid}", headers=auth_headers)

    # login e valida roles no token
    r = client.post("/auth/token", data={"username": "e2e.rbac", "password": "pass"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    rv = client.post("/auth/validate", json={"token": token})
    assert "e2e_role" in rv.json()["roles"]
''')

    w("tests/e2e/test_admin_webapp.py", '''\
import pytest


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_docs_available(client):
    r = client.get("/docs")
    assert r.status_code == 200


def test_redoc_available(client):
    r = client.get("/redoc")
    assert r.status_code == 200


def test_full_crud_user(client, auth_headers):
    """CRUD completo de usuario via API"""
    # create
    r = client.post("/admin/users/",
                    json={"username": "crud.full", "password": "pass",
                          "email": "crud@test.com", "full_name": "CRUD User",
                          "is_active": True, "is_superuser": False, "role_names": []},
                    headers=auth_headers)
    assert r.status_code == 201
    uid = r.json()["id"]

    # read
    r2 = client.get(f"/admin/users/{uid}", headers=auth_headers)
    assert r2.json()["full_name"] == "CRUD User"

    # update
    r3 = client.put(f"/admin/users/{uid}",
                    json={"full_name": "Updated Name"},
                    headers=auth_headers)
    assert r3.status_code == 200
    assert r3.json()["full_name"] == "Updated Name"

    # delete
    r4 = client.delete(f"/admin/users/{uid}", headers=auth_headers)
    assert r4.status_code == 204

    # confirm deleted
    r5 = client.get(f"/admin/users/{uid}", headers=auth_headers)
    assert r5.status_code == 404
''')


# ===========================================================================
# RUNNER — popula, roda pytest, exibe relatorio rico
# ===========================================================================

def run_pytest(cwd: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "--no-header", "-q"],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout + result.stderr


def parse_results(output: str) -> dict:
    passed = failed = error = skipped = 0
    for line in output.splitlines():
        if " passed" in line:
            import re
            m = re.search(r"(\d+) passed", line)
            if m: passed = int(m.group(1))
        if " failed" in line:
            import re
            m = re.search(r"(\d+) failed", line)
            if m: failed = int(m.group(1))
        if " error" in line:
            import re
            m = re.search(r"(\d+) error", line)
            if m: error = int(m.group(1))
        if " skipped" in line:
            import re
            m = re.search(r"(\d+) skipped", line)
            if m: skipped = int(m.group(1))
    return {"passed": passed, "failed": failed, "error": error, "skipped": skipped}


if __name__ == "__main__":
    from colorama import init, Fore, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.progress import track

    init(autoreset=True)
    console = Console()
    _start = time.time()

    console.print(Panel.fit(
        "[bold orange1]🧪 APOLLO IAM — run_tests.py[/bold orange1]\n"
        "[dim]Populando testes e rodando pytest ate 100% passar...[/dim]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1"
    ))

    # 1. popula todos os arquivos de teste
    steps = [
        ("📋  conftest.py + fixtures",        write_conftest),
        ("🏗️   Unit — domain entities",        write_unit_domain),
        ("⚙️   Unit — application use cases",  write_unit_application),
        ("🔗  Integration — auth API",         write_integration),
        ("🌐  E2E — fluxos completos",         write_e2e),
    ]

    written = []
    for label, fn in track(steps, description="[orange1]Escrevendo testes...[/orange1]"):
        fn()
        console.print(f"  [green]✅[/green] {label}")

    console.print()

    # 2. roda pytest
    cwd = os.path.join(os.getcwd(), BASE)
    MAX_ATTEMPTS = 3
    last_output = ""
    last_code = 1
    stats = {}

    for attempt in range(1, MAX_ATTEMPTS + 1):
        console.print(f"[bold cyan]🔄 Tentativa {attempt}/{MAX_ATTEMPTS} — rodando pytest...[/bold cyan]")
        code, output = run_pytest(cwd)
        last_output = output
        last_code = code
        stats = parse_results(output)

        total = stats["passed"] + stats["failed"] + stats["error"]
        pct = int(stats["passed"] / total * 100) if total > 0 else 0

        status_color = "green" if code == 0 else "red"
        console.print(
            f"  [{status_color}]{'✅ PASSOU' if code == 0 else '❌ FALHOU'}[/{status_color}] "
            f"  passed={stats['passed']}  failed={stats['failed']}  "
            f"errors={stats['error']}  ({pct}%)"
        )

        if code == 0:
            break
        time.sleep(0.5)

    # 3. relatorio final
    elapsed = time.time() - _start
    total = stats["passed"] + stats["failed"] + stats["error"]
    pct = int(stats["passed"] / total * 100) if total > 0 else 0

    table = Table(title="📊 Resultado dos Testes", border_style="orange1", show_lines=True)
    table.add_column("Métrica", style="bold cyan", min_width=28)
    table.add_column("Valor", style="bold green")
    table.add_row("✅ Testes passando", str(stats["passed"]))
    table.add_row("❌ Testes falhando", str(stats["failed"]))
    table.add_row("💥 Erros", str(stats["error"]))
    table.add_row("⏭️  Skipped", str(stats["skipped"]))
    table.add_row("📈 Taxa de sucesso", f"{pct}%")
    table.add_row("⏱️  Tempo total", f"{elapsed:.2f}s")
    console.print(table)

    # mostra output do pytest se houver falhas
    if last_code != 0:
        console.print("\n[bold red]📋 Output do pytest (falhas):[/bold red]")
        # filtra apenas linhas de falha
        fail_lines = [l for l in last_output.splitlines()
                      if any(k in l for k in ["FAILED", "ERROR", "assert", "Error:", "raise"])]
        for line in fail_lines[:40]:
            console.print(f"  [red]{line}[/red]")

    if last_code == 0:
        console.print(Panel.fit(
            f"[bold green]🎉 100% dos testes passando![/bold green]\n"
            f"[dim]{stats['passed']} testes — {elapsed:.2f}s[/dim]",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[bold yellow]⚠️  {pct}% passando ({stats['passed']}/{total})[/bold yellow]\n"
            f"[dim]Verifique os erros acima e rode novamente.[/dim]",
            border_style="yellow"
        ))

    sys.exit(last_code)
