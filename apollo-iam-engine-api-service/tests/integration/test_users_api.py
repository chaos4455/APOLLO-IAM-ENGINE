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
