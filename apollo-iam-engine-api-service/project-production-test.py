# project-production-test
"""
project-production-test.py
Testa o projeto Apollo IAM Engine em producao:
  - Health check
  - Todas as rotas da API
  - Cria RBAC padrao (sistema de cotacao)
  - Cria usuario1 / vendedor com role cotacao:create
  - Testa login e valida roles no token
  - BLOCO 8 — Testes ABAC completos (/auth/check)
  - Salva relatorio em YAML, MD e JSON em project-test-run-setup-logs/
O2 Data Solutions
"""

import os
import sys
import ssl
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
import yaml
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import track, Progress, SpinnerColumn, TextColumn

init(autoreset=True)
console = Console()

# ── resolve raiz do projeto e importa config de segurança ────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from src.infrastructure.config.security_config import (
    is_mtls_enabled, get_certs_dir, get_api_port,
)

# ── config ────────────────────────────────────────────────────────────────────
_MTLS    = is_mtls_enabled()
_PORT    = get_api_port() if _MTLS else 8000
_PROTO   = "https" if _MTLS else "http"
API_BASE = f"{_PROTO}://localhost:{_PORT}"

LOGS_DIR   = os.path.join(_HERE, "project-test-run-setup-logs")
RUN_ID     = datetime.now().strftime("%Y%m%d_%H%M%S")
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

os.makedirs(LOGS_DIR, exist_ok=True)

# ── SSLContext para mTLS ──────────────────────────────────────────────────────
def _build_ssl_ctx() -> ssl.SSLContext | bool:
    """Retorna SSLContext com cert cliente se mTLS ativo, senão True (verify padrão)."""
    if not _MTLS:
        return True
    certs = get_certs_dir()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(cafile=str(certs / "ca" / "ca.crt"))
    ctx.load_cert_chain(
        certfile=str(certs / "client" / "client.crt"),
        keyfile=str(certs / "client" / "client.key"),
    )
    ctx.check_hostname = False
    return ctx

_SSL = _build_ssl_ctx()

# ── estado global do run ──────────────────────────────────────────────────────
results: list[dict] = []
kpis: dict = {
    "total": 0, "passed": 0, "failed": 0,
    "created_roles": [], "created_permissions": [],
    "created_users": [], "created_groups": [],
    "token_admin": None, "token_usuario1": None,
    "token_gerente": None,
}


# ── helpers ───────────────────────────────────────────────────────────────────

_TIMEOUT = httpx.Timeout(30.0, connect=10.0)


class _FakeResponse:
    """Resposta fake para erros de conexao — evita crash com traceback."""
    def __init__(self, exc):
        self.status_code = 0
        self._exc = exc
    def json(self): return {"detail": str(self._exc)}
    @property
    def text(self): return str(self._exc)


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def step(name: str, ok: bool, status_code: int = 0,
         detail: str = "", data: dict | None = None):
    icon  = "✅" if ok else "❌"
    color = "bold green" if ok else "bold red"
    kpis["total"] += 1
    if ok:
        kpis["passed"] += 1
    else:
        kpis["failed"] += 1

    entry = {
        "step": name, "ok": ok, "status_code": status_code,
        "detail": detail, "data": data or {}, "timestamp": _ts(),
    }
    results.append(entry)

    console.print(
        f"  {icon} [{color}]{name}[/{color}]"
        + (f"  [dim]{detail}[/dim]" if detail else "")
        + (f"  [dim cyan]HTTP {status_code}[/dim cyan]" if status_code else "")
    )
    return ok


