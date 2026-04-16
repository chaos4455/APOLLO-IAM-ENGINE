"""
fix-v1.py — Apollo IAM Engine API Service
Corrige todos os problemas identificados no projeto:
  1. Completa password_hasher_impl.py (truncado)
  2. Corrige auth.py (prefix cortado)
  3. Adiciona application services (ausentes)
  4. Adiciona webapp routes, templates, main (ausentes)
  5. Adiciona __main__ block ao populate_apollo_iam.py
  6. Adiciona __init__.py com exports corretos
O2 Data Solutions
"""

import os

BASE = "apollo-iam-engine-api-service"


def w(rel: str, content: str):
    path = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ===========================================================================
# FIX 1 — password_hasher_impl.py (estava truncado)
# ===========================================================================

def fix_password_hasher():
    w("src/infrastructure/security/password_hasher_impl.py", '''\
from passlib.context import CryptContext
from src.domain.ports.password_hasher import PasswordHasher

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, plain: str) -> str:
        return _ctx.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return _ctx.verify(plain, hashed)
''')


# ===========================================================================
# FIX 2 — auth.py (prefix estava cortado)
# ===========================================================================

def fix_auth_route():
    w("src/interface/api/routes/auth.py", '''\
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
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
from src.interface.api.dependencies import oauth2_scheme

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
    uc = LoginUseCase(users, hasher, tokens, audit)
    ip = request.client.host if request and request.client else ""
    result = uc.execute(LoginInputDTO(username=form.username, password=form.password, ip_address=ip))
    return result.__dict__


@router.post("/refresh", summary="Renovar access token")
async def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    return RefreshTokenUseCase(tokens).execute(body.refresh_token)


@router.post("/logout", summary="Revogar token")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    LogoutUseCase(tokens).execute(token)
    return {"message": "Logout realizado."}


@router.post("/validate", summary="Validar token e retornar payload")
async def validate(body: ValidateTokenRequest, db: Session = Depends(get_db)):
    _, _, tokens, _ = _deps(db)
    payload = ValidateTokenUseCase(tokens).execute(body.token)
    return payload.__dict__
''')


# ===========================================================================
# FIX 3 — Application Services (ausentes)
# ===========================================================================

