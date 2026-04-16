"""
jwt_service.py
Serviço JWT com cache em memória para decode_token.
- decode_token: cache do payload por hash do token (TTL = tempo restante do token)
- create/revoke: sem cache (operações de escrita)
O2 Data Solutions
"""
from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.domain.ports.token_service import TokenService
from src.domain.value_objects.token_payload import TokenPayload
from src.domain.exceptions.auth_exceptions import TokenExpiredError, TokenInvalidError
from src.infrastructure.config.settings import get_settings
from src.infrastructure.cache.memory_cache import token_cache

settings = get_settings()


def _token_key(token: str) -> str:
    """Hash SHA-256 truncado do token — evita armazenar o token completo como chave."""
    return hashlib.sha256(token.encode()).hexdigest()[:32]


def _payload_to_dict(p: TokenPayload) -> dict:
    return {
        "sub": p.sub, "user_id": p.user_id, "is_superuser": p.is_superuser,
        "roles": p.roles, "permissions": p.permissions,
        "group": p.group, "group_id": p.group_id,
        "user_type": p.user_type, "user_level": p.user_level,
        "user_level_rank": p.user_level_rank,
        "rbac": p.rbac, "abac": p.abac,
        "exp": p.exp, "iat": p.iat, "jti": p.jti,
    }


def _dict_to_payload(d: dict) -> TokenPayload:
    return TokenPayload(
        sub=d["sub"], user_id=d["user_id"], is_superuser=d["is_superuser"],
        roles=d["roles"], permissions=d["permissions"],
        group=d.get("group"), group_id=d.get("group_id"),
        user_type=d.get("user_type"), user_level=d.get("user_level"),
        user_level_rank=d.get("user_level_rank", 0),
        rbac=d.get("rbac", {}), abac=d.get("abac", {}),
        exp=d.get("exp", 0), iat=d.get("iat", 0), jti=d.get("jti", ""),
    )


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
        cache_key = _token_key(token)

        # L1: cache — evita decode JWT + query blacklist a cada request
        cached = token_cache.get(cache_key)
        if cached is not None:
            return _dict_to_payload(cached)

        # decode JWT
        try:
            data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except JWTError as exc:
            if "expired" in str(exc).lower():
                raise TokenExpiredError() from exc
            raise TokenInvalidError() from exc

        jti = data.get("jti", "")

        # verifica blacklist (já tem cache interno em SqliteTokenBlacklist)
        if self._blacklist and self._blacklist.is_revoked(jti):
            raise TokenInvalidError("Token revogado.")

        payload = TokenPayload(
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

        # armazena no cache com TTL = tempo restante do token (máx 30s para segurança)
        import time as _time
        remaining = max(0.0, data.get("exp", 0) - _time.time())
        cache_ttl = min(remaining, 30.0)
        if cache_ttl > 1.0:
            token_cache.set(cache_key, _payload_to_dict(payload), ttl=cache_ttl)

        return payload

    def revoke_token(self, jti: str) -> None:
        if self._blacklist:
            self._blacklist.revoke(jti)
        # invalida o cache de tokens que contenham este jti
        # (não temos o token raw aqui, mas o blacklist_cache já foi atualizado)

    def is_revoked(self, jti: str) -> bool:
        return self._blacklist.is_revoked(jti) if self._blacklist else False
