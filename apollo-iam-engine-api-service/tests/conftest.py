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
