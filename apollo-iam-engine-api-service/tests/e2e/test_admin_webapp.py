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