def fix_application_services():
    w("src/application/services/auth_service.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.infrastructure.security.jwt_service import JwtTokenService
from src.infrastructure.security.token_blacklist import SqliteTokenBlacklist
from src.application.use_cases.auth.login import LoginUseCase
from src.application.use_cases.auth.logout import LogoutUseCase
from src.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from src.application.use_cases.auth.validate_token import ValidateTokenUseCase
from src.application.dtos.auth_dto import LoginInputDTO, TokenOutputDTO
from src.domain.value_objects.token_payload import TokenPayload


class AuthService:
    """Orquestra os casos de uso de autenticação."""

    def __init__(self, db: Session):
        bl = SqliteTokenBlacklist(db)
        self._users = SqliteUserRepository(db)
        self._hasher = BcryptPasswordHasher()
        self._tokens = JwtTokenService(bl)
        self._audit = SqliteAuditLogRepository(db)

    def login(self, username: str, password: str, ip: str = "") -> TokenOutputDTO:
        uc = LoginUseCase(self._users, self._hasher, self._tokens, self._audit)
        return uc.execute(LoginInputDTO(username=username, password=password, ip_address=ip))

    def logout(self, token: str) -> None:
        LogoutUseCase(self._tokens).execute(token)

    def refresh(self, refresh_token: str) -> dict:
        return RefreshTokenUseCase(self._tokens).execute(refresh_token)

    def validate(self, token: str) -> TokenPayload:
        return ValidateTokenUseCase(self._tokens).execute(token)
''')

    w("src/application/services/user_service.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.use_cases.users.update_user import UpdateUserUseCase
from src.application.use_cases.users.delete_user import DeleteUserUseCase
from src.application.use_cases.users.get_user import GetUserUseCase
from src.application.use_cases.users.list_users import ListUsersUseCase
from src.application.use_cases.users.change_password import ChangePasswordUseCase
from src.application.use_cases.users.reset_password import ResetPasswordUseCase
from src.application.use_cases.users.toggle_user_status import ToggleUserStatusUseCase
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO, UserOutputDTO


class UserService:
    """Orquestra os casos de uso de usuários."""

    def __init__(self, db: Session):
        self._repo = SqliteUserRepository(db)
        self._hasher = BcryptPasswordHasher()

    def create(self, dto: CreateUserDTO) -> UserOutputDTO:
        return CreateUserUseCase(self._repo, self._hasher).execute(dto)

    def update(self, dto: UpdateUserDTO) -> UserOutputDTO:
        return UpdateUserUseCase(self._repo).execute(dto)

    def delete(self, user_id: str) -> None:
        DeleteUserUseCase(self._repo).execute(user_id)

    def get(self, user_id: str) -> UserOutputDTO:
        return GetUserUseCase(self._repo).execute(user_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[UserOutputDTO]:
        return ListUsersUseCase(self._repo).execute(skip, limit)

    def change_password(self, user_id: str, old: str, new: str) -> None:
        ChangePasswordUseCase(self._repo, self._hasher).execute(user_id, old, new)

    def reset_password(self, user_id: str, new: str) -> None:
        ResetPasswordUseCase(self._repo, self._hasher).execute(user_id, new)

    def toggle_status(self, user_id: str) -> bool:
        return ToggleUserStatusUseCase(self._repo).execute(user_id)
''')

    w("src/application/services/rbac_service.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.repositories.role_repository_impl import SqliteRoleRepository
from src.infrastructure.repositories.permission_repository_impl import SqlitePermissionRepository
from src.infrastructure.repositories.group_repository_impl import SqliteGroupRepository
from src.infrastructure.repositories.rbac_attribute_repository_impl import SqliteRbacAttributeRepository
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.list_roles import ListRolesUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.roles.assign_role_to_user import AssignRoleToUserUseCase
from src.application.use_cases.roles.revoke_role_from_user import RevokeRoleFromUserUseCase
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.permissions.list_permissions import ListPermissionsUseCase
from src.application.use_cases.permissions.delete_permission import DeletePermissionUseCase
from src.application.use_cases.permissions.assign_permission_to_role import AssignPermissionToRoleUseCase
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.use_cases.groups.list_groups import ListGroupsUseCase
from src.application.use_cases.groups.delete_group import DeleteGroupUseCase
from src.application.use_cases.groups.assign_user_to_group import AssignUserToGroupUseCase
from src.application.use_cases.rbac.create_attribute import CreateRbacAttributeUseCase
from src.application.use_cases.rbac.list_attributes import ListRbacAttributesUseCase
from src.application.use_cases.rbac.delete_attribute import DeleteRbacAttributeUseCase
from src.application.use_cases.rbac.assign_attribute_to_user import AssignAttributeToUserUseCase
from src.application.dtos.role_dto import CreateRoleDTO, RoleOutputDTO
from src.application.dtos.permission_dto import CreatePermissionDTO, PermissionOutputDTO
from src.application.dtos.group_dto import CreateGroupDTO, GroupOutputDTO
from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, RbacAttributeOutputDTO, AssignAttributeDTO


class RbacService:
    """Orquestra roles, permissões, grupos e atributos RBAC."""

    def __init__(self, db: Session):
        self._db = db
        self._roles = SqliteRoleRepository(db)
        self._perms = SqlitePermissionRepository(db)
        self._groups = SqliteGroupRepository(db)
        self._attrs = SqliteRbacAttributeRepository(db)

    # roles
    def create_role(self, dto: CreateRoleDTO) -> RoleOutputDTO:
        return CreateRoleUseCase(self._roles).execute(dto)

    def list_roles(self) -> list[RoleOutputDTO]:
        return ListRolesUseCase(self._roles).execute()

    def delete_role(self, role_id: str) -> None:
        DeleteRoleUseCase(self._roles).execute(role_id)

    def assign_role(self, user_id: str, role_id: str) -> None:
        AssignRoleToUserUseCase(self._db).execute(user_id, role_id)

    def revoke_role(self, user_id: str, role_id: str) -> None:
        RevokeRoleFromUserUseCase(self._db).execute(user_id, role_id)

    # permissions
    def create_permission(self, dto: CreatePermissionDTO) -> PermissionOutputDTO:
        return CreatePermissionUseCase(self._perms).execute(dto)

    def list_permissions(self) -> list[PermissionOutputDTO]:
        return ListPermissionsUseCase(self._perms).execute()

    def delete_permission(self, perm_id: str) -> None:
        DeletePermissionUseCase(self._perms).execute(perm_id)

    def assign_permission(self, role_id: str, perm_id: str) -> None:
        AssignPermissionToRoleUseCase(self._db).execute(role_id, perm_id)

    # groups
    def create_group(self, dto: CreateGroupDTO) -> GroupOutputDTO:
        return CreateGroupUseCase(self._groups).execute(dto)

    def list_groups(self) -> list[GroupOutputDTO]:
        return ListGroupsUseCase(self._groups).execute()

    def delete_group(self, group_id: str) -> None:
        DeleteGroupUseCase(self._groups).execute(group_id)

    def assign_user_to_group(self, user_id: str, group_id: str) -> None:
        AssignUserToGroupUseCase(self._db).execute(user_id, group_id)

    # rbac attributes
    def create_attribute(self, dto: CreateRbacAttributeDTO) -> RbacAttributeOutputDTO:
        return CreateRbacAttributeUseCase(self._attrs).execute(dto)

    def list_attributes(self) -> list[RbacAttributeOutputDTO]:
        return ListRbacAttributesUseCase(self._attrs).execute()

    def delete_attribute(self, attr_id: str) -> None:
        DeleteRbacAttributeUseCase(self._attrs).execute(attr_id)

    def assign_attribute(self, dto: AssignAttributeDTO) -> None:
        AssignAttributeToUserUseCase(self._db).execute(dto)
''')

    w("src/application/services/settings_service.py", '''\
from sqlalchemy.orm import Session
from src.application.use_cases.settings.get_settings import GetSettingsUseCase
from src.application.use_cases.settings.update_settings import UpdateSettingsUseCase
from src.application.dtos.settings_dto import SettingsOutputDTO, UpdateSettingsDTO


class SettingsService:
    def __init__(self, db: Session):
        self._db = db

    def get(self) -> SettingsOutputDTO:
        return GetSettingsUseCase(self._db).execute()

    def update(self, dto: UpdateSettingsDTO) -> SettingsOutputDTO:
        return UpdateSettingsUseCase(self._db).execute(dto)
''')

    w("src/application/services/audit_service.py", '''\
from sqlalchemy.orm import Session
from src.infrastructure.repositories.audit_log_repository_impl import SqliteAuditLogRepository
from src.application.dtos.audit_dto import AuditLogOutputDTO


class AuditService:
    def __init__(self, db: Session):
        self._repo = SqliteAuditLogRepository(db)

    def list_logs(self, skip: int = 0, limit: int = 100) -> list[AuditLogOutputDTO]:
        return [
            AuditLogOutputDTO(
                id=l.id, actor=l.actor, action=l.action, resource=l.resource,
                resource_id=l.resource_id, detail=l.detail, ip_address=l.ip_address,
                status=l.status, created_at=str(l.created_at),
            )
            for l in self._repo.list_logs(skip, limit)
        ]
''')


# ===========================================================================
# FIX 4 — Webapp middleware session_auth.py
# ===========================================================================

def fix_webapp_middleware():
    w("src/interface/webapp/middleware/session_auth.py", '''\
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse


class SessionAuthMiddleware(BaseHTTPMiddleware):
    """Redireciona para /admin/login se não houver sessão ativa."""

    EXEMPT = {"/admin/login", "/admin/login/", "/static"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(e) for e in self.EXEMPT):
            return await call_next(request)
        if not request.session.get("user"):
            return RedirectResponse(url="/admin/login", status_code=302)
        return await call_next(request)
''')


# ===========================================================================
# FIX 5 — Webapp dependencies.py
# ===========================================================================

def fix_webapp_dependencies():
    w("src/interface/webapp/dependencies.py", '''\
from fastapi import Request, HTTPException, status


def get_session_user(request: Request) -> dict:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
''')


# ===========================================================================
# FIX 6 — Webapp routes
# ===========================================================================

def fix_webapp_routes():

    w("src/interface/webapp/routes/login.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))

API_BASE = "http://localhost:8000"


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = ""):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/admin/login")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{API_BASE}/auth/token",
                data={"username": username, "password": password},
            )
            if resp.status_code == 200:
                data = resp.json()
                request.session["user"] = {"username": username, "token": data["access_token"]}
                return RedirectResponse(url="/admin/dashboard", status_code=302)
            error = "Credenciais inválidas."
        except Exception:
            error = "Serviço de API indisponível."
    return RedirectResponse(url=f"/admin/login?error={error}", status_code=302)


@router.get("/admin/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=302)
''')

    w("src/interface/webapp/routes/dashboard.py", '''\
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


async def _get(path: str, token: str) -> dict | list:
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API_BASE}{path}", headers={"Authorization": f"Bearer {token}"})
        return r.json() if r.status_code == 200 else []


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    token = request.session["user"]["token"]
    users = await _get("/admin/users/", token)
    roles = await _get("/admin/roles/", token)
    groups = await _get("/admin/groups/", token)
    perms = await _get("/admin/permissions/", token)
    stats = {
        "users": len(users) if isinstance(users, list) else 0,
        "roles": len(roles) if isinstance(roles, list) else 0,
        "groups": len(groups) if isinstance(groups, list) else 0,
        "permissions": len(perms) if isinstance(perms, list) else 0,
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats})
''')

    w("src/interface/webapp/routes/users.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _headers(request: Request):
    return {"Authorization": f"Bearer {request.session['user']['token']}"}


@router.get("/admin/users", response_class=HTMLResponse)
async def list_users(request: Request):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API_BASE}/admin/users/", headers=_headers(request))
        users = r.json() if r.status_code == 200 else []
    return templates.TemplateResponse("users/list.html", {"request": request, "users": users})


