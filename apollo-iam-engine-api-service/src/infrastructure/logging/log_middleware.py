"""
log_middleware.py
Middleware FastAPI que loga 100% das requisições/respostas HTTP.
"""
from __future__ import annotations
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.infrastructure.logging.event_logger import log_event

# rotas que não precisam de log (ruído sem valor)
_SKIP = {"/docs", "/redoc", "/openapi.json", "/favicon.ico"}


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in _SKIP:
            return await call_next(request)

        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

        status = "success" if response.status_code < 400 else "failure"
        log_event(
            event="http.request",
            actor=request.client.host if request.client else "unknown",
            resource=request.url.path,
            status=status,
            detail={
                "method":     request.method,
                "path":       request.url.path,
                "query":      str(request.url.query),
                "http_status": response.status_code,
                "elapsed_ms": elapsed_ms,
            },
        )
        return response
