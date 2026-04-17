# pep_middleware.py
# Policy Enforcement Point (PEP) — middleware FastAPI
# Aplica avaliacao APL automaticamente em rotas configuradas.
# Elias Andrade — O2 Data Solutions
#
# Uso:
#   app.add_middleware(PEPMiddleware, rules=[
#       PEPRule(path_prefix="/api/cotacoes", action="cotacao:read",
#               resource_template="cotacao/{path_suffix}",
#               tenant_id_header="X-Tenant-ID"),
#   ])
#
# O middleware:
#   1. Extrai o JWT do header Authorization
#   2. Monta o subject a partir do payload do token
#   3. Avalia a policy APL para (subject, action, resource, tenant_id)
#   4. Retorna 403 se negado, passa adiante se permitido
#   5. Adiciona X-APL-Decision e X-APL-Policy nos headers de resposta
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


@dataclass
class PEPRule:
    """Regra de enforcement: qual path, qual action, qual resource."""
    path_prefix: str                    # ex: "/api/cotacoes"
    action: str                         # ex: "cotacao:read"
    resource_template: str = "{path}"   # ex: "cotacao/{path_suffix}"
    tenant_id_header: str = "X-Tenant-ID"
    skip_superuser: bool = True         # superuser bypassa o PEP
    methods: list[str] = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE", "PATCH"])


class PEPMiddleware(BaseHTTPMiddleware):
    """
    Policy Enforcement Point como middleware ASGI.
    Intercepta requests e avalia policies APL antes de chegar no handler.

    Nao requer modificacao dos handlers existentes.
    Compativel com qualquer rota FastAPI/Starlette.
    """

    def __init__(self, app, rules: list[PEPRule] | None = None):
        super().__init__(app)
        self._rules = rules or []

    def _match_rule(self, path: str, method: str) -> PEPRule | None:
        for rule in self._rules:
            if path.startswith(rule.path_prefix) and method.upper() in rule.methods:
                return rule
        return None

    def _build_resource(self, rule: PEPRule, path: str) -> str:
        suffix = path[len(rule.path_prefix):].strip("/")
        return rule.resource_template.replace("{path}", path).replace("{path_suffix}", suffix)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        rule = self._match_rule(request.url.path, request.method)
        if not rule:
            return await call_next(request)

        # extrai token
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "PEP: Authorization header ausente."},
            )
        token = auth[7:]

        # decodifica token (usa o servico existente)
        try:
            from src.infrastructure.database.connection import SessionLocal
            from src.infrastructure.security.jwt_service import JwtTokenService
            from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
            db = SessionLocal()
            try:
                svc = JwtTokenService(SqliteTokenBlacklist(db))
                payload = svc.decode_token(token)
            finally:
                db.close()
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"PEP: Token invalido — {e}"},
            )

        # superuser bypass
        if rule.skip_superuser and payload.is_superuser:
            response = await call_next(request)
            response.headers["X-APL-Decision"] = "allow"
            response.headers["X-APL-Policy"] = "superuser-bypass"
            return response

        # monta subject a partir do payload
        subject = {
            "roles":           payload.roles,
            "permissions":     payload.permissions,
            "user_level":      payload.user_level_rank,
            "user_level_rank": payload.user_level_rank,
            "is_superuser":    payload.is_superuser,
            "group":           payload.group,
            "user_type":       payload.user_type,
            **payload.rbac,
            **payload.abac,
        }

        tenant_id = request.headers.get(rule.tenant_id_header)
        resource  = self._build_resource(rule, request.url.path)

        # avalia policy APL
        try:
            from src.infrastructure.database.connection import SessionLocal
            from src.application.services.policy_service import PolicyService
            db = SessionLocal()
            try:
                result = PolicyService(db).evaluate(
                    subject=subject,
                    action=rule.action,
                    resource=resource,
                    tenant_id=tenant_id,
                    subject_id=payload.user_id,
                    use_cache=True,
                    actor=payload.sub,
                )
            finally:
                db.close()
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": f"PEP: Erro na avaliacao APL — {e}"},
            )

        if not result.allowed:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": f"PEP: Acesso negado. {result.reason}",
                    "decision": result.decision,
                    "matched_policy": result.matched_policy,
                },
                headers={
                    "X-APL-Decision": result.decision,
                    "X-APL-Policy":   result.matched_policy or "no_match",
                },
            )

        response = await call_next(request)
        response.headers["X-APL-Decision"] = "allow"
        response.headers["X-APL-Policy"]   = result.matched_policy or ""
        return response
