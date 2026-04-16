from src.domain.entities.permission import Permission


def test_permission_fields():
    p = Permission(name="users:read", resource="users", action="read")
    assert p.name == "users:read"
    assert p.resource == "users"
    assert p.action == "read"
    assert p.id != ""
