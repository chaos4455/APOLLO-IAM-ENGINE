from src.domain.entities.user import User


def test_user_defaults():
    u = User(username="joao", hashed_password="hash")
    assert u.is_active is True
    assert u.is_superuser is False
    assert u.roles == []
    assert u.id != ""


def test_user_touch_updates_timestamp():
    import time
    u = User(username="maria", hashed_password="h")
    before = u.updated_at
    time.sleep(0.01)
    u.touch()
    assert u.updated_at >= before


def test_user_rbac_attributes_default_empty():
    u = User(username="x", hashed_password="h")
    assert u.rbac_attributes == {}