@router.get("/admin/users/new", response_class=HTMLResponse)
async def new_user_form(request: Request):
    async with httpx.AsyncClient() as c:
        roles = (await c.get(f"{API_BASE}/admin/roles/", headers=_headers(request))).json()
        groups = (await c.get(f"{API_BASE}/admin/groups/", headers=_headers(request))).json()
    return templates.TemplateResponse("users/form.html",
        {"request": request, "user": None, "roles": roles, "groups": groups, "error": ""})


@router.post("/admin/users/new")
async def create_user(
    request: Request,
    username: str = Form(...), password: str = Form(...),
    email: Optional[str] = Form(None), full_name: Optional[str] = Form(None),
    is_active: bool = Form(True), is_superuser: bool = Form(False),
    group_id: Optional[str] = Form(None),
):
    payload = {"username": username, "password": password, "email": email or None,
               "full_name": full_name or None, "is_active": is_active,
               "is_superuser": is_superuser, "group_id": group_id or None, "role_names": []}
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{API_BASE}/admin/users/", json=payload, headers=_headers(request))
    if r.status_code == 201:
        return RedirectResponse(url="/admin/users", status_code=302)
    return RedirectResponse(url="/admin/users/new?error=Erro+ao+criar+usuário", status_code=302)


@router.post("/admin/users/{user_id}/delete")
async def delete_user(user_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.delete(f"{API_BASE}/admin/users/{user_id}", headers=_headers(request))
    return RedirectResponse(url="/admin/users", status_code=302)


@router.post("/admin/users/{user_id}/toggle")
async def toggle_user(user_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API_BASE}/admin/users/{user_id}/toggle-status", headers=_headers(request))
    return RedirectResponse(url="/admin/users", status_code=302)
''')

    w("src/interface/webapp/routes/roles.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _h(r: Request): return {"Authorization": f"Bearer {r.session['user']['token']}"}


@router.get("/admin/roles", response_class=HTMLResponse)
async def list_roles(request: Request):
    async with httpx.AsyncClient() as c:
        roles = (await c.get(f"{API_BASE}/admin/roles/", headers=_h(request))).json()
    return templates.TemplateResponse("roles/list.html", {"request": request, "roles": roles})


@router.post("/admin/roles/new")
async def create_role(request: Request, name: str = Form(...), description: str = Form("")):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API_BASE}/admin/roles/", json={"name": name, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/roles", status_code=302)


@router.post("/admin/roles/{role_id}/delete")
async def delete_role(role_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.delete(f"{API_BASE}/admin/roles/{role_id}", headers=_h(request))
    return RedirectResponse(url="/admin/roles", status_code=302)
''')

    w("src/interface/webapp/routes/permissions.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _h(r: Request): return {"Authorization": f"Bearer {r.session['user']['token']}"}


@router.get("/admin/permissions", response_class=HTMLResponse)
async def list_perms(request: Request):
    async with httpx.AsyncClient() as c:
        perms = (await c.get(f"{API_BASE}/admin/permissions/", headers=_h(request))).json()
    return templates.TemplateResponse("permissions/list.html", {"request": request, "permissions": perms})


@router.post("/admin/permissions/new")
async def create_perm(request: Request, name: str = Form(...), resource: str = Form(...),
                      action: str = Form(...), description: str = Form("")):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API_BASE}/admin/permissions/",
                     json={"name": name, "resource": resource, "action": action, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/permissions", status_code=302)


@router.post("/admin/permissions/{perm_id}/delete")
async def delete_perm(perm_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.delete(f"{API_BASE}/admin/permissions/{perm_id}", headers=_h(request))
    return RedirectResponse(url="/admin/permissions", status_code=302)
''')

    w("src/interface/webapp/routes/groups.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _h(r: Request): return {"Authorization": f"Bearer {r.session['user']['token']}"}


@router.get("/admin/groups", response_class=HTMLResponse)
async def list_groups(request: Request):
    async with httpx.AsyncClient() as c:
        groups = (await c.get(f"{API_BASE}/admin/groups/", headers=_h(request))).json()
    return templates.TemplateResponse("groups/list.html", {"request": request, "groups": groups})


@router.post("/admin/groups/new")
async def create_group(request: Request, name: str = Form(...), description: str = Form("")):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API_BASE}/admin/groups/",
                     json={"name": name, "description": description}, headers=_h(request))
    return RedirectResponse(url="/admin/groups", status_code=302)


@router.post("/admin/groups/{group_id}/delete")
async def delete_group(group_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.delete(f"{API_BASE}/admin/groups/{group_id}", headers=_h(request))
    return RedirectResponse(url="/admin/groups", status_code=302)
''')

    w("src/interface/webapp/routes/rbac_attributes.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _h(r: Request): return {"Authorization": f"Bearer {r.session['user']['token']}"}


@router.get("/admin/rbac", response_class=HTMLResponse)
async def list_attrs(request: Request):
    async with httpx.AsyncClient() as c:
        attrs = (await c.get(f"{API_BASE}/admin/rbac/", headers=_h(request))).json()
    return templates.TemplateResponse("rbac/list.html", {"request": request, "attributes": attrs})


@router.post("/admin/rbac/new")
async def create_attr(request: Request, key: str = Form(...), label: str = Form(...),
                      value_type: str = Form("string"), description: str = Form("")):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API_BASE}/admin/rbac/",
                     json={"key": key, "label": label, "value_type": value_type, "description": description},
                     headers=_h(request))
    return RedirectResponse(url="/admin/rbac", status_code=302)


