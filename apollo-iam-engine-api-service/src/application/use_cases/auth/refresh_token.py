from src.domain.ports.token_service import TokenService
from src.domain.exceptions.auth_exceptions import TokenInvalidError


class RefreshTokenUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, refresh_token: str) -> dict:
        payload = self._tokens.decode_token(refresh_token)
        new_access = self._tokens.create_access_token(payload)
        return {"access_token": new_access, "token_type": "bearer"}
