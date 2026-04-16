from __future__ import annotations
from typing import Any, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infrastructure.database.connection import get_db
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.domain.value_objects.token_payload import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_token_service(db: Session = Depends(get_db)) -> JwtTokenService:
    return JwtTokenService(SqliteTokenBlacklist(db))


def get_current_user(
    token: str = Depends(oauth2_scheme),
    svc: JwtTokenService = Depends(get_token_service),
) -> TokenPayload:
    try:
        return svc.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token invalido ou expirado.")


def require_superuser(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if not current.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return current


def require_role(*roles: str) -> Callable:
    """Dependency factory: exige que o usuario tenha pelo menos uma das roles."""
    def _dep(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current.is_superuser:
            return current
        if not current.has_any_role(*roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requer uma das roles: {list(roles)}",
            )
        return current
    return _dep


def require_permission(*perms: str) -> Callable:
    """Dependency factory: exige que o usuario tenha pelo menos uma das permissoes."""
    def _dep(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current.is_superuser:
            return current
        if not any(current.has_permission(p) for p in perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requer uma das permissoes: {list(perms)}",
            )
        return current
    return _dep


def require_level(min_rank: int) -> Callable:
    """Dependency factory: exige nivel >= min_rank."""
    def _dep(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current.is_superuser:
            return current
        if not current.level_gte(min_rank):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Nivel insuficiente. Requer rank>={min_rank}.",
            )
        return current
    return _dep


def require_abac(**conditions: Any) -> Callable:
    """
    Dependency factory: verifica atributos ABAC do usuario.
    Exemplo: require_abac(sistema="cotacao", user_type="interno")
    """
    def _dep(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current.is_superuser:
            return current
        for key, expected in conditions.items():
            if not current.abac_match(key, expected):
                actual = current.abac.get(key, "<ausente>")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"ABAC negado: '{key}' esperado='{expected}' atual='{actual}'",
                )
        return current
    return _dep


def require_rbac_and_abac(roles: list[str] = None,
                           permissions: list[str] = None,
                           abac_conditions: dict[str, Any] = None,
                           min_level: int = None) -> Callable:
    """
    Dependency factory combinada RBAC + ABAC.
    Todos os criterios fornecidos devem ser satisfeitos.
    """
    def _dep(current: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if current.is_superuser:
            return current
        if roles and not current.has_any_role(*roles):
            raise HTTPException(status_code=403,
                                detail=f"Requer role: {roles}")
        if permissions and not any(current.has_permission(p) for p in permissions):
            raise HTTPException(status_code=403,
                                detail=f"Requer permissao: {permissions}")
        if abac_conditions:
            for key, val in abac_conditions.items():
                if not current.abac_match(key, val):
                    raise HTTPException(status_code=403,
                                        detail=f"ABAC negado: {key}={val}")
        if min_level is not None and not current.level_gte(min_level):
            raise HTTPException(status_code=403,
                                detail=f"Nivel insuficiente: requer rank>={min_level}")
        return current
    return _dep
