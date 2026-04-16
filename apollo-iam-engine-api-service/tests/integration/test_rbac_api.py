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
