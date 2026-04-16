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