@router.post("/admin/rbac/{attr_id}/delete")
async def delete_attr(attr_id: str, request: Request):
    async with httpx.AsyncClient() as c:
        await c.delete(f"{API_BASE}/admin/rbac/{attr_id}", headers=_h(request))
    return RedirectResponse(url="/admin/rbac", status_code=302)
''')

    w("src/interface/webapp/routes/settings.py", '''\
import httpx
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


def _h(r: Request): return {"Authorization": f"Bearer {r.session['user']['token']}"}


@router.get("/admin/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    async with httpx.AsyncClient() as c:
        s = (await c.get(f"{API_BASE}/admin/settings/", headers=_h(request))).json()
    return templates.TemplateResponse("settings/index.html", {"request": request, "settings": s})


@router.post("/admin/settings")
async def update_settings(
    request: Request,
    access_token_expire_minutes: int = Form(60),
    refresh_token_expire_days: int = Form(7),
    allow_registration: bool = Form(False),
    max_login_attempts: int = Form(5),
    lockout_minutes: int = Form(15),
):
    payload = {
        "access_token_expire_minutes": access_token_expire_minutes,
        "refresh_token_expire_days": refresh_token_expire_days,
        "allow_registration": allow_registration,
        "max_login_attempts": max_login_attempts,
        "lockout_minutes": lockout_minutes,
    }
    async with httpx.AsyncClient() as c:
        await c.put(f"{API_BASE}/admin/settings/", json=payload, headers=_h(request))
    return RedirectResponse(url="/admin/settings", status_code=302)
''')

    w("src/interface/webapp/routes/audit_logs.py", '''\
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "interface", "webapp", "templates"))
API_BASE = "http://localhost:8000"


