from src.domain.entities.role import Role


def test_role_defaults():
    r = Role(name="admin")
    assert r.is_active is True
    assert r.permissions == []
    assert r.id != ""


def test_role_has_name():
    r = Role(name="viewer", description="Read only")
    assert r.name == "viewer"
    assert r.description == "Read only"
