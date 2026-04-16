from sqlalchemy.orm import Session
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.application.use_cases.auth.login import LoginUseCase
from src.application.use_cases.auth.logout import LogoutUseCase
from src.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from src.application.use_cases.auth.validate_token import ValidateTokenUseCase
from src.application.dtos.auth_dto import LoginInputDTO, TokenOutputDTO
from src.domain.value_objects.token_payload import TokenPayload


class AuthService:
    """Orquestra os casos de uso de autenticação."""

    def __init__(self, db: Session):
        bl = SqliteTokenBlacklist(db)
        self._users = SqliteUserRepository(db)
        self._hasher = BcryptPasswordHasher()
        self._tokens = JwtTokenService(bl)
        self._audit = SqliteAuditLogRepository(db)

    def login(self, username: str, password: str, ip: str = "") -> TokenOutputDTO:
        uc = LoginUseCase(self._users, self._hasher, self._tokens, self._audit)
        return uc.execute(LoginInputDTO(username=username, password=password, ip_address=ip))

    def logout(self, token: str) -> None:
        LogoutUseCase(self._tokens).execute(token)

    def refresh(self, refresh_token: str) -> dict:
        return RefreshTokenUseCase(self._tokens).execute(refresh_token)

    def validate(self, token: str) -> TokenPayload:
        return ValidateTokenUseCase(self._tokens).execute(token)
