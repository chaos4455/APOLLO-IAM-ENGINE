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
