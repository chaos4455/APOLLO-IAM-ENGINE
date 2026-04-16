import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.infrastructure.config.settings import get_settings
from src.interface.webapp.middleware.session_auth import SessionAuthMiddleware
from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware
from src.infrastructure.security.rate_limit_middleware import RateLimitMiddleware
from src.infrastructure.security.request_queue_middleware import RequestQueueMiddleware
from src.interface.webapp.routes import (
    login, dashboard, users, roles, permissions, groups,
    rbac_attributes, settings as settings_route, audit_logs,
)
from src.interface.webapp.routes import user_types, user_levels, custom_entities, metrics

settings = get_settings()

app = FastAPI(title=f"{settings.app_name} — Admin UI", docs_url=None, redoc_url=None)

# ── middleware stack (ordem inversa de execução no Starlette) ─────────────────
# SecurityHeaders → CORS → SessionAuth → Session (Session executa primeiro)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestQueueMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SessionAuthMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# caminho absoluto — funciona independente do cwd do processo filho
_HERE = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(_HERE, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

for r in [
    login.router, dashboard.router, users.router, roles.router,
    permissions.router, groups.router, rbac_attributes.router,
    settings_route.router, audit_logs.router,
    user_types.router, user_levels.router, custom_entities.router, metrics.router,
]:
    app.include_router(r)


@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/login")


@app.exception_handler(Exception)
async def global_error(request: Request, exc: Exception):
    return HTMLResponse(
        f"<pre style='font-family:monospace;padding:20px;color:red'>"
        f"500 — {type(exc).__name__}: {exc}</pre>",
        status_code=500,
    )
