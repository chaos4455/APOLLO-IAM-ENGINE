class InvalidCredentialsError(Exception):
    """Credenciais inválidas."""

class TokenExpiredError(Exception):
    """Token expirado."""

class TokenInvalidError(Exception):
    """Token inválido ou revogado."""

class InactiveUserError(Exception):
    """Usuário inativo."""
