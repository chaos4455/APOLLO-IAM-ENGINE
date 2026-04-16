from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.infrastructure.config.settings import get_settings
from src.infrastructure.database.connection import init_db, SessionLocal
from src.infrastructure.seed.seed_roles import seed_roles
from src.infrastructure.seed.seed_permissions import seed_permissions
from src.infrastructure.seed.seed_admin import seed_admin
from src.interface.api.routes.auth import router as auth_router
from src.interface.api.routes.admin.users import router as users_router
from src.interface.api.routes.admin.roles import router as roles_router
from src.interface.api.routes.admin.permissions import router as perms_router
from src.interface.api.routes.admin.groups import router as groups_router
from src.interface.api.routes.admin.rbac_attributes import router as rbac_router
from src.interface.api.routes.admin.settings import router as settings_router
from src.interface.api.routes.admin.audit_logs import router as audit_router
from src.interface.api.routes.admin.user_types import router as user_types_router
from src.interface.api.routes.admin.user_levels import router as user_levels_router
from src.interface.api.routes.admin.custom_entities import router as custom_entities_router
from src.interface.api.routes.admin.metrics import router as metrics_router
from src.infrastructure.logging.console_logger import success, info
from src.infrastructure.logging.log_middleware import RequestLogMiddleware
from src.infrastructure.logging.event_logger import log_event
from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware
from src.infrastructure.security.rate_limit_middleware import RateLimitMiddleware
from src.infrastructure.security.request_queue_middleware import RequestQueueMiddleware
from src.domain.exceptions.auth_exceptions import (
    InvalidCredentialsError, TokenExpiredError, TokenInvalidError, InactiveUserError
)
from src.domain.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError
from src.domain.exceptions.rbac_exceptions import (
    RoleNotFoundError, PermissionNotFoundError, GroupNotFoundError,
    AttributeNotFoundError, InsufficientPermissionsError
)
from sqlalchemy.exc import IntegrityError

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_permissions(db)
        seed_admin(db)
    finally:
        db.close()
    success(f"Apollo IAM Engine v{settings.app_version} iniciado!")
    info("Docs: http://localhost:8000/docs")
    log_event("system.startup", actor="system", resource="api",
              detail={"version": settings.app_version})
    yield
    log_event("system.shutdown", actor="system", resource="api")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Servico centralizado de IAM + RBAC — O2 Data Solutions",
    docs_url="/docs",
    redoc_url=None,          # desabilita o redoc padrão — usamos rota customizada
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLogMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestQueueMiddleware)

# ── exception handlers globais ────────────────────────────────────────────────

@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

@app.exception_handler(InactiveUserError)
async def inactive_user_handler(request: Request, exc: InactiveUserError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

@app.exception_handler(TokenExpiredError)
async def token_expired_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(status_code=401, content={"detail": "Token expirado."})

@app.exception_handler(TokenInvalidError)
async def token_invalid_handler(request: Request, exc: TokenInvalidError):
    return JSONResponse(status_code=401, content={"detail": "Token invalido."})

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Usuario nao encontrado."})

@app.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(RoleNotFoundError)
async def role_not_found_handler(request: Request, exc: RoleNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Role nao encontrada."})

@app.exception_handler(PermissionNotFoundError)
async def perm_not_found_handler(request: Request, exc: PermissionNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Permissao nao encontrada."})

@app.exception_handler(GroupNotFoundError)
async def group_not_found_handler(request: Request, exc: GroupNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Grupo nao encontrado."})

@app.exception_handler(AttributeNotFoundError)
async def attr_not_found_handler(request: Request, exc: AttributeNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Atributo nao encontrado."})

@app.exception_handler(InsufficientPermissionsError)
async def insuf_perm_handler(request: Request, exc: InsufficientPermissionsError):
    return JSONResponse(status_code=403, content={"detail": "Permissoes insuficientes."})

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
    if "UNIQUE" in msg.upper():
        return JSONResponse(status_code=409, content={"detail": f"Registro ja existe: {msg}"})
    return JSONResponse(status_code=400, content={"detail": f"Erro de integridade: {msg}"})

# ── routers ───────────────────────────────────────────────────────────────────

for router in [auth_router, users_router, roles_router, perms_router,
               groups_router, rbac_router, settings_router, audit_router,
               user_types_router, user_levels_router, custom_entities_router,
               metrics_router]:
    app.include_router(router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""<!DOCTYPE html>
<html>
<head>
  <title>ReDoc — Apollo IAM Engine</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔐</text></svg>"/>
  <style>body{margin:0;padding:0}</style>
</head>
<body>
  <div id="redoc-container"></div>
  <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"
          crossorigin="anonymous"></script>
  <script>
    Redoc.init('/openapi.json', {
      theme: {
        colors: { primary: { main: '#f97316' } },
        typography: { fontFamily: 'Inter, sans-serif' }
      }
    }, document.getElementById('redoc-container'));
  </script>
</body>
</html>""", media_type="text/html")
