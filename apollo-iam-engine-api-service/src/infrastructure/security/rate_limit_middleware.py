"""
rate_limit_middleware.py
Rate limiting em memoria — sliding window por IP e por tenant.
Configuracao por rota via RATE_LIMIT_RULES.
v2: adiciona rate limit por tenant (X-Tenant-ID header).
Elias Andrade — O2 Data Solutions
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
    ("/auth/token",      10,  60),
    ("/auth/refresh",    20,  60),
    ("/auth/check",      60,  60),
    ("/auth/",           30,  60),
    ("/admin/metrics",   60,  60),
    ("/admin/",         120,  60),
    ("/",               200,  60),
]

# ── rate limit por tenant (requests / janela em segundos) ─────────────────────
# Aplicado em adicao ao rate limit por IP.
# Protege contra um tenant monopolizar o servico.
TENANT_RATE_LIMIT_RULES: list[tuple[str, int, int]] = [
    ("/admin/policies/evaluate", 500, 60),  # 500 evaluations/min por tenant
    ("/auth/check",              300, 60),  # 300 checks/min por tenant
    ("/auth/token",               50, 60),  # 50 logins/min por tenant
    ("/admin/",                  600, 60),  # 600 admin ops/min por tenant
]

WHITELIST_IPS: set[str] = {"127.0.0.1", "::1"}
SKIP_PATHS: set[str] = {"/health", "/docs", "/redoc", "/openapi.json", "/static"}

_ip_windows: dict[str, deque] = defaultdict(deque)
_tenant_windows: dict[str, deque] = defaultdict(deque)
_lock = asyncio.Lock()


def _get_rule(path: str) -> tuple[int, int]:
    for prefix, max_req, window in RATE_LIMIT_RULES:
        if path.startswith(prefix):
            return max_req, window
    return 200, 60


def _get_tenant_rule(path: str) -> tuple[int, int] | None:
    for prefix, max_req, window in TENANT_RATE_LIMIT_RULES:
        if path.startswith(prefix):
            return max_req, window
    return None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding window rate limiter em memoria.
    Aplica limite por IP e, se X-Tenant-ID presente, por tenant.
    Retorna 429 com header Retry-After quando o limite e excedido.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        for skip in SKIP_PATHS:
            if path.startswith(skip):
                return await call_next(request)

        ip = (request.headers.get("X-Forwarded-For") or
              (request.client.host if request.client else "unknown")).split(",")[0].strip()

        if ip in WHITELIST_IPS:
            return await call_next(request)

        max_req, window = _get_rule(path)
        ip_key = f"{ip}:{path}"
        now = time.monotonic()

        async with _lock:
            # ── rate limit por IP ─────────────────────────────────────────────
            dq = _ip_windows[ip_key]
            while dq and dq[0] < now - window:
                dq.popleft()

            if len(dq) >= max_req:
                retry_after = int(window - (now - dq[0])) + 1
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit excedido (IP). Tente novamente em breve.",
                        "retry_after_seconds": retry_after,
                        "limit_type": "ip",
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

            # ── rate limit por tenant ─────────────────────────────────────────
            tenant_id = request.headers.get("X-Tenant-ID")
            if tenant_id:
                tenant_rule = _get_tenant_rule(path)
                if tenant_rule:
                    t_max, t_window = tenant_rule
                    t_key = f"tenant:{tenant_id}:{path}"
                    tdq = _tenant_windows[t_key]
                    while tdq and tdq[0] < now - t_window:
                        tdq.popleft()

                    if len(tdq) >= t_max:
                        retry_after = int(t_window - (now - tdq[0])) + 1
                        return JSONResponse(
                            status_code=429,
                            content={
                                "detail": f"Rate limit excedido (tenant {tenant_id}).",
                                "retry_after_seconds": retry_after,
                                "limit_type": "tenant",
                            },
                            headers={
                                "Retry-After": str(retry_after),
                                "X-RateLimit-Tenant-Limit": str(t_max),
                                "X-RateLimit-Tenant-Remaining": "0",
                            },
                        )
                    tdq.append(now)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"]     = str(max_req)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"]    = str(window)
        return response