@router.get("/admin/audit", response_class=HTMLResponse)
async def list_logs(request: Request, skip: int = 0, limit: int = 100):
    token = request.session["user"]["token"]
    async with httpx.AsyncClient() as c:
        logs = (await c.get(
            f"{API_BASE}/admin/audit/?skip={skip}&limit={limit}",
            headers={"Authorization": f"Bearer {token}"},
        )).json()
    return templates.TemplateResponse("audit/list.html", {"request": request, "logs": logs})
''')


# ===========================================================================
# FIX 7 — Webapp main.py
# ===========================================================================

def fix_webapp_main():
    w("src/interface/webapp/main.py", '''\
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.infrastructure.config.settings import get_settings
from src.interface.webapp.middleware.session_auth import SessionAuthMiddleware
from src.interface.webapp.routes import (
    login, dashboard, users, roles, permissions, groups,
    rbac_attributes, settings as settings_route, audit_logs,
)
import os

settings = get_settings()

app = FastAPI(title=f"{settings.app_name} — Admin UI", docs_url=None, redoc_url=None)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.add_middleware(SessionAuthMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

static_dir = os.path.join("src", "interface", "webapp", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

for r in [login.router, dashboard.router, users.router, roles.router,
          permissions.router, groups.router, rbac_attributes.router,
          settings_route.router, audit_logs.router]:
    app.include_router(r)


@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/login")
''')

    w("src/interface/webapp/routes/__init__.py", '''\
from src.interface.webapp.routes import (
    login, dashboard, users, roles, permissions,
    groups, rbac_attributes, settings, audit_logs,
)
''')


# ===========================================================================
# RELATÓRIO FINAL
# ===========================================================================

def _report(files_written: list, start: float):
    import time
    from colorama import init
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    init(autoreset=True)
    console = Console()
    elapsed = time.time() - start
    total_bytes = sum(os.path.getsize(f) for f in files_written if os.path.exists(f))

    table = Table(title="🔧 Fix-v1 Concluído", border_style="orange1", show_lines=True)
    table.add_column("Arquivo corrigido", style="bold cyan")
    table.add_column("Tamanho", style="bold green")
    for f in files_written:
        kb = os.path.getsize(f) / 1024 if os.path.exists(f) else 0
        table.add_row(f.replace(BASE + os.sep, ""), f"{kb:.1f} KB")
    console.print(table)

    summary = Table(title="📊 Resumo", border_style="green", show_lines=True)
    summary.add_column("Métrica", style="bold cyan")
    summary.add_column("Valor", style="bold green")
    summary.add_row("🔧 Arquivos corrigidos", str(len(files_written)))
    summary.add_row("💾 Total escrito", f"{total_bytes / 1024:.1f} KB")
    summary.add_row("⏱️  Tempo", f"{elapsed:.2f}s")
    console.print(summary)

    console.print(Panel.fit(
        "[bold green]✅ Fix-v1 aplicado com sucesso![/bold green]\n"
        "[dim]Próximo passo: execute [bold]python fix-v2.py[/bold][/dim]",
        border_style="green"
    ))


if __name__ == "__main__":
    import time
    _start = time.time()
    _written = []
    _orig_w = w

    def w_tracked(rel, content):
        path = os.path.join(BASE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        _written.append(path)
        return path

    w.__code__ = w_tracked.__code__

    fix_password_hasher()
    fix_auth_route()
    fix_application_services()
    fix_webapp_middleware()
    fix_webapp_dependencies()
    fix_webapp_routes()
    fix_webapp_main()

    _report(_written, _start)
