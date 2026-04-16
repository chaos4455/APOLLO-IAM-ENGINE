"""
security_headers_middleware.py
Adiciona headers de segurança HTTP em todas as respostas.
O2 Data Solutions
"""
from __future__ import annotations
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.infrastructure.config.security_config import get_security_headers_config

_DEFAULT_CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdn.redoc.ly; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data: https: blob:; "
    "worker-src blob: 'self'; "
    "connect-src 'self' https:; "
    "frame-src 'none'"
)

# rotas que não devem ter CSP restritivo (docs interativos)
_NO_CSP_PATHS = {"/docs", "/redoc", "/openapi.json"}


def _clean(value: str) -> str:
    """Remove newlines e espaços extras — HTTP headers não aceitam quebras de linha."""
    return " ".join(value.split())


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        cfg = get_security_headers_config()
        if not cfg.get("enabled", True):
            return response

        hsts = cfg.get("hsts_max_age", 31536000)
        response.headers["Strict-Transport-Security"] = (
            f"max-age={hsts}; includeSubDomains; preload"
        )

        # docs precisam de CSP mais permissivo (ReDoc usa blob: workers + unsafe-eval)
        if request.url.path in _NO_CSP_PATHS:
            csp = (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval' blob: data: https:; "
                "worker-src blob:; img-src 'self' data: https: blob:"
            )
        else:
            csp = _clean(cfg.get("content_security_policy", _DEFAULT_CSP))

        response.headers["Content-Security-Policy"]  = csp
        response.headers["X-Frame-Options"]          = _clean(cfg.get("x_frame_options", "DENY"))
        response.headers["X-Content-Type-Options"]   = _clean(cfg.get("x_content_type_options", "nosniff"))
        response.headers["Referrer-Policy"]          = _clean(cfg.get("referrer_policy", "strict-origin-when-cross-origin"))
        response.headers["X-XSS-Protection"]         = "1; mode=block"
        response.headers["Permissions-Policy"]       = "geolocation=(), microphone=(), camera=()"
        response.headers["Cross-Origin-Opener-Policy"]   = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
        return response
