import pytest
from unittest.mock import MagicMock
from src.application.use_cases.auth.login import LoginUseCase
from src.application.dtos.auth_dto import LoginInputDTO
from src.domain.entities.user import User
from src.domain.exceptions.auth_exceptions import InvalidCredentialsError, InactiveUserError


def _make_user(active=True):
    return User(
        id="u1", username="joao", hashed_password="hashed",
        is_active=active, is_superuser=False,
    )


def test_login_success():
    users = MagicMock()
    users.find_by_username.return_value = _make_user()
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = True
    tokens = MagicMock()
    tokens.create_access_token.return_value = "access_tok"
    tokens.create_refresh_token.return_value = "refresh_tok"
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    result = uc.execute(LoginInputDTO(username="joao", password="senha"))

    assert result.access_token == "access_tok"
    assert result.refresh_token == "refresh_tok"
    audit.log.assert_called_once()


def test_login_wrong_password():
    users = MagicMock()
    users.find_by_username.return_value = _make_user()
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = False
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InvalidCredentialsError):
        uc.execute(LoginInputDTO(username="joao", password="errada"))


def test_login_user_not_found():
    users = MagicMock()
    users.find_by_username.return_value = None
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = False
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InvalidCredentialsError):
        uc.execute(LoginInputDTO(username="naoexiste", password="x"))


def test_login_inactive_user():
    users = MagicMock()
    users.find_by_username.return_value = _make_user(active=False)
    users.find_by_email.return_value = None
    hasher = MagicMock()
    hasher.verify.return_value = True
    tokens = MagicMock()
    audit = MagicMock()

    uc = LoginUseCase(users, hasher, tokens, audit)
    with pytest.raises(InactiveUserError):
        uc.execute(LoginInputDTO(username="joao", password="senha"))
