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
