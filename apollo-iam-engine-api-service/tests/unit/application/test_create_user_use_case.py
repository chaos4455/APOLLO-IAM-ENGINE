import pytest
from unittest.mock import MagicMock
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.dtos.user_dto import CreateUserDTO
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError


def test_create_user_success():
    repo = MagicMock()
    repo.find_by_username.return_value = None
    repo.find_by_email.return_value = None
    repo.save.side_effect = lambda u: u
    hasher = MagicMock()
    hasher.hash.return_value = "hashed_pw"

    uc = CreateUserUseCase(repo, hasher)
    dto = CreateUserDTO(username="novo.usuario", password="senha123")
    result = uc.execute(dto)

    assert result.username == "novo.usuario"
    repo.save.assert_called_once()


def test_create_user_duplicate_username():
    from src.domain.entities.user import User
    repo = MagicMock()
    repo.find_by_username.return_value = User(username="existente", hashed_password="h")
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(UserAlreadyExistsError):
        uc.execute(CreateUserDTO(username="existente", password="x"))


def test_create_user_invalid_username():
    repo = MagicMock()
    repo.find_by_username.return_value = None
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(ValueError):
        uc.execute(CreateUserDTO(username="nome invalido com espaco", password="x"))


def test_create_user_duplicate_email():
    from src.domain.entities.user import User
    repo = MagicMock()
    repo.find_by_username.return_value = None
    repo.find_by_email.return_value = User(username="outro", hashed_password="h")
    hasher = MagicMock()

    uc = CreateUserUseCase(repo, hasher)
    with pytest.raises(UserAlreadyExistsError):
        uc.execute(CreateUserDTO(username="novo", password="x", email="dup@test.com"))
