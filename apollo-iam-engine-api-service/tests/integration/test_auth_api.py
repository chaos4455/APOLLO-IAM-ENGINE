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