def get(path: str, token: str = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return httpx.get(f"{API_BASE}{path}", headers=headers,
                         timeout=_TIMEOUT, verify=_SSL)
    except Exception as e:
        return _FakeResponse(e)


def post(path: str, json_body: dict = None, form: dict = None, token: str = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        if form:
            return httpx.post(f"{API_BASE}{path}", data=form, headers=headers,
                              timeout=_TIMEOUT, verify=_SSL)
        return httpx.post(f"{API_BASE}{path}", json=json_body, headers=headers,
                          timeout=_TIMEOUT, verify=_SSL)
    except Exception as e:
        return _FakeResponse(e)


def put(path: str, json_body: dict, token: str = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return httpx.put(f"{API_BASE}{path}", json=json_body, headers=headers,
                         timeout=_TIMEOUT, verify=_SSL)
    except Exception as e:
        return _FakeResponse(e)


def delete(path: str, token: str = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return httpx.delete(f"{API_BASE}{path}", headers=headers,
                            timeout=_TIMEOUT, verify=_SSL)
    except Exception as e:
        return _FakeResponse(e)


def delete(path: str, token: str = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return httpx.delete(f"{API_BASE}{path}", headers=headers, timeout=_TIMEOUT)
    except Exception as e:
        return _FakeResponse(e)


# ===========================================================================
# BLOCO 1 — Health & Conectividade
# ===========================================================================

def test_health():
    console.print(Rule("[bold cyan]1. Health & Conectividade[/bold cyan]", style="cyan"))

    console.print("  [dim]Aguardando API responder...[/dim]")
    for attempt in range(15):
        try:
            r = httpx.get(f"{API_BASE}/health", timeout=3, verify=_SSL)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(2)
    else:
        step("API disponivel", False, 0, "API nao respondeu em 30s")
        console.print("[bold red]  Certifique-se de rodar run-init-api-engine.py primeiro.[/bold red]")
        sys.exit(1)

    try:
        r = get("/health")
        ok = r.status_code == 200 and r.json().get("status") == "ok"
        step("GET /health", ok, r.status_code, r.json().get("service", ""))
    except Exception as e:
        step("GET /health", False, 0, str(e))
        sys.exit(1)

    try:
        r = get("/docs")
        step("GET /docs (Swagger)", r.status_code == 200, r.status_code)
    except Exception as e:
        step("GET /docs (Swagger)", False, 0, str(e))

    try:
        r = get("/redoc")
        step("GET /redoc", r.status_code == 200, r.status_code)
    except Exception as e:
        step("GET /redoc", False, 0, str(e))


# ===========================================================================
# BLOCO 2 — Autenticacao Admin
# ===========================================================================

def test_auth_admin():
    console.print(Rule("[bold cyan]2. Autenticacao Admin[/bold cyan]", style="cyan"))

    r = post("/auth/token", form={"username": ADMIN_USER, "password": ADMIN_PASS})
    ok = r.status_code == 200
    step("POST /auth/token (admin)", ok, r.status_code)
    if not ok:
        console.print(f"[red]  Falha no login admin: {r.text}[/red]")
        sys.exit(1)

    data = r.json()
    kpis["token_admin"] = data["access_token"]

    r2 = post("/auth/validate", json_body={"token": kpis["token_admin"]})
    ok2 = r2.status_code == 200
    payload = r2.json() if ok2 else {}
    step("POST /auth/validate (admin)", ok2, r2.status_code,
         f"sub={payload.get('sub')} superuser={payload.get('is_superuser')}")

    r3 = post("/auth/token", form={"username": "admin", "password": "errada"})
    step("POST /auth/token (senha errada → 401)", r3.status_code == 401, r3.status_code)

    r4 = post("/auth/token", form={"username": "naoexiste", "password": "x"})
    step("POST /auth/token (user inexistente → 401)", r4.status_code == 401, r4.status_code)


# ===========================================================================
# BLOCO 3 — Rotas Admin: Users, Roles, Permissions, Groups, RBAC, Settings
# ===========================================================================

def test_admin_routes():
    tok = kpis["token_admin"]
    console.print(Rule("[bold cyan]3. Rotas Admin — listagem[/bold cyan]", style="cyan"))

    for path, label in [
        ("/admin/users/",       "GET /admin/users/"),
        ("/admin/roles/",       "GET /admin/roles/"),
        ("/admin/permissions/", "GET /admin/permissions/"),
        ("/admin/groups/",      "GET /admin/groups/"),
        ("/admin/rbac/",        "GET /admin/rbac/"),
        ("/admin/settings/",    "GET /admin/settings/"),
        ("/admin/audit/",       "GET /admin/audit/"),
    ]:
        r = get(path, token=tok)
        step(label, r.status_code == 200, r.status_code,
             f"{len(r.json()) if isinstance(r.json(), list) else 'ok'} itens")

    r = get("/admin/users/")
    step("GET /admin/users/ sem token → 401", r.status_code == 401, r.status_code)


# ===========================================================================
# BLOCO 4 — Setup RBAC: Sistema de Cotacao
# ===========================================================================

def setup_rbac_cotacao():
    tok = kpis["token_admin"]
    console.print(Rule("[bold cyan]4. Setup RBAC — Sistema de Cotacao[/bold cyan]", style="cyan"))

    perms_to_create = [
        {"name": "cotacao:create", "resource": "cotacao", "action": "create",
         "description": "Criar nova cotacao"},
        {"name": "cotacao:read",   "resource": "cotacao", "action": "read",
         "description": "Visualizar cotacoes"},
        {"name": "cotacao:update", "resource": "cotacao", "action": "update",
         "description": "Editar cotacao"},
        {"name": "cotacao:delete", "resource": "cotacao", "action": "delete",
         "description": "Excluir cotacao"},
        {"name": "cotacao:approve","resource": "cotacao", "action": "approve",
         "description": "Aprovar cotacao"},
    ]

    perm_ids: dict[str, str] = {}
    for p in perms_to_create:
        r = post("/admin/permissions/", json_body=p, token=tok)
        ok = r.status_code in (200, 201, 409)
        pid = r.json().get("id") if r.status_code in (200, 201) else None
        if r.status_code == 409:
            all_p = get("/admin/permissions/", token=tok).json()
            existing = next((x for x in all_p if x["name"] == p["name"]), None)
            pid = existing["id"] if existing else None
        if pid:
            perm_ids[p["name"]] = pid
            kpis["created_permissions"].append(p["name"])
        step(f"Permissao [{p['name']}]", ok, r.status_code,
             "criada" if r.status_code == 201 else ("ja existe" if r.status_code == 409 else "erro"))

    roles_to_create = [
        {"name": "vendedor",   "description": "Vendedor — cria cotacoes"},
        {"name": "aprovador",  "description": "Aprovador — aprova cotacoes"},
        {"name": "gerente",    "description": "Gerente — acesso total a cotacoes"},
    ]

    role_ids: dict[str, str] = {}
    for ro in roles_to_create:
        r = post("/admin/roles/", json_body=ro, token=tok)
        ok = r.status_code in (200, 201, 409)
        rid = r.json().get("id") if r.status_code in (200, 201) else None
        if r.status_code == 409:
            all_r = get("/admin/roles/", token=tok).json()
            existing = next((x for x in all_r if x["name"] == ro["name"]), None)
            rid = existing["id"] if existing else None
        if rid:
            role_ids[ro["name"]] = rid
            kpis["created_roles"].append(ro["name"])
        step(f"Role [{ro['name']}]", ok, r.status_code,
             "criada" if r.status_code == 201 else ("ja existe" if r.status_code == 409 else "erro"))

    console.print()
    console.print("  [dim]Atribuindo permissoes as roles...[/dim]")

    vendedor_perms  = ["cotacao:create"]
    aprovador_perms = ["cotacao:read", "cotacao:approve"]
    gerente_perms   = list(perm_ids.keys())

    assignments = (
        [("vendedor",  p) for p in vendedor_perms] +
        [("aprovador", p) for p in aprovador_perms] +
        [("gerente",   p) for p in gerente_perms]
    )

    for role_name, perm_name in assignments:
        rid = role_ids.get(role_name)
        pid = perm_ids.get(perm_name)
        if not rid or not pid:
            step(f"  Assign {role_name} ← {perm_name}", False, 0, "id nao encontrado")
            continue
        r = post(f"/admin/permissions/{pid}/assign-role/{rid}", token=tok)
        ok = r.status_code == 200
        step(f"  Assign [{role_name}] ← [{perm_name}]", ok, r.status_code)

    r = post("/admin/groups/",
             json_body={"name": "Vendas", "description": "Time de Vendas"},
             token=tok)
    ok = r.status_code in (200, 201, 409)
    gid = r.json().get("id") if r.status_code in (200, 201) else None
    if r.status_code == 409:
        all_g = get("/admin/groups/", token=tok).json()
        ex = next((x for x in all_g if x["name"] == "Vendas"), None)
        gid = ex["id"] if ex else None
    kpis["created_groups"].append("Vendas")
    step("Grupo [Vendas]", ok, r.status_code,
         "criado" if r.status_code == 201 else "ja existe")

    r = post("/admin/rbac/",
             json_body={"key": "sistema", "label": "Sistema de Acesso",
                        "value_type": "string",
                        "description": "Sistema ao qual o usuario tem acesso"},
             token=tok)
    ok = r.status_code in (200, 201, 409)
    step("Atributo RBAC [sistema]", ok, r.status_code,
         "criado" if r.status_code == 201 else "ja existe")

    return role_ids, perm_ids, gid


# ===========================================================================
# BLOCO 5 — Criar usuario1 / vendedor
# ===========================================================================

def create_usuario1(role_ids: dict, gid: str | None):
    tok = kpis["token_admin"]
    console.print(Rule("[bold cyan]5. Criar usuario1 (vendedor)[/bold cyan]", style="cyan"))

    payload = {
        "username":     "usuario1",
        "password":     "usuario1",
        "email":        "usuario1@cotacao.local",
        "full_name":    "Usuario Um — Vendedor",
        "is_active":    True,
        "is_superuser": False,
        "role_names":   [],
    }
    r = post("/admin/users/", json_body=payload, token=tok)
    ok = r.status_code in (200, 201, 409)
    uid = r.json().get("id") if r.status_code in (200, 201) else None

    if r.status_code == 409:
        all_u = get("/admin/users/", token=tok).json()
        ex = next((x for x in all_u if x["username"] == "usuario1"), None)
        uid = ex["id"] if ex else None
        step("Criar usuario1", True, 409, "ja existe — reutilizando")
    else:
        step("Criar usuario1", ok, r.status_code,
             f"id={uid}" if uid else r.text[:80])

    if not uid:
        step("usuario1 id nao encontrado", False, 0)
        return None

    kpis["created_users"].append("usuario1")

    rid = role_ids.get("vendedor")
    if rid:
        r2 = post(f"/admin/roles/{rid}/assign-user/{uid}", token=tok)
        step("Atribuir role [vendedor] a usuario1", r2.status_code == 200, r2.status_code)

    if gid:
        r3 = post(f"/admin/groups/{gid}/assign-user/{uid}", token=tok)
        step("Atribuir grupo [Vendas] a usuario1", r3.status_code == 200, r3.status_code)

    r4 = post(f"/admin/rbac/assign/{uid}",
              json_body={"attribute_key": "sistema", "value": "cotacao"},
              token=tok)
    step("Atribuir RBAC [sistema=cotacao] a usuario1", r4.status_code == 200, r4.status_code)

    return uid


# ===========================================================================
# BLOCO 6 — Login usuario1 e validacao de roles
# ===========================================================================

def test_usuario1_login_and_roles(uid: str | None):
    console.print(Rule("[bold cyan]6. Login usuario1 + Validacao de Roles[/bold cyan]", style="cyan"))

    r = post("/auth/token", form={"username": "usuario1", "password": "usuario1"})
    ok = r.status_code == 200
    step("POST /auth/token (usuario1)", ok, r.status_code)
    if not ok:
        step("Login usuario1 falhou", False, r.status_code, r.text[:120])
        return

    data = r.json()
    kpis["token_usuario1"] = data["access_token"]

    r2 = post("/auth/validate", json_body={"token": kpis["token_usuario1"]})
    ok2 = r2.status_code == 200
    payload = r2.json() if ok2 else {}
    step("POST /auth/validate (usuario1)", ok2, r2.status_code,
         f"sub={payload.get('sub')}")

    roles_no_token = payload.get("roles", [])
    tem_vendedor = "vendedor" in roles_no_token
    step("Token contem role [vendedor]", tem_vendedor, 0, f"roles={roles_no_token}")

    nao_superuser = not payload.get("is_superuser", True)
    step("usuario1 NAO e superuser", nao_superuser, 0,
         f"is_superuser={payload.get('is_superuser')}")

    r3 = get("/admin/users/", token=kpis["token_usuario1"])
    step("GET /admin/users/ com token usuario1 → 403 (nao superuser)",
         r3.status_code == 403, r3.status_code)

    refresh = data.get("refresh_token")
    if refresh:
        r4 = post("/auth/refresh", json_body={"refresh_token": refresh})
        step("POST /auth/refresh (usuario1)", r4.status_code == 200, r4.status_code)

    r5 = post("/auth/logout", token=kpis["token_usuario1"])
    step("POST /auth/logout (usuario1)", r5.status_code == 200, r5.status_code)

    r6 = post("/auth/validate", json_body={"token": kpis["token_usuario1"]})
    step("Token usuario1 invalido apos logout → 401", r6.status_code == 401, r6.status_code)


# ===========================================================================
# BLOCO 7 — Testes de integridade adicionais
# ===========================================================================

def test_integrity():
    tok = kpis["token_admin"]
    console.print(Rule("[bold cyan]7. Integridade & Edge Cases[/bold cyan]", style="cyan"))

    r = post("/auth/token", form={"username": "usuario1", "password": "errada"})
    step("Login usuario1 senha errada → 401", r.status_code == 401, r.status_code)

    r = post("/auth/token", form={"username": "fantasma", "password": "x"})
    step("Login usuario inexistente → 401", r.status_code == 401, r.status_code)

    r = post("/auth/validate", json_body={"token": "token.invalido.aqui"})
    step("Validar token invalido → 401", r.status_code == 401, r.status_code)

    r = get("/admin/settings/", token=tok)
    step("GET /admin/settings/", r.status_code == 200, r.status_code)

    r2 = put("/admin/settings/",
             json_body={"access_token_expire_minutes": 90,
                        "refresh_token_expire_days": 7,
                        "allow_registration": False,
                        "max_login_attempts": 5,
                        "lockout_minutes": 15},
             token=tok)
    step("PUT /admin/settings/ (expire=90min)", r2.status_code == 200, r2.status_code,
         f"expire={r2.json().get('access_token_expire_minutes')}min" if r2.status_code == 200 else "")

    r3 = get("/admin/audit/", token=tok)
    ok3 = r3.status_code == 200
    n_logs = len(r3.json()) if ok3 and isinstance(r3.json(), list) else 0
    step("GET /admin/audit/", ok3, r3.status_code, f"{n_logs} entradas")


# ===========================================================================
# BLOCO 8 — Testes ABAC (/auth/check)
# ===========================================================================

def _fresh_token(username: str, password: str) -> str | None:
    """Faz login e retorna access_token fresco."""
    r = post("/auth/token", form={"username": username, "password": password})
    if r.status_code == 200:
        return r.json().get("access_token")
    return None


def _check(token: str, **kwargs) -> dict:
    """Chama /auth/check e retorna o JSON."""
    body = {"token": token, **kwargs}
    r = post("/auth/check", json_body=body)
    if r.status_code == 200:
        return r.json()
    return {"allowed": False, "reason": f"HTTP {r.status_code}: {r.text[:80]}"}


def setup_abac_usuarios(role_ids: dict, gid: str | None):
    """
    Cria usuarios adicionais para os testes ABAC:
      - gerente1  → role gerente, grupo Vendas, sistema=cotacao, cargo=gerente
      - aprovador1 → role aprovador, sistema=cotacao
    Retorna (uid_gerente, uid_aprovador)
    """
    tok = kpis["token_admin"]

    # ── cria tipo de entidade 'cargo' (ABAC) ──────────────────────────────────
    r = post("/admin/custom-entities/types",
             json_body={"slug": "cargo", "label": "Cargo", "description": "Cargo do usuario"},
             token=tok)
    cargo_type_ok = r.status_code in (201, 409)
    step("Entidade ABAC tipo [cargo]", cargo_type_ok, r.status_code,
         "criado" if r.status_code == 201 else "ja existe")

    # ── cria valor 'gerente' no tipo cargo ────────────────────────────────────
    r = post("/admin/custom-entities/cargo/values",
             json_body={"name": "gerente", "description": "Cargo de gerente"},
             token=tok)
    cargo_val_ok = r.status_code in (201, 409)
    cargo_val_id = r.json().get("id") if r.status_code == 201 else None
    if r.status_code == 409:
        rv = get("/admin/custom-entities/cargo/values", token=tok)
        ex = next((x for x in rv.json() if x["name"] == "gerente"), None)
        cargo_val_id = ex["id"] if ex else None
    step("Entidade ABAC valor [cargo=gerente]", cargo_val_ok, r.status_code,
         "criado" if r.status_code == 201 else "ja existe")

    # ── cria valor 'vendedor' no tipo cargo ───────────────────────────────────
    r = post("/admin/custom-entities/cargo/values",
             json_body={"name": "vendedor", "description": "Cargo de vendedor"},
             token=tok)
    cargo_vend_id = r.json().get("id") if r.status_code == 201 else None
    if r.status_code == 409:
        rv = get("/admin/custom-entities/cargo/values", token=tok)
        ex = next((x for x in rv.json() if x["name"] == "vendedor"), None)
        cargo_vend_id = ex["id"] if ex else None
    step("Entidade ABAC valor [cargo=vendedor]", r.status_code in (201, 409), r.status_code,
         "criado" if r.status_code == 201 else "ja existe")

    # ── gerente1 ──────────────────────────────────────────────────────────────
    r = post("/admin/users/",
             json_body={"username": "gerente1", "password": "gerente1",
                        "email": "gerente1@cotacao.local",
                        "full_name": "Gerente Um", "is_active": True,
                        "is_superuser": False, "role_names": []},
             token=tok)
    uid_g = r.json().get("id") if r.status_code in (200, 201) else None
    if r.status_code == 409:
        all_u = get("/admin/users/", token=tok).json()
        ex = next((x for x in all_u if x["username"] == "gerente1"), None)
        uid_g = ex["id"] if ex else None
    step("Criar gerente1", r.status_code in (200, 201, 409), r.status_code,
         "ja existe" if r.status_code == 409 else f"id={uid_g}")

    if uid_g:
        kpis["created_users"].append("gerente1")
        rid_g = role_ids.get("gerente")
        if rid_g:
            r2 = post(f"/admin/roles/{rid_g}/assign-user/{uid_g}", token=tok)
            step("Atribuir role [gerente] a gerente1", r2.status_code == 200, r2.status_code)
        if gid:
            r3 = post(f"/admin/groups/{gid}/assign-user/{uid_g}", token=tok)
            step("Atribuir grupo [Vendas] a gerente1", r3.status_code == 200, r3.status_code)
        r4 = post(f"/admin/rbac/assign/{uid_g}",
                  json_body={"attribute_key": "sistema", "value": "cotacao"}, token=tok)
        step("Atribuir RBAC [sistema=cotacao] a gerente1", r4.status_code == 200, r4.status_code)
        if cargo_val_id:
            r5 = post(f"/admin/custom-entities/assign/{uid_g}",
                      json_body={"entity_type_slug": "cargo", "entity_value_id": cargo_val_id},
                      token=tok)
            step("Atribuir ABAC [cargo=gerente] a gerente1", r5.status_code == 200, r5.status_code)

    # ── aprovador1 ────────────────────────────────────────────────────────────
    r = post("/admin/users/",
             json_body={"username": "aprovador1", "password": "aprovador1",
                        "email": "aprovador1@cotacao.local",
                        "full_name": "Aprovador Um", "is_active": True,
                        "is_superuser": False, "role_names": []},
             token=tok)
    uid_a = r.json().get("id") if r.status_code in (200, 201) else None
    if r.status_code == 409:
        all_u = get("/admin/users/", token=tok).json()
        ex = next((x for x in all_u if x["username"] == "aprovador1"), None)
        uid_a = ex["id"] if ex else None
    step("Criar aprovador1", r.status_code in (200, 201, 409), r.status_code,
         "ja existe" if r.status_code == 409 else f"id={uid_a}")

    if uid_a:
        kpis["created_users"].append("aprovador1")
        rid_a = role_ids.get("aprovador")
        if rid_a:
            r2 = post(f"/admin/roles/{rid_a}/assign-user/{uid_a}", token=tok)
            step("Atribuir role [aprovador] a aprovador1", r2.status_code == 200, r2.status_code)
        r3 = post(f"/admin/rbac/assign/{uid_a}",
                  json_body={"attribute_key": "sistema", "value": "cotacao"}, token=tok)
        step("Atribuir RBAC [sistema=cotacao] a aprovador1", r3.status_code == 200, r3.status_code)

    # atribui cargo=vendedor a usuario1 (para testes ABAC de cargo)
    all_u = get("/admin/users/", token=tok).json()
    uid_u1 = next((x["id"] for x in all_u if x["username"] == "usuario1"), None)
    if uid_u1 and cargo_vend_id:
        r = post(f"/admin/custom-entities/assign/{uid_u1}",
                 json_body={"entity_type_slug": "cargo", "entity_value_id": cargo_vend_id},
                 token=tok)
        step("Atribuir ABAC [cargo=vendedor] a usuario1", r.status_code == 200, r.status_code)

    return uid_g, uid_a


def test_abac(role_ids: dict, gid: str | None):
    console.print(Rule("[bold cyan]8. Testes ABAC — /auth/check[/bold cyan]", style="cyan"))

    # ── setup: cria usuarios ABAC e obtém tokens frescos ─────────────────────
    uid_g, uid_a = setup_abac_usuarios(role_ids, gid)
    console.print()

    tok_admin    = kpis["token_admin"]
    tok_usuario1 = _fresh_token("usuario1", "usuario1")
    tok_gerente  = _fresh_token("gerente1", "gerente1")
    tok_aprovador = _fresh_token("aprovador1", "aprovador1")
    kpis["token_gerente"] = tok_gerente

    if not tok_usuario1:
        step("Login usuario1 para ABAC", False, 0, "falhou")
        return
    if not tok_gerente:
        step("Login gerente1 para ABAC", False, 0, "falhou")
        return

    console.print("  [dim]Iniciando testes /auth/check...[/dim]")
    console.print()

    # ── 8.1 Superuser passa em tudo ───────────────────────────────────────────
    console.print("  [bold yellow]8.1 Superuser bypass[/bold yellow]")
    res = _check(tok_admin, require_roles=["vendedor"], require_abac={"sistema": "cotacao"})
    step("Superuser: allowed=True (bypass tudo)", res.get("allowed") is True, 0,
         f"reason={res.get('reason')}")

    # ── 8.2 Verificacao de role unica ─────────────────────────────────────────
    console.print("  [bold yellow]8.2 Verificacao de role[/bold yellow]")
    res = _check(tok_usuario1, require_roles=["vendedor"])
    step("usuario1 tem role [vendedor] → allowed", res.get("allowed") is True, 0,
         f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_roles=["aprovador"])
    step("usuario1 NAO tem role [aprovador] → denied", res.get("allowed") is False, 0,
         f"reason={res.get('reason')}")

    res = _check(tok_gerente, require_roles=["gerente"])
    step("gerente1 tem role [gerente] → allowed", res.get("allowed") is True, 0,
         f"reason={res.get('reason')}")

    # ── 8.3 require_any_role (qualquer uma) ───────────────────────────────────
    console.print("  [bold yellow]8.3 require_roles (qualquer uma)[/bold yellow]")
    res = _check(tok_usuario1, require_roles=["aprovador", "vendedor"])
    step("usuario1: require_roles=[aprovador,vendedor] → allowed (tem vendedor)",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_roles=["aprovador", "gerente"])
    step("usuario1: require_roles=[aprovador,gerente] → denied (nao tem nenhuma)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    # ── 8.4 require_all_roles (todas obrigatorias) ────────────────────────────
    console.print("  [bold yellow]8.4 require_all_roles (todas)[/bold yellow]")
    res = _check(tok_gerente, require_all_roles=["gerente"])
    step("gerente1: require_all_roles=[gerente] → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_all_roles=["vendedor", "aprovador"])
    step("usuario1: require_all_roles=[vendedor,aprovador] → denied (falta aprovador)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    # ── 8.5 Verificacao de permissao ──────────────────────────────────────────
    console.print("  [bold yellow]8.5 Verificacao de permissao[/bold yellow]")
    res = _check(tok_usuario1, require_permissions=["cotacao:create"])
    step("usuario1 tem permissao [cotacao:create] → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_permissions=["cotacao:approve"])
    step("usuario1 NAO tem permissao [cotacao:approve] → denied",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    res = _check(tok_gerente, require_permissions=["cotacao:approve", "cotacao:delete"])
    step("gerente1 tem [cotacao:approve] ou [cotacao:delete] → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    # ── 8.6 Verificacao ABAC simples (atributo RBAC) ──────────────────────────
    console.print("  [bold yellow]8.6 ABAC — atributo RBAC (sistema)[/bold yellow]")
    res = _check(tok_usuario1, require_abac={"sistema": "cotacao"})
    step("usuario1: ABAC sistema=cotacao → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_abac={"sistema": "financeiro"})
    step("usuario1: ABAC sistema=financeiro → denied (tem cotacao)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    res = _check(tok_gerente, require_abac={"sistema": "cotacao"})
    step("gerente1: ABAC sistema=cotacao → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    # ── 8.7 ABAC com entidade customizada (cargo) ─────────────────────────────
    console.print("  [bold yellow]8.7 ABAC — entidade customizada (cargo)[/bold yellow]")
    res = _check(tok_gerente, require_abac={"cargo": "gerente"})
    step("gerente1: ABAC cargo=gerente → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_gerente, require_abac={"cargo": "vendedor"})
    step("gerente1: ABAC cargo=vendedor → denied (tem gerente)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1, require_abac={"cargo": "vendedor"})
    step("usuario1: ABAC cargo=vendedor → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    # ── 8.8 ABAC combinado: role + atributo ───────────────────────────────────
    console.print("  [bold yellow]8.8 ABAC combinado: role + atributo[/bold yellow]")
    res = _check(tok_usuario1,
                 require_roles=["vendedor"],
                 require_abac={"sistema": "cotacao"})
    step("usuario1: role=vendedor AND sistema=cotacao → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1,
                 require_roles=["vendedor"],
                 require_abac={"sistema": "financeiro"})
    step("usuario1: role=vendedor AND sistema=financeiro → denied (ABAC falha)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    res = _check(tok_gerente,
                 require_roles=["gerente"],
                 require_abac={"sistema": "cotacao", "cargo": "gerente"})
    step("gerente1: role=gerente AND sistema=cotacao AND cargo=gerente → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_usuario1,
                 require_roles=["gerente"],
                 require_abac={"sistema": "cotacao"})
    step("usuario1: role=gerente AND sistema=cotacao → denied (role falha)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    # ── 8.9 ABAC combinado: permissao + atributo ──────────────────────────────
    console.print("  [bold yellow]8.9 ABAC combinado: permissao + atributo[/bold yellow]")
    res = _check(tok_usuario1,
                 require_permissions=["cotacao:create"],
                 require_abac={"sistema": "cotacao"})
    step("usuario1: perm=cotacao:create AND sistema=cotacao → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_aprovador,
                 require_permissions=["cotacao:approve"],
                 require_abac={"sistema": "cotacao"})
    step("aprovador1: perm=cotacao:approve AND sistema=cotacao → allowed",
         res.get("allowed") is True, 0, f"reason={res.get('reason')}")

    res = _check(tok_aprovador,
                 require_permissions=["cotacao:delete"],
                 require_abac={"sistema": "cotacao"})
    step("aprovador1: perm=cotacao:delete AND sistema=cotacao → denied (sem perm)",
         res.get("allowed") is False, 0, f"reason={res.get('reason')}")

    # ── 8.10 Token invalido no /auth/check ────────────────────────────────────
    console.print("  [bold yellow]8.10 Token invalido no /auth/check[/bold yellow]")
    res = _check("token.invalido.aqui", require_roles=["vendedor"])
    step("/auth/check com token invalido → denied",
         res.get("allowed") is False, 0, f"reason={res.get('reason')[:60]}")

    # ── 8.11 Payload ABAC no token (validacao via /auth/validate) ─────────────
    console.print("  [bold yellow]8.11 Payload ABAC no token[/bold yellow]")
    r = post("/auth/validate", json_body={"token": tok_gerente})
    if r.status_code == 200:
        p = r.json()
        abac = p.get("abac", {})
        step("Token gerente1 contem abac.sistema=cotacao",
             abac.get("sistema") == "cotacao", 0, f"abac={abac}")
        step("Token gerente1 contem abac.cargo=gerente",
             abac.get("cargo") == "gerente", 0, f"cargo={abac.get('cargo')}")
        step("Token gerente1 contem roles=[gerente]",
             "gerente" in p.get("roles", []), 0, f"roles={p.get('roles')}")
        step("Token gerente1 contem permissions cotacao:*",
             any("cotacao" in perm for perm in p.get("permissions", [])), 0,
             f"perms={p.get('permissions')}")
    else:
        step("Validar token gerente1", False, r.status_code, r.text[:80])

    r2 = post("/auth/validate", json_body={"token": tok_usuario1})
    if r2.status_code == 200:
        p2 = r2.json()
        abac2 = p2.get("abac", {})
        step("Token usuario1 contem abac.cargo=vendedor",
             abac2.get("cargo") == "vendedor", 0, f"abac={abac2}")
    else:
        step("Validar token usuario1 (ABAC)", False, r2.status_code)

    # ── 8.12 require_level_gte (nivel minimo) ─────────────────────────────────
    console.print("  [bold yellow]8.12 require_level_gte[/bold yellow]")
    # sem nivel configurado → rank=0, level_gte(0) = True
    res = _check(tok_usuario1, require_level_gte=0)
    step("usuario1: require_level_gte=0 → allowed (rank=0 >= 0)",
         res.get("allowed") is True, 0, f"rank={res.get('user_level_rank')}")

    res = _check(tok_usuario1, require_level_gte=10)
    step("usuario1: require_level_gte=10 → denied (rank=0 < 10)",
         res.get("allowed") is False, 0, f"rank={res.get('user_level_rank')}")

    # ── 8.13 Resposta ABAC inclui campos corretos ─────────────────────────────
    console.print("  [bold yellow]8.13 Estrutura da resposta /auth/check[/bold yellow]")
    res = _check(tok_gerente, require_roles=["gerente"])
    campos_ok = all(k in res for k in ("allowed", "reason", "subject", "roles",
                                        "permissions", "abac", "user_level_rank"))
    step("Resposta /auth/check tem todos os campos esperados", campos_ok, 0,
         f"campos={list(res.keys())}")
    step("subject=gerente1 na resposta",
         res.get("subject") == "gerente1", 0, f"subject={res.get('subject')}")


# ===========================================================================
# RELATORIO — salva YAML, MD, JSON
# ===========================================================================

def save_reports(elapsed: float):
    ts_str  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pct     = int(kpis["passed"] / kpis["total"] * 100) if kpis["total"] else 0
    status  = "PASSED" if kpis["failed"] == 0 else "PARTIAL" if pct >= 50 else "FAILED"

    report = {
        "run_id":     RUN_ID,
        "timestamp":  ts_str,
        "status":     status,
        "elapsed_s":  round(elapsed, 2),
        "kpis": {
            "total_steps":   kpis["total"],
            "passed":        kpis["passed"],
            "failed":        kpis["failed"],
            "success_rate":  f"{pct}%",
        },
        "setup": {
            "roles_created":       kpis["created_roles"],
            "permissions_created": kpis["created_permissions"],
            "users_created":       kpis["created_users"],
            "groups_created":      kpis["created_groups"],
        },
        "steps": results,
    }

    base = os.path.join(LOGS_DIR, f"run_{RUN_ID}")

    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    with open(f"{base}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(report, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    passed_icon = "✅" if status == "PASSED" else "⚠️" if status == "PARTIAL" else "❌"
    lines = [
        f"# {passed_icon} Apollo IAM Engine — Production Test Report",
        f"",
        f"| Campo | Valor |",
        f"|-------|-------|",
        f"| Run ID | `{RUN_ID}` |",
        f"| Data/Hora | {ts_str} |",
        f"| Status | **{status}** |",
        f"| Tempo | {elapsed:.2f}s |",
        f"| Total Steps | {kpis['total']} |",
        f"| ✅ Passed | {kpis['passed']} |",
        f"| ❌ Failed | {kpis['failed']} |",
        f"| Taxa de Sucesso | **{pct}%** |",
        f"",
        f"## Setup RBAC — Sistema de Cotacao",
        f"",
        f"| Tipo | Itens |",
        f"|------|-------|",
        f"| Roles | {', '.join(kpis['created_roles']) or '—'} |",
        f"| Permissoes | {', '.join(kpis['created_permissions']) or '—'} |",
        f"| Usuarios | {', '.join(kpis['created_users']) or '—'} |",
        f"| Grupos | {', '.join(kpis['created_groups']) or '—'} |",
        f"",
        f"## Steps",
        f"",
        f"| # | Step | Status | HTTP | Detalhe |",
        f"|---|------|--------|------|---------|",
    ]
    for i, r in enumerate(results, 1):
        icon = "✅" if r["ok"] else "❌"
        lines.append(
            f"| {i} | {r['step']} | {icon} | "
            f"{r['status_code'] or '—'} | {r['detail'] or '—'} |"
        )
    lines += ["", f"---", f"*Gerado por O2 Data Solutions — Apollo IAM Engine*"]

    with open(f"{base}.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return base, status, pct


# ===========================================================================
# RELATORIO CONSOLE — rich
# ===========================================================================

def print_report(elapsed: float, base_path: str, status: str, pct: int):
    console.print()
    console.print(Rule("[bold white]Relatorio Final[/bold white]"))
    console.print()

    kpi_table = Table(title="📊 KPIs do Run", border_style="orange1", show_lines=True)
    kpi_table.add_column("Indicador",      style="bold cyan",  min_width=28)
    kpi_table.add_column("Valor",          style="bold green", min_width=14)

    status_color = "green" if status == "PASSED" else "yellow" if status == "PARTIAL" else "red"
    kpi_table.add_row("🆔 Run ID",                RUN_ID)
    kpi_table.add_row("📅 Timestamp",             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    kpi_table.add_row(f"[{status_color}]🏁 Status[/{status_color}]",
                      f"[{status_color}]{status}[/{status_color}]")
    kpi_table.add_row("⏱️  Tempo total",           f"{elapsed:.2f}s")
    kpi_table.add_row("🔢 Total de steps",         str(kpis["total"]))
    kpi_table.add_row("✅ Passed",                 str(kpis["passed"]))
    kpi_table.add_row("❌ Failed",                 str(kpis["failed"]))
    kpi_table.add_row("📈 Taxa de sucesso",        f"{pct}%")
    console.print(kpi_table)
    console.print()

    setup_table = Table(title="🔧 Setup RBAC — Sistema de Cotacao",
                        border_style="cyan", show_lines=True)
    setup_table.add_column("Tipo",   style="bold white", min_width=16)
    setup_table.add_column("Itens",  style="bold green", min_width=40)
    setup_table.add_row("🎭 Roles",       ", ".join(kpis["created_roles"]) or "—")
    setup_table.add_row("🔑 Permissoes",  ", ".join(kpis["created_permissions"]) or "—")
    setup_table.add_row("👤 Usuarios",    ", ".join(kpis["created_users"]) or "—")
    setup_table.add_row("👥 Grupos",      ", ".join(kpis["created_groups"]) or "—")
    console.print(setup_table)
    console.print()

    steps_table = Table(title="📋 Steps Detalhados", border_style="dim", show_lines=True)
    steps_table.add_column("#",       style="dim",        width=4)
    steps_table.add_column("Step",    style="white",      min_width=50)
    steps_table.add_column("Status",  style="bold",       width=6)
    steps_table.add_column("HTTP",    style="dim cyan",   width=6)
    steps_table.add_column("Detalhe", style="dim",        min_width=20)

    for i, r in enumerate(results, 1):
        icon  = "✅" if r["ok"] else "❌"
        color = "green" if r["ok"] else "red"
        steps_table.add_row(
            str(i),
            f"[{color}]{r['step']}[/{color}]",
            icon,
            str(r["status_code"]) if r["status_code"] else "—",
            r["detail"] or "—",
        )
    console.print(steps_table)
    console.print()

    files_table = Table(title="💾 Relatorios Salvos", border_style="green", show_lines=True)
    files_table.add_column("Formato", style="bold cyan",  width=8)
    files_table.add_column("Arquivo", style="bold white", min_width=50)
    for ext in ("json", "yaml", "md"):
        files_table.add_row(ext.upper(), f"{base_path}.{ext}")
    console.print(files_table)
    console.print()

    if status == "PASSED":
        console.print(Panel.fit(
            f"[bold green]🎉 Todos os {kpis['total']} steps passaram![/bold green]\n"
            f"[dim]ABAC testado: roles, permissoes, atributos, entidades customizadas[/dim]\n"
            f"[dim]Relatorios em: project-test-run-setup-logs/[/dim]",
            border_style="green",
        ))
    else:
        failed_steps = [r["step"] for r in results if not r["ok"]]
        console.print(Panel.fit(
            f"[bold yellow]⚠️  {pct}% — {kpis['failed']} step(s) falharam[/bold yellow]\n"
            + "\n".join(f"  [red]• {s}[/red]" for s in failed_steps[:10])
            + f"\n[dim]Relatorios em: project-test-run-setup-logs/[/dim]",
            border_style="yellow",
        ))


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    _start = time.time()

    console.print()
    console.print(Panel.fit(
        "[bold orange1]🧪 APOLLO IAM ENGINE — Production Test[/bold orange1]\n"
        f"[dim]API: {API_BASE}  {'🔐 mTLS' if _MTLS else '🔓 HTTP'}[/dim]\n"
        "[dim]Testando API, RBAC, ABAC, usuario1/vendedor, gerente1, aprovador1...[/dim]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1",
        padding=(1, 4),
    ))
    console.print()

    test_health()
    console.print()

    test_auth_admin()
    console.print()

    test_admin_routes()
    console.print()

    role_ids, perm_ids, gid = setup_rbac_cotacao()
    console.print()

    uid = create_usuario1(role_ids, gid)
    console.print()

    test_usuario1_login_and_roles(uid)
    console.print()

    test_integrity()
    console.print()

    test_abac(role_ids, gid)
    console.print()

    elapsed = time.time() - _start
    base_path, status, pct = save_reports(elapsed)
    print_report(elapsed, base_path, status, pct)
"""  """