"""
rate_limit_middleware.py
Rate limiting em memória — sliding window por IP.
Configuração por rota via RATE_LIMIT_RULES.
O2 Data Solutions
"""
from __future__ import annotations
import time
import asyncio
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# ── regras por prefixo de rota (requests / janela em segundos) ────────────────
RATE_LIMIT_RULES: list[tuple[str, int, int]] = [
    # (prefixo,          max_requests, window_seconds)
    ("/auth/token",      10,  60),   # login: 10 tentativas/min por IP
    ("/auth/refresh",    20,  60),
    ("/auth/check",      60,  60),
    ("/auth/",           30,  60),
    ("/admin/metrics",   60,  60),
    ("/admin/",         120,  60),
    ("/",               200,  60),   # fallback global
]

# ── whitelist de IPs que nunca são limitados ──────────────────────────────────
WHITELIST_IPS: set[str] = {"127.0.0.1", "::1"}

# ── rotas que nunca são limitadas ─────────────────────────────────────────────
SKIP_PATHS: set[str] = {"/health", "/docs", "/redoc", "/openapi.json", "/static"}

_windows: dict[str, deque] = defaultdict(deque)
_lock = asyncio.Lock()


def _get_rule(path: str) -> tuple[int, int]:
    for prefix, max_req, window in RATE_LIMIT_RULES:
        if path.startswith(prefix):
            return max_req, window
    return 200, 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding window rate limiter em memória.
    Retorna 429 com header Retry-After quando o limite é excedido.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        # skip static e rotas isentas
        for skip in SKIP_PATHS:
            if path.startswith(skip):
                return await call_next(request)

        ip = (request.headers.get("X-Forwarded-For") or
              (request.client.host if request.client else "unknown")).split(",")[0].strip()

        if ip in WHITELIST_IPS:
            return await call_next(request)

        max_req, window = _get_rule(path)
        key = f"{ip}:{path}"
        now = time.monotonic()

        async with _lock:
            dq = _windows[key]
            # remove timestamps fora da janela
            while dq and dq[0] < now - window:
                dq.popleft()

            if len(dq) >= max_req:
                retry_after = int(window - (now - dq[0])) + 1
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit excedido. Tente novamente em breve.",
                        "retry_after_seconds": retry_after,
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(max_req),
                        "X-RateLimit-Window": str(window),
                        "X-RateLimit-Remaining": "0",
                    },
                )

            dq.append(now)
            remaining = max_req - len(dq)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"]     = str(max_req)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"]    = str(window)
        return response
