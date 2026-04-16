"""
request_queue_middleware.py
Pool de requisições em memória com fila de espera.
Limita concorrência máxima e enfileira o excedente.
O2 Data Solutions
"""
from __future__ import annotations
import asyncio
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# ── configuração ──────────────────────────────────────────────────────────────
MAX_CONCURRENT   = 50    # requisições simultâneas máximas
MAX_QUEUE_SIZE   = 200   # fila de espera máxima
QUEUE_TIMEOUT_S  = 30.0  # tempo máximo de espera na fila (segundos)

# rotas que nunca entram na fila (health, static)
SKIP_QUEUE_PATHS = {"/health", "/static", "/docs", "/redoc", "/openapi.json"}

_semaphore: asyncio.Semaphore | None = None
_queue_size = 0
_active     = 0
_total_req  = 0
_rejected   = 0


def get_pool_stats() -> dict:
    return {
        "max_concurrent": MAX_CONCURRENT,
        "max_queue":      MAX_QUEUE_SIZE,
        "active":         _active,
        "queued":         _queue_size,
        "total_requests": _total_req,
        "rejected":       _rejected,
    }


class RequestQueueMiddleware(BaseHTTPMiddleware):
    """
    Controla concorrência via asyncio.Semaphore.
    Requisições além do limite entram em fila com timeout.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        global _semaphore, _queue_size, _active, _total_req, _rejected

        # inicializa semáforo na primeira requisição (loop já existe)
        if _semaphore is None:
            _semaphore = asyncio.Semaphore(MAX_CONCURRENT)

        path = request.url.path
        for skip in SKIP_QUEUE_PATHS:
            if path.startswith(skip):
                return await call_next(request)

        _total_req += 1

        # verifica se a fila está cheia
        if _semaphore._value == 0 and _queue_size >= MAX_QUEUE_SIZE:
            _rejected += 1
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "Servidor sobrecarregado. Tente novamente em instantes.",
                    "queued": _queue_size,
                    "active": _active,
                },
                headers={"Retry-After": "5"},
            )

        _queue_size += 1
        t0 = time.monotonic()
        try:
            acquired = await asyncio.wait_for(
                _semaphore.acquire(), timeout=QUEUE_TIMEOUT_S
            )
        except asyncio.TimeoutError:
            _queue_size -= 1
            _rejected += 1
            return JSONResponse(
                status_code=503,
                content={"detail": "Timeout na fila de requisições. Tente novamente."},
                headers={"Retry-After": "10"},
            )
        finally:
            _queue_size = max(0, _queue_size - 1)

        _active += 1
        wait_ms = round((time.monotonic() - t0) * 1000, 1)
        try:
            response = await call_next(request)
            response.headers["X-Queue-Wait-Ms"] = str(wait_ms)
            response.headers["X-Pool-Active"]   = str(_active)
            return response
        finally:
            _active = max(0, _active - 1)
            _semaphore.release()
