from __future__ import annotations
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.domain.ports.token_service import TokenService
from src.domain.value_objects.token_payload import TokenPayload
from src.domain.exceptions.auth_exceptions import TokenExpiredError, TokenInvalidError
from src.infrastructure.config.settings import get_settings

settings = get_settings()


class JwtTokenService(TokenService):
    def __init__(self, blacklist=None):
        self._blacklist = blacklist

    def _build_claims(self, payload: TokenPayload, expire_delta: timedelta) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "sub":              payload.sub,
            "user_id":          payload.user_id,
            "is_superuser":     payload.is_superuser,
            "roles":            payload.roles,
            "permissions":      payload.permissions,
            "group":            payload.group,
            "group_id":         payload.group_id,
            "user_type":        payload.user_type,
            "user_level":       payload.user_level,
            "user_level_rank":  payload.user_level_rank,
            "rbac":             payload.rbac,
            "abac":             payload.abac,
            "iat":              int(now.timestamp()),
            "exp":              int((now + expire_delta).timestamp()),
            "jti":              str(uuid.uuid4()),
        }

    def create_access_token(self, payload: TokenPayload) -> str:
        claims = self._build_claims(
            payload, timedelta(minutes=settings.access_token_expire_minutes)
        )
        return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)

    def create_refresh_token(self, payload: TokenPayload) -> str:
        claims = self._build_claims(
            payload, timedelta(days=settings.refresh_token_expire_days)
        )
        claims["type"] = "refresh"
        return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except JWTError as exc:
            if "expired" in str(exc).lower():
                raise TokenExpiredError() from exc
            raise TokenInvalidError() from exc
        jti = data.get("jti", "")
        if self._blacklist and self._blacklist.is_revoked(jti):
            raise TokenInvalidError("Token revogado.")
        return TokenPayload(
            sub=data["sub"],
            user_id=data.get("user_id", ""),
            is_superuser=data.get("is_superuser", False),
            roles=data.get("roles", []),
            permissions=data.get("permissions", []),
            group=data.get("group"),
            group_id=data.get("group_id"),
            user_type=data.get("user_type"),
            user_level=data.get("user_level"),
            user_level_rank=data.get("user_level_rank", 0),
            rbac=data.get("rbac", {}),
            abac=data.get("abac", {}),
            exp=data.get("exp", 0),
            iat=data.get("iat", 0),
            jti=jti,
        )

    def revoke_token(self, jti: str) -> None:
        if self._blacklist:
            self._blacklist.revoke(jti)

    def is_revoked(self, jti: str) -> bool:
        return self._blacklist.is_revoked(jti) if self._blacklist else False
