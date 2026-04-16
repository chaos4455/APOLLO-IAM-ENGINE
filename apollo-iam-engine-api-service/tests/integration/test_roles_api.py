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
