class UserNotFoundError(Exception):
    """Usuário não encontrado."""

class UserAlreadyExistsError(Exception):
    """Usuário já existe."""

class InvalidUsernameError(Exception):
    """Username inválido."""
