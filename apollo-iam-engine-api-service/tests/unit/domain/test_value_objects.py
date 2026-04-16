import pytest
from src.domain.value_objects.username import Username
from src.domain.value_objects.password import Password
from src.domain.value_objects.email import Email
from src.domain.value_objects.token_payload import TokenPayload


def test_username_simple():
    assert str(Username("joao")) == "joao"


def test_username_dot_notation():
    assert str(Username("joao.silva")) == "joao.silva"


def test_username_email_format():
    assert str(Username("joao@empresa.com")) == "joao@empresa.com"


def test_username_invalid_empty():
    with pytest.raises(ValueError):
        Username("")


def test_username_invalid_space():
    with pytest.raises(ValueError):
        Username("joao silva")


def test_password_valid():
    p = Password("minhasenha123")
    assert str(p) == "minhasenha123"


def test_password_short_allowed():
    p = Password("ab")
    assert str(p) == "ab"


def test_password_empty_raises():
    with pytest.raises(ValueError):
        Password("")


def test_email_valid():
    e = Email("user@example.com")
    assert str(e) == "user@example.com"


def test_email_invalid():
    with pytest.raises(ValueError):
        Email("not-an-email")


def test_token_payload_defaults():
    tp = TokenPayload(sub="admin")
    assert tp.roles == []
    assert tp.permissions == []
    assert tp.rbac == {}
    assert tp.is_superuser is False
