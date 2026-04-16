from __future__ import annotations
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any, Optional
from src.infrastructure.database.connection import get_db
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.application.use_cases.auth.login import LoginUseCase
from src.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from src.application.use_cases.auth.logout import LogoutUseCase
from src.application.use_cases.auth.validate_token import ValidateTokenUseCase
from src.application.dtos.auth_dto import LoginInputDTO
from src.interface.api.schemas.auth_schema import TokenResponse, RefreshRequest, ValidateTokenRequest
from src.interface.api.dependencies import oauth2_scheme, get_current_user
from src.domain.value_objects.token_payload import TokenPayload
from src.infrastructure.logging import log_hooks as lh

router = APIRouter(prefix="/auth", tags=["Auth"])


def _deps(db: Session):
    bl = SqliteTokenBlacklist(db)
    return (SqliteUserRepository(db), BcryptPasswordHasher(),
            JwtTokenService(bl), SqliteAuditLogRepository(db))


@router.post("/token", response_model=TokenResponse, summary="Login — obter token JWT")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db),
):
    users, hasher, tokens, audit = _deps(db)
    # passa db para enriquecer token com ABAC
    uc = LoginUseCase(users, hasher, tokens, audit, db=db)
    ip = request.client.host if request and request.client else ""
    result = uc.execute(LoginInputDTO(username=form.username, password=form.password, ip_address=ip))
    lh.log_login_success(username=form.username, ip=ip, user_id=result.access_token[:8])
    return result.__dict__


@router.post("/refresh", summary="Renovar access token")
async def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    return RefreshTokenUseCase(tokens).execute(body.refresh_token)


@router.post("/logout", summary="Revogar token")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    LogoutUseCase(tokens).execute(token)
    lh.log_logout(username="token", jti=token[-8:])
    return {"message": "Logout realizado."}


@router.post("/validate", summary="Validar token e retornar payload completo")
async def validate(body: ValidateTokenRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    payload = ValidateTokenUseCase(tokens).execute(body.token)
    return {
        "sub":             payload.sub,
        "user_id":         payload.user_id,
        "is_superuser":    payload.is_superuser,
        "roles":           payload.roles,
        "permissions":     payload.permissions,
        "group":           payload.group,
        "group_id":        payload.group_id,
        "user_type":       payload.user_type,
        "user_level":      payload.user_level,
        "user_level_rank": payload.user_level_rank,
        "rbac":            payload.rbac,
        "abac":            payload.abac,
        "exp":             payload.exp,
        "iat":             payload.iat,
        "jti":             payload.jti,
    }


# ── /auth/check — verificacao RBAC+ABAC para sistemas externos ────────────────

class CheckRequest(BaseModel):
    token: str
    require_roles: Optional[list[str]] = None          # qualquer uma dessas roles
    require_all_roles: Optional[list[str]] = None      # todas essas roles
    require_permissions: Optional[list[str]] = None    # qualquer uma dessas permissoes
    require_abac: Optional[dict[str, Any]] = None      # todos esses atributos ABAC
    require_level_gte: Optional[int] = None            # nivel >= rank


class CheckResponse(BaseModel):
    allowed: bool
    reason: str
    subject: str
    roles: list[str]
    permissions: list[str]
    abac: dict
    user_level_rank: int


@router.post("/check", response_model=CheckResponse,
             summary="Verificar RBAC+ABAC — para sistemas externos")
async def check_access(body: CheckRequest, db: Session = Depends(get_db)):
    """
    Endpoint para sistemas externos verificarem se um token tem acesso.
    Combina RBAC (roles + permissions) com ABAC (atributos do usuario).
    Retorna allowed=true/false com o motivo.
    """
    _, _, tokens, _ = _deps(db)
    try:
        payload = ValidateTokenUseCase(tokens).execute(body.token)
    except Exception as e:
        lh.log_abac_check(actor="anonymous", allowed=False, reason=f"Token invalido: {str(e)}")
        return CheckResponse(
            allowed=False, reason=f"Token invalido: {str(e)}",
            subject="", roles=[], permissions=[], abac={}, user_level_rank=0,
        )

    # superuser passa em tudo
    if payload.is_superuser:
        lh.log_abac_check(actor=payload.sub, allowed=True, reason="superuser")
        return CheckResponse(
            allowed=True, reason="superuser",
            subject=payload.sub, roles=payload.roles,
            permissions=payload.permissions, abac=payload.abac,
            user_level_rank=payload.user_level_rank,
        )

    # verifica roles (qualquer uma)
    if body.require_roles:
        if not payload.has_any_role(*body.require_roles):
            return CheckResponse(
                allowed=False,
                reason=f"Requer uma das roles: {body.require_roles}. Usuario tem: {payload.roles}",
                subject=payload.sub, roles=payload.roles,
                permissions=payload.permissions, abac=payload.abac,
                user_level_rank=payload.user_level_rank,
            )

    # verifica roles (todas)
    if body.require_all_roles:
        missing = [r for r in body.require_all_roles if r not in payload.roles]
        if missing:
            return CheckResponse(
                allowed=False,
                reason=f"Faltam roles obrigatorias: {missing}",
                subject=payload.sub, roles=payload.roles,
                permissions=payload.permissions, abac=payload.abac,
                user_level_rank=payload.user_level_rank,
            )

    # verifica permissoes (qualquer uma)
    if body.require_permissions:
        if not any(payload.has_permission(p) for p in body.require_permissions):
            return CheckResponse(
                allowed=False,
                reason=f"Requer uma das permissoes: {body.require_permissions}",
                subject=payload.sub, roles=payload.roles,
                permissions=payload.permissions, abac=payload.abac,
                user_level_rank=payload.user_level_rank,
            )

    # verifica atributos ABAC
    if body.require_abac:
        for key, expected in body.require_abac.items():
            if not payload.abac_match(key, expected):
                actual = payload.abac.get(key, "<ausente>")
                return CheckResponse(
                    allowed=False,
                    reason=f"ABAC falhou: '{key}' esperado='{expected}' atual='{actual}'",
                    subject=payload.sub, roles=payload.roles,
                    permissions=payload.permissions, abac=payload.abac,
                    user_level_rank=payload.user_level_rank,
                )

    # verifica nivel minimo
    if body.require_level_gte is not None:
        if not payload.level_gte(body.require_level_gte):
            return CheckResponse(
                allowed=False,
                reason=f"Nivel insuficiente: requer rank>={body.require_level_gte}, usuario tem {payload.user_level_rank}",
                subject=payload.sub, roles=payload.roles,
                permissions=payload.permissions, abac=payload.abac,
                user_level_rank=payload.user_level_rank,
            )

    lh.log_abac_check(actor=payload.sub, allowed=True, reason="ok",
                      detail={"roles": payload.roles, "abac": payload.abac})
    return CheckResponse(
        allowed=True, reason="ok",
        subject=payload.sub, roles=payload.roles,
        permissions=payload.permissions, abac=payload.abac,
        user_level_rank=payload.user_level_rank,
    )
