from src.domain.ports.token_service import TokenService


class LogoutUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, token: str) -> None:
        payload = self._tokens.decode_token(token)
        self._tokens.revoke_token(payload.jti)
