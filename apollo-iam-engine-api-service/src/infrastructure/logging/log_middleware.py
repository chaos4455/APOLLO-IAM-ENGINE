"""
log_middleware.py
Middleware FastAPI que loga 100% das requisições/respostas HTTP.
Inclui: duration_ms, session_id (X-Request-ID), tenant_id (X-Tenant-ID),
        user-agent, content-length, tags por categoria de rota.
"""
from __future__ import annotations
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.infrastructure.logging.event_logger import log_event

# rotas que não precisam de log (ruído sem valor)
_SKIP = {"/docs", "/redoc", "/openapi.json", "/favicon.ico", "/static"}

# tags por prefixo de rota
_ROUTE_TAGS: list[tuple[str, list[str]]] = [
    ("/auth/token",    ["auth", "login"]),
    ("/auth/refresh",  ["auth", "refresh"]),
    ("/auth/logout",   ["auth", "logout"]),
    ("/auth/validate", ["auth", "validate"]),
    ("/auth/check",    ["auth", "check", "rbac", "abac"]),
    ("/auth/",         ["auth"]),
    ("/admin/policies", ["policy", "dsl", "admin"]),
    ("/admin/users",   ["users", "admin"]),
    ("/admin/roles",   ["roles", "rbac", "admin"]),
    ("/admin/permissions", ["permissions", "rbac", "admin"]),
    ("/admin/groups",  ["groups", "admin"]),
    ("/admin/rbac",    ["rbac", "admin"]),
    ("/admin/audit",   ["audit", "admin"]),
    ("/admin/",        ["admin"]),
    ("/health",        ["health"]),
]


def _tags_for(path: str) -> list[str]:
    for prefix, tags in _ROUTE_TAGS:
        if path.startswith(prefix):
            return tags
    return ["http"]


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        for skip in _SKIP:
            if path.startswith(skip):
                return await call_next(request)

        # request-id: usa header se presente, senão gera
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        tenant_id = request.headers.get("X-Tenant-ID") or None

        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

        # injeta request-id na resposta
        response.headers["X-Request-ID"] = req_id

        status = "success" if response.status_code < 400 else "failure"
        if response.status_code == 429:
            status = "warning"

        log_event(
            event="http.request",
            actor=request.headers.get("X-Forwarded-For",
                  request.client.host if request.client else "unknown").split(",")[0].strip(),
            resource=path,
            status=status,
            tenant_id=tenant_id,
            session_id=req_id,
            duration_ms=elapsed_ms,
            tags=_tags_for(path),
            detail={
                "method":          request.method,
                "path":            path,
                "query":           str(request.url.query) or None,
                "http_status":     response.status_code,
                "user_agent":      request.headers.get("User-Agent", "")[:120],
                "content_length":  request.headers.get("Content-Length"),
                "request_id":      req_id,
            },
        )
        return response
