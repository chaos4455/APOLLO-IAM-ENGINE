from src.domain.ports.token_service import TokenService
from src.domain.value_objects.token_payload import TokenPayload


class ValidateTokenUseCase:
    def __init__(self, tokens: TokenService):
        self._tokens = tokens

    def execute(self, token: str) -> TokenPayload:
        return self._tokens.decode_token(token)
