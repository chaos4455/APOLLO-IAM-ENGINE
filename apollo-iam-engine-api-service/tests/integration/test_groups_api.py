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
