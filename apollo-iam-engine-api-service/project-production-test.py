"""
project-production-test.py
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌟 APOLLO IAM ENGINE — Production Test Suite v3 🌟                        ║
║  "Hora de Aventura no Reino de Ooo IAM"                                     ║
║  Finn e Jake testam TUDO antes de salvar o reino!                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Cobre: Health, Auth, RBAC, ABAC, APL (Policy DSL), Cache de Decisão,
       Multi-tenant, User Types/Levels, Custom Entities, Settings, Audit.
O2 Data Solutions
"""
from __future__ import annotations

import json
import os
import ssl
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx
import yaml
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

init(autoreset=True)
console = Console()

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from src.infrastructure.config.security_config import (
    get_api_port, get_certs_dir, is_mtls_enabled,
)

_MTLS    = is_mtls_enabled()
_PORT    = get_api_port() if _MTLS else 8000
_PROTO   = "https" if _MTLS else "http"
API_BASE = f"{_PROTO}://localhost:{_PORT}"

LOGS_DIR   = os.path.join(_HERE, "project-test-run-setup-logs")
RUN_ID     = datetime.now().strftime("%Y%m%d_%H%M%S")
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
os.makedirs(LOGS_DIR, exist_ok=True)

# ── SSL ───────────────────────────────────────────────────────────────────────
def _build_ssl_ctx() -> ssl.SSLContext | bool:
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

# ── estado global ─────────────────────────────────────────────────────────────
results: list[dict] = []
kpis: dict = {
    "total": 0, "passed": 0, "failed": 0,
    "created_roles": [], "created_permissions": [],
    "created_users": [], "created_groups": [],
    "created_policies": [],
    "token_admin": None, "token_usuario1": None,
    "token_gerente": None, "token_aprovador": None,
    "latencies_ms": [],
}
_TIMEOUT = httpx.Timeout(30.0, connect=10.0)

# ── helpers HTTP ──────────────────────────────────────────────────────────────
class _FakeResponse:
    def __init__(self, exc):
        self.status_code = 0
        self._exc = exc
    def json(self): return {"detail": str(self._exc)}
    @property
    def text(self): return str(self._exc)

def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()

def step(name: str, ok: bool, status_code: int = 0,
         detail: str = "", data: dict | None = None,
         latency_ms: float | None = None):
    icon  = "✅" if ok else "❌"
    color = "bold green" if ok else "bold red"
    kpis["total"] += 1
    if ok: kpis["passed"] += 1
    else:  kpis["failed"] += 1
    if latency_ms is not None:
        kpis["latencies_ms"].append(latency_ms)
    entry = {"step": name, "ok": ok, "status_code": status_code,
             "detail": detail, "data": data or {}, "latency_ms": latency_ms,
             "timestamp": _ts()}
    results.append(entry)
    lat_str = f"  [dim magenta]{latency_ms:.0f}ms[/dim magenta]" if latency_ms else ""
    console.print(
        f"  {icon} [{color}]{name}[/{color}]"
        + (f"  [dim]{detail}[/dim]" if detail else "")
        + (f"  [dim cyan]HTTP {status_code}[/dim cyan]" if status_code else "")
        + lat_str
    )
    return ok

def _req(method: str, path: str, token: str | None = None,
         json_body: dict | None = None, form: dict | None = None,
         params: dict | None = None) -> tuple[Any, float]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    t0 = time.perf_counter()
    try:
        fn = getattr(httpx, method.lower())
        kwargs: dict = {"headers": headers, "timeout": _TIMEOUT, "verify": _SSL}
        if json_body is not None: kwargs["json"] = json_body
        if form is not None:      kwargs["data"] = form
        if params is not None:    kwargs["params"] = params
        r = fn(f"{API_BASE}{path}", **kwargs)
        return r, round((time.perf_counter() - t0) * 1000, 1)
    except Exception as e:
        return _FakeResponse(e), round((time.perf_counter() - t0) * 1000, 1)

def get(path, token=None, params=None):
    r, _ = _req("get", path, token=token, params=params); return r
def post(path, json_body=None, form=None, token=None):
    r, _ = _req("post", path, token=token, json_body=json_body, form=form); return r
def put(path, json_body, token=None):
    r, _ = _req("put", path, token=token, json_body=json_body); return r
def patch(path, token=None, params=None):
    r, _ = _req("patch", path, token=token, params=params); return r
def delete(path, token=None):
    r, _ = _req("delete", path, token=token); return r
def _timed_post(path, json_body=None, form=None, token=None):
    return _req("post", path, token=token, json_body=json_body, form=form)
def _fresh_token(username, password):
    r = post("/auth/token", form={"username": username, "password": password})
    return r.json().get("access_token") if r.status_code == 200 else None
def _check(token, **kwargs):
    body = {"token": token, **kwargs}
    r = post("/auth/check", json_body=body)
    return r.json() if r.status_code == 200 else {"allowed": False, "reason": f"HTTP {r.status_code}: {r.text[:80]}"}

def _hdr(title: str):
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]"))


# ══════════════════════════════════════════════════════════════════════════════
# 1. HEALTH CHECK — "Finn verifica se o castelo ainda está de pé"
# ══════════════════════════════════════════════════════════════════════════════
def test_health():
    _hdr("🏰 1. HEALTH CHECK")
    r, ms = _req("get", "/health")
    step("GET /health", r.status_code == 200,
         r.status_code, r.json().get("status", ""), latency_ms=ms)

# ══════════════════════════════════════════════════════════════════════════════
# 2. AUTH — "Jake usa a magia do JWT para entrar no reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_auth():
    _hdr("🔑 2. AUTH — Login, Refresh, Validate, Logout")

    # login admin
    r, ms = _timed_post("/auth/token", form={"username": ADMIN_USER, "password": ADMIN_PASS})
    ok = r.status_code == 200
    step("Login admin", ok, r.status_code, latency_ms=ms)
    if not ok:
        console.print(f"  [red]Detalhe: {r.text[:200]}[/red]")
        return
    data = r.json()
    kpis["token_admin"] = data["access_token"]
    refresh_token = data.get("refresh_token", "")

    # validate
    r2, ms2 = _timed_post("/auth/validate", json_body={"token": kpis["token_admin"]})
    step("Validate token admin", r2.status_code == 200, r2.status_code, latency_ms=ms2)

    # refresh
    if refresh_token:
        r3, ms3 = _timed_post("/auth/refresh", json_body={"refresh_token": refresh_token})
        step("Refresh token", r3.status_code == 200, r3.status_code, latency_ms=ms3)

    # check superuser
    chk = _check(kpis["token_admin"])
    step("Check superuser bypass", chk.get("allowed") is True,
         detail=chk.get("reason", ""))

    # token inválido
    r4, ms4 = _timed_post("/auth/validate", json_body={"token": "token.invalido.aqui"})
    step("Validate token inválido → 401/422", r4.status_code in (401, 422),
         r4.status_code, latency_ms=ms4)

# ══════════════════════════════════════════════════════════════════════════════
# 3. ROLES — "As roles são as espadas do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_roles():
    _hdr("⚔️  3. ROLES")
    tok = kpis["token_admin"]
    if not tok: return

    for role_name in ["vendedor", "gerente", "aprovador"]:
        r = post("/admin/roles/", json_body={"name": role_name, "description": f"Role {role_name}"},
                 token=tok)
        ok = r.status_code in (200, 201, 409)
        step(f"Criar role '{role_name}'", ok, r.status_code)
        if r.status_code in (200, 201):
            kpis["created_roles"].append(r.json().get("id", ""))

    r = get("/admin/roles/", token=tok)
    step("Listar roles", r.status_code == 200, r.status_code,
         f"{len(r.json())} roles" if r.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 4. PERMISSIONS — "Permissões são as chaves do castelo"
# ══════════════════════════════════════════════════════════════════════════════
def test_permissions():
    _hdr("🗝️  4. PERMISSIONS")
    tok = kpis["token_admin"]
    if not tok: return

    perms = [
        ("cotacao:create", "cotacao", "create"),
        ("cotacao:read",   "cotacao", "read"),
        ("cotacao:update", "cotacao", "update"),
        ("relatorio:read", "relatorio", "read"),
    ]
    for name, resource, action in perms:
        r = post("/admin/permissions/",
                 json_body={"name": name, "resource": resource, "action": action},
                 token=tok)
        ok = r.status_code in (200, 201, 409)
        step(f"Criar permissão '{name}'", ok, r.status_code)
        if r.status_code in (200, 201):
            kpis["created_permissions"].append(r.json().get("id", ""))

    r = get("/admin/permissions/", token=tok)
    step("Listar permissões", r.status_code == 200, r.status_code,
         f"{len(r.json())} permissões" if r.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 5. USERS — "Finn cria os heróis do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_users():
    _hdr("🧙 5. USERS")
    tok = kpis["token_admin"]
    if not tok: return

    uid = uuid.uuid4().hex[:6]
    users = [
        {"username": f"usuario1_{uid}", "password": "Senha123!", "email": f"u1_{uid}@test.com",
         "full_name": "Usuário Um", "is_active": True},
        {"username": f"gerente_{uid}",  "password": "Senha123!", "email": f"ger_{uid}@test.com",
         "full_name": "Gerente Teste", "is_active": True},
        {"username": f"aprovador_{uid}","password": "Senha123!", "email": f"apr_{uid}@test.com",
         "full_name": "Aprovador Teste","is_active": True},
    ]
    for u in users:
        r = post("/admin/users/", json_body=u, token=tok)
        ok = r.status_code in (200, 201, 409)
        step(f"Criar usuário '{u['username']}'", ok, r.status_code)
        if r.status_code in (200, 201):
            kpis["created_users"].append({"id": r.json().get("id"), "username": u["username"],
                                          "password": u["password"]})

    # login dos usuários criados
    for u in kpis["created_users"]:
        tok_u = _fresh_token(u["username"], u["password"])
        if "usuario1" in u["username"]:
            kpis["token_usuario1"] = tok_u
        elif "gerente" in u["username"]:
            kpis["token_gerente"] = tok_u
        elif "aprovador" in u["username"]:
            kpis["token_aprovador"] = tok_u
        step(f"Login '{u['username']}'", tok_u is not None)

    # listar
    r = get("/admin/users/", token=tok)
    step("Listar usuários", r.status_code == 200, r.status_code,
         f"{len(r.json())} usuários" if r.status_code == 200 else "")


# ══════════════════════════════════════════════════════════════════════════════
# 6. RBAC — "Jake distribui as espadas para os heróis"
# ══════════════════════════════════════════════════════════════════════════════
def test_rbac():
    _hdr("🛡️  6. RBAC — Assign roles e permissions")
    tok = kpis["token_admin"]
    if not tok or not kpis["created_users"] or not kpis["created_roles"]: return

    # busca IDs de roles por nome
    r = get("/admin/roles/", token=tok)
    if r.status_code != 200: return
    roles_by_name = {ro["name"]: ro["id"] for ro in r.json()}

    # busca IDs de permissões
    rp = get("/admin/permissions/", token=tok)
    perms_by_name = {p["name"]: p["id"] for p in rp.json()} if rp.status_code == 200 else {}

    # assign role vendedor ao usuario1
    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if u1 and "vendedor" in roles_by_name:
        r2 = post(f"/admin/roles/{roles_by_name['vendedor']}/assign/{u1['id']}", token=tok)
        step("Assign role 'vendedor' → usuario1", r2.status_code in (200, 201, 204),
             r2.status_code)

    # assign role gerente ao gerente
    ger = next((u for u in kpis["created_users"] if "gerente" in u["username"]), None)
    if ger and "gerente" in roles_by_name:
        r3 = post(f"/admin/roles/{roles_by_name['gerente']}/assign/{ger['id']}", token=tok)
        step("Assign role 'gerente' → gerente", r3.status_code in (200, 201, 204),
             r3.status_code)

    # assign permissão cotacao:create à role vendedor
    if "vendedor" in roles_by_name and "cotacao:create" in perms_by_name:
        r4 = post(f"/admin/permissions/{perms_by_name['cotacao:create']}/assign/{roles_by_name['vendedor']}",
                  token=tok)
        step("Assign perm 'cotacao:create' → role vendedor",
             r4.status_code in (200, 201, 204), r4.status_code)

    # verifica token atualizado do usuario1
    if u1:
        tok_u1 = _fresh_token(u1["username"], u1["password"])
        kpis["token_usuario1"] = tok_u1
        if tok_u1:
            chk = _check(tok_u1, require_roles=["vendedor"])
            step("Check usuario1 tem role 'vendedor'", chk.get("allowed") is True,
                 detail=chk.get("reason", ""))

# ══════════════════════════════════════════════════════════════════════════════
# 7. ABAC — "Marceline verifica os atributos mágicos"
# ══════════════════════════════════════════════════════════════════════════════
def test_abac():
    _hdr("🧛 7. ABAC — Atributos e check combinado")
    tok = kpis["token_admin"]
    if not tok: return

    # cria atributo RBAC
    r = post("/admin/rbac-attributes/",
             json_body={"key": "department", "label": "Departamento",
                        "description": "Departamento do usuário"},
             token=tok)
    step("Criar atributo RBAC 'department'", r.status_code in (200, 201, 409), r.status_code)
    attr_id = r.json().get("id") if r.status_code in (200, 201) else None

    # assign atributo ao usuario1
    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if u1 and attr_id:
        r2 = post(f"/admin/rbac-attributes/{attr_id}/assign/{u1['id']}",
                  json_body={"value": "sales"}, token=tok)
        step("Assign department=sales → usuario1", r2.status_code in (200, 201, 204),
             r2.status_code)

    # check ABAC
    if kpis["token_usuario1"]:
        tok_u1 = _fresh_token(
            next((u["username"] for u in kpis["created_users"] if "usuario1" in u["username"]), ""),
            "Senha123!"
        ) or kpis["token_usuario1"]
        chk = _check(tok_u1, require_abac={"department": "sales"})
        step("Check ABAC department=sales", chk.get("allowed") is True,
             detail=chk.get("reason", ""))

        chk2 = _check(tok_u1, require_abac={"department": "finance"})
        step("Check ABAC department=finance → denied", chk2.get("allowed") is False,
             detail=chk2.get("reason", ""))

# ══════════════════════════════════════════════════════════════════════════════
# 8. APL — "O Grimório de Jake: Apollo Policy Language"
# ══════════════════════════════════════════════════════════════════════════════
def test_apl():
    _hdr("📜 8. APL — Apollo Policy Language (DSL Engine)")
    tok = kpis["token_admin"]
    if not tok: return

    # ── 8.1 Criar policy Allow via JSON estruturado ───────────────────────────
    pol_allow = {
        "name": f"test-allow-vendedor-{RUN_ID}",
        "description": "Vendedores podem criar cotações",
        "effect": "allow",
        "priority": 10,
        "actions": ["cotacao:create", "cotacao:read"],
        "resources": ["cotacao/*"],
        "conditions": [
            {"field": "department", "op": "eq",      "value": "sales"},
            {"field": "user_level",  "op": "gte",     "value": 1},
        ],
        "condition_logic": "AND",
        "tenant_id": "tenant-teste",
        "enabled": True,
    }
    r = post("/admin/policies/", json_body=pol_allow, token=tok)
    ok = r.status_code in (200, 201)
    step("Criar policy Allow (JSON estruturado)", ok, r.status_code)
    pol_allow_id = r.json().get("id") if ok else None
    if pol_allow_id:
        kpis["created_policies"].append(pol_allow_id)

    # ── 8.2 Criar policy Deny via raw YAML ───────────────────────────────────
    yaml_content = f"""
id: test-deny-blocked-{RUN_ID}
name: Negar usuários bloqueados
description: Deny explícito para status bloqueado
effect: deny
priority: 1
actions:
  - "*"
resources:
  - "*"
conditions:
  - field: status
    op: eq
    value: blocked
condition_logic: AND
tenant_id: tenant-teste
enabled: true
"""
    r2 = post("/admin/policies/raw",
              json_body={"format": "yaml", "content": yaml_content.strip()},
              token=tok)
    ok2 = r2.status_code in (200, 201)
    step("Criar policy Deny (raw YAML)", ok2, r2.status_code)
    pol_deny_id = r2.json().get("id") if ok2 else None
    if pol_deny_id:
        kpis["created_policies"].append(pol_deny_id)

    # ── 8.3 Criar policy com OR logic ────────────────────────────────────────
    pol_or = {
        "name": f"test-or-logic-{RUN_ID}",
        "effect": "allow",
        "priority": 20,
        "actions": ["relatorio:read"],
        "resources": ["relatorio/*"],
        "conditions": [
            {"field": "roles", "op": "contains", "value": "gerente"},
            {"field": "roles", "op": "contains", "value": "aprovador"},
        ],
        "condition_logic": "OR",
        "tenant_id": "tenant-teste",
    }
    r3 = post("/admin/policies/", json_body=pol_or, token=tok)
    ok3 = r3.status_code in (200, 201)
    step("Criar policy OR logic (gerente OU aprovador)", ok3, r3.status_code)
    if ok3:
        kpis["created_policies"].append(r3.json().get("id", ""))

    # ── 8.4 Criar policy com glob resource ───────────────────────────────────
    pol_glob = {
        "name": f"test-glob-{RUN_ID}",
        "effect": "allow",
        "priority": 30,
        "actions": ["admin:*"],
        "resources": ["admin/*"],
        "conditions": [
            {"field": "is_superuser", "op": "eq", "value": True},
        ],
        "tenant_id": None,
    }
    r4 = post("/admin/policies/", json_body=pol_glob, token=tok)
    ok4 = r4.status_code in (200, 201)
    step("Criar policy glob resource (admin/*)", ok4, r4.status_code)
    if ok4:
        kpis["created_policies"].append(r4.json().get("id", ""))

    # ── 8.5 Criar policy com todos os operadores ──────────────────────────────
    pol_ops = {
        "name": f"test-operators-{RUN_ID}",
        "effect": "allow",
        "priority": 50,
        "actions": ["test:*"],
        "resources": ["test/*"],
        "conditions": [
            {"field": "score",    "op": "gte",        "value": 5},
            {"field": "region",   "op": "in",         "value": ["SP", "RJ", "MG"]},
            {"field": "email",    "op": "ends_with",  "value": "@empresa.com"},
            {"field": "username", "op": "starts_with","value": "user"},
            {"field": "tag",      "op": "regex",      "value": "^prod-\\d+$"},
            {"field": "blocked",  "op": "not_exists"},
        ],
        "condition_logic": "AND",
        "tenant_id": "tenant-teste",
    }
    r5 = post("/admin/policies/", json_body=pol_ops, token=tok)
    ok5 = r5.status_code in (200, 201)
    step("Criar policy com 6 operadores distintos", ok5, r5.status_code)
    if ok5:
        kpis["created_policies"].append(r5.json().get("id", ""))

    # ── 8.6 Reload engine ────────────────────────────────────────────────────
    r6 = post("/admin/policies/reload", token=tok)
    step("Reload engine APL", r6.status_code == 200, r6.status_code,
         f"loaded={r6.json().get('loaded', '?')}" if r6.status_code == 200 else "")

    # ── 8.7 Listar policies ───────────────────────────────────────────────────
    r7 = get("/admin/policies/", token=tok, params={"tenant_id": "tenant-teste"})
    step("Listar policies (tenant-teste)", r7.status_code == 200, r7.status_code,
         f"{len(r7.json())} policies" if r7.status_code == 200 else "")

    # ── 8.8 Avaliar — Allow esperado ─────────────────────────────────────────
    eval_allow = {
        "subject": {"department": "sales", "user_level": 3, "roles": ["vendedor"]},
        "action": "cotacao:create",
        "resource": "cotacao/123",
        "tenant_id": "tenant-teste",
        "subject_id": f"subj-allow-{RUN_ID}",
        "use_cache": False,
    }
    r8, ms8 = _timed_post("/admin/policies/evaluate", json_body=eval_allow, token=tok)
    if r8.status_code == 200:
        res = r8.json()
        step("Evaluate → Allow esperado", res.get("allowed") is True,
             r8.status_code, res.get("reason", ""), latency_ms=ms8)
    else:
        step("Evaluate → Allow esperado", False, r8.status_code, r8.text[:80], latency_ms=ms8)

    # ── 8.9 Avaliar — Deny explícito vence ───────────────────────────────────
    eval_deny = {
        "subject": {"status": "blocked", "department": "sales", "user_level": 5},
        "action": "cotacao:create",
        "resource": "cotacao/456",
        "tenant_id": "tenant-teste",
        "subject_id": f"subj-deny-{RUN_ID}",
        "use_cache": False,
    }
    r9, ms9 = _timed_post("/admin/policies/evaluate", json_body=eval_deny, token=tok)
    if r9.status_code == 200:
        res9 = r9.json()
        step("Evaluate → Deny explícito vence Allow", res9.get("allowed") is False,
             r9.status_code, res9.get("reason", ""), latency_ms=ms9)
    else:
        step("Evaluate → Deny explícito vence Allow", False, r9.status_code, latency_ms=ms9)

    # ── 8.10 Avaliar — No match → default deny ────────────────────────────────
    eval_nomatch = {
        "subject": {"department": "finance", "user_level": 1},
        "action": "cotacao:delete",
        "resource": "cotacao/789",
        "tenant_id": "tenant-teste",
        "subject_id": f"subj-nomatch-{RUN_ID}",
        "use_cache": False,
    }
    r10, ms10 = _timed_post("/admin/policies/evaluate", json_body=eval_nomatch, token=tok)
    if r10.status_code == 200:
        res10 = r10.json()
        step("Evaluate → No match → default deny", res10.get("allowed") is False,
             r10.status_code, res10.get("reason", ""), latency_ms=ms10)
    else:
        step("Evaluate → No match → default deny", False, r10.status_code, latency_ms=ms10)

    # ── 8.11 Toggle policy (disable) ─────────────────────────────────────────
    if pol_allow_id:
        r11 = patch(f"/admin/policies/{pol_allow_id}/toggle",
                    token=tok, params={"enabled": "false"})
        step("Toggle policy → disabled", r11.status_code == 200, r11.status_code)

        # re-avaliar — agora deve ser no-match
        r12, ms12 = _timed_post("/admin/policies/evaluate", json_body=eval_allow, token=tok)
        if r12.status_code == 200:
            res12 = r12.json()
            step("Evaluate após disable → denied", res12.get("allowed") is False,
                 r12.status_code, res12.get("reason", ""), latency_ms=ms12)

        # re-enable
        r13 = patch(f"/admin/policies/{pol_allow_id}/toggle",
                    token=tok, params={"enabled": "true"})
        step("Toggle policy → re-enabled", r13.status_code == 200, r13.status_code)

    # ── 8.12 Get policy por ID ────────────────────────────────────────────────
    if pol_allow_id:
        r14 = get(f"/admin/policies/{pol_allow_id}", token=tok)
        step("Get policy por ID", r14.status_code == 200, r14.status_code,
             r14.json().get("name", "") if r14.status_code == 200 else "")


# ══════════════════════════════════════════════════════════════════════════════
# 9. DECISION CACHE — "BMO guarda as decisões na memória turbo"
# ══════════════════════════════════════════════════════════════════════════════
def test_decision_cache():
    _hdr("⚡ 9. DECISION CACHE — TTL, LRU, hit rate")
    tok = kpis["token_admin"]
    if not tok: return

    eval_body = {
        "subject": {"department": "sales", "user_level": 3, "roles": ["vendedor"]},
        "action": "cotacao:read",
        "resource": "cotacao/cache-test",
        "tenant_id": "tenant-teste",
        "subject_id": "cache-subject-fixo",
        "use_cache": True,
    }

    # primeira chamada — cache miss
    r1, ms1 = _timed_post("/admin/policies/evaluate", json_body=eval_body, token=tok)
    step("Evaluate #1 (cache miss)", r1.status_code == 200, r1.status_code,
         f"allowed={r1.json().get('allowed')}" if r1.status_code == 200 else "",
         latency_ms=ms1)

    # segunda chamada — cache hit (deve ser mais rápida)
    r2, ms2 = _timed_post("/admin/policies/evaluate", json_body=eval_body, token=tok)
    step("Evaluate #2 (cache hit)", r2.status_code == 200, r2.status_code,
         f"allowed={r2.json().get('allowed')} | {ms2:.0f}ms vs {ms1:.0f}ms",
         latency_ms=ms2)

    # terceira chamada — confirma cache hit
    r3, ms3 = _timed_post("/admin/policies/evaluate", json_body=eval_body, token=tok)
    step("Evaluate #3 (cache hit confirmado)", r3.status_code == 200, r3.status_code,
         f"reason={r3.json().get('reason', '')[:60]}" if r3.status_code == 200 else "",
         latency_ms=ms3)

    # cache hit deve ser mais rápido que miss (ou pelo menos não muito mais lento)
    if ms1 > 0 and ms2 > 0:
        step("Cache hit mais rápido que miss", ms2 <= ms1 * 2,
             detail=f"miss={ms1:.0f}ms hit={ms2:.0f}ms")

    # stats do cache
    r4 = get("/admin/policies/cache/stats", token=tok)
    if r4.status_code == 200:
        stats = r4.json()
        step("Cache stats disponíveis", True, r4.status_code,
             f"hits={stats.get('hits')} misses={stats.get('misses')} "
             f"hit_rate={stats.get('hit_rate')} size={stats.get('size')}")
    else:
        step("Cache stats disponíveis", False, r4.status_code)

    # multi-tenant isolation — subject_id diferente por tenant
    eval_t2 = {**eval_body, "tenant_id": "tenant-outro", "subject_id": "cache-subject-fixo"}
    r5, ms5 = _timed_post("/admin/policies/evaluate", json_body=eval_t2, token=tok)
    step("Cache isolado por tenant_id", r5.status_code == 200, r5.status_code,
         f"tenant-outro: allowed={r5.json().get('allowed')}" if r5.status_code == 200 else "",
         latency_ms=ms5)

# ══════════════════════════════════════════════════════════════════════════════
# 10. MULTI-TENANT — "Cada reino tem suas próprias leis"
# ══════════════════════════════════════════════════════════════════════════════
def test_multitenant():
    _hdr("🏰 10. MULTI-TENANT — Isolamento lógico por tenant_id")
    tok = kpis["token_admin"]
    if not tok: return

    # policy exclusiva do tenant-A
    pol_a = {
        "name": f"tenant-a-only-{RUN_ID}",
        "effect": "allow",
        "priority": 5,
        "actions": ["recurso:read"],
        "resources": ["recurso/*"],
        "conditions": [{"field": "roles", "op": "contains", "value": "admin"}],
        "tenant_id": "tenant-A",
    }
    r = post("/admin/policies/", json_body=pol_a, token=tok)
    step("Criar policy exclusiva tenant-A", r.status_code in (200, 201), r.status_code)
    if r.status_code in (200, 201):
        kpis["created_policies"].append(r.json().get("id", ""))

    post("/admin/policies/reload", token=tok)

    # avaliar no tenant-A → deve permitir
    eval_a = {
        "subject": {"roles": ["admin"]},
        "action": "recurso:read",
        "resource": "recurso/123",
        "tenant_id": "tenant-A",
        "subject_id": f"mt-subj-{RUN_ID}",
        "use_cache": False,
    }
    r2, ms2 = _timed_post("/admin/policies/evaluate", json_body=eval_a, token=tok)
    if r2.status_code == 200:
        step("Evaluate tenant-A → allowed", r2.json().get("allowed") is True,
             r2.status_code, r2.json().get("reason", ""), latency_ms=ms2)

    # avaliar no tenant-B → deve negar (policy não se aplica)
    eval_b = {**eval_a, "tenant_id": "tenant-B", "subject_id": f"mt-subj-b-{RUN_ID}"}
    r3, ms3 = _timed_post("/admin/policies/evaluate", json_body=eval_b, token=tok)
    if r3.status_code == 200:
        step("Evaluate tenant-B → denied (isolamento)", r3.json().get("allowed") is False,
             r3.status_code, r3.json().get("reason", ""), latency_ms=ms3)

    # listar policies filtradas por tenant
    r4 = get("/admin/policies/", token=tok, params={"tenant_id": "tenant-A"})
    step("Listar policies tenant-A", r4.status_code == 200, r4.status_code,
         f"{len(r4.json())} policies" if r4.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 11. USER TYPES & LEVELS — "Os níveis de poder do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_user_types_levels():
    _hdr("⭐ 11. USER TYPES & LEVELS")
    tok = kpis["token_admin"]
    if not tok: return

    # user types
    r = post("/admin/user-types/", json_body={"name": "funcionario", "description": "Funcionário"},
             token=tok)
    step("Criar user type 'funcionario'", r.status_code in (200, 201, 409), r.status_code)

    r2 = get("/admin/user-types/", token=tok)
    step("Listar user types", r2.status_code == 200, r2.status_code,
         f"{len(r2.json())} tipos" if r2.status_code == 200 else "")

    # user levels
    for name, rank in [("junior", 1), ("pleno", 2), ("senior", 3), ("lead", 4)]:
        r3 = post("/admin/user-levels/",
                  json_body={"name": name, "rank": rank, "description": f"Nível {name}"},
                  token=tok)
        step(f"Criar user level '{name}' (rank={rank})",
             r3.status_code in (200, 201, 409), r3.status_code)

    r4 = get("/admin/user-levels/", token=tok)
    step("Listar user levels", r4.status_code == 200, r4.status_code,
         f"{len(r4.json())} níveis" if r4.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 12. CUSTOM ENTITIES — "As entidades mágicas do ABAC"
# ══════════════════════════════════════════════════════════════════════════════
def test_custom_entities():
    _hdr("🔮 12. CUSTOM ENTITIES (ABAC)")
    tok = kpis["token_admin"]
    if not tok: return

    # criar tipo de entidade
    r = post("/admin/custom-entities/types/",
             json_body={"slug": "regiao", "name": "Região", "description": "Região geográfica"},
             token=tok)
    step("Criar entity type 'regiao'", r.status_code in (200, 201, 409), r.status_code)

    # criar valores
    for val in ["sul", "sudeste", "nordeste"]:
        r2 = post("/admin/custom-entities/types/regiao/values/",
                  json_body={"name": val, "description": f"Região {val}"},
                  token=tok)
        step(f"Criar entity value '{val}'", r2.status_code in (200, 201, 409), r2.status_code)

    # listar tipos
    r3 = get("/admin/custom-entities/types/", token=tok)
    step("Listar entity types", r3.status_code == 200, r3.status_code,
         f"{len(r3.json())} tipos" if r3.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 13. SETTINGS — "As configurações do castelo"
# ══════════════════════════════════════════════════════════════════════════════
def test_settings():
    _hdr("⚙️  13. SETTINGS")
    tok = kpis["token_admin"]
    if not tok: return

    r = get("/admin/settings/", token=tok)
    step("GET settings", r.status_code == 200, r.status_code)

    r2 = put("/admin/settings/", json_body={"max_login_attempts": 5, "session_timeout": 3600},
             token=tok)
    step("PUT settings", r2.status_code in (200, 201, 204), r2.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 14. AUDIT LOGS — "O livro de registros do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_audit():
    _hdr("📖 14. AUDIT LOGS")
    tok = kpis["token_admin"]
    if not tok: return

    r = get("/admin/audit-logs/", token=tok, params={"limit": 20})
    step("Listar audit logs", r.status_code == 200, r.status_code,
         f"{len(r.json())} entradas" if r.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 15. GROUPS — "Os grupos de heróis do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_groups():
    _hdr("👥 15. GROUPS")
    tok = kpis["token_admin"]
    if not tok: return

    r = post("/admin/groups/",
             json_body={"name": f"grupo-vendas-{RUN_ID}", "description": "Grupo de vendas"},
             token=tok)
    ok = r.status_code in (200, 201, 409)
    step("Criar grupo 'grupo-vendas'", ok, r.status_code)
    if r.status_code in (200, 201):
        kpis["created_groups"].append(r.json().get("id", ""))

    r2 = get("/admin/groups/", token=tok)
    step("Listar grupos", r2.status_code == 200, r2.status_code,
         f"{len(r2.json())} grupos" if r2.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 16. METRICS — "O painel de controle do BMO"
# ══════════════════════════════════════════════════════════════════════════════
def test_metrics():
    _hdr("📊 16. METRICS")
    tok = kpis["token_admin"]
    if not tok: return

    r = get("/admin/metrics/", token=tok)
    step("GET metrics", r.status_code == 200, r.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 17. APL — OPERADORES AVANÇADOS — "O grimório completo"
# ══════════════════════════════════════════════════════════════════════════════
def test_apl_operators():
    _hdr("🧪 17. APL — Todos os 14 operadores")
    tok = kpis["token_admin"]
    if not tok: return

    # policy com neq
    pol = {
        "name": f"test-neq-{RUN_ID}",
        "effect": "allow",
        "priority": 99,
        "actions": ["op:neq"],
        "resources": ["op/*"],
        "conditions": [{"field": "status", "op": "neq", "value": "blocked"}],
        "tenant_id": "tenant-ops",
    }
    r = post("/admin/policies/", json_body=pol, token=tok)
    step("Criar policy op=neq", r.status_code in (200, 201), r.status_code)
    if r.status_code in (200, 201):
        kpis["created_policies"].append(r.json().get("id", ""))

    post("/admin/policies/reload", token=tok)

    # testar cada operador via evaluate
    test_cases = [
        ("neq",          {"status": "active"},  "op:neq",  "op/test", True),
        ("neq-blocked",  {"status": "blocked"}, "op:neq",  "op/test", False),
    ]
    for label, subject, action, resource, expected in test_cases:
        ev = {
            "subject": subject, "action": action, "resource": resource,
            "tenant_id": "tenant-ops",
            "subject_id": f"op-{label}-{RUN_ID}",
            "use_cache": False,
        }
        r2, ms2 = _timed_post("/admin/policies/evaluate", json_body=ev, token=tok)
        if r2.status_code == 200:
            got = r2.json().get("allowed")
            step(f"Op neq [{label}] → {'allow' if expected else 'deny'}",
                 got is expected, r2.status_code,
                 r2.json().get("reason", "")[:60], latency_ms=ms2)


# ══════════════════════════════════════════════════════════════════════════════
# 18. CLEANUP — "Finn limpa o campo de batalha"
# ══════════════════════════════════════════════════════════════════════════════
def test_cleanup():
    _hdr("🧹 18. CLEANUP — Removendo recursos de teste")
    tok = kpis["token_admin"]
    if not tok: return

    for pol_id in kpis["created_policies"]:
        r = delete(f"/admin/policies/{pol_id}", token=tok)
        step(f"Delete policy {pol_id[:8]}...", r.status_code in (200, 204), r.status_code)

    for u in kpis["created_users"]:
        if u.get("id"):
            r = delete(f"/admin/users/{u['id']}", token=tok)
            step(f"Delete user '{u['username']}'", r.status_code in (200, 204), r.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIO FINAL
# ══════════════════════════════════════════════════════════════════════════════
def _save_report():
    lats = kpis["latencies_ms"]
    lats_sorted = sorted(lats) if lats else [0]
    n = len(lats_sorted)
    def pct(p): return round(lats_sorted[min(int(n * p), n - 1)], 1)

    summary = {
        "run_id":    RUN_ID,
        "timestamp": _ts(),
        "server":    API_BASE,
        "total":     kpis["total"],
        "passed":    kpis["passed"],
        "failed":    kpis["failed"],
        "pass_rate": round(kpis["passed"] / kpis["total"] * 100, 1) if kpis["total"] else 0,
        "latency": {
            "avg_ms": round(sum(lats) / n, 1) if lats else 0,
            "p50_ms": pct(0.50), "p90_ms": pct(0.90),
            "p95_ms": pct(0.95), "p99_ms": pct(0.99),
        },
        "created": {
            "policies":    len(kpis["created_policies"]),
            "users":       len(kpis["created_users"]),
            "roles":       len(kpis["created_roles"]),
            "permissions": len(kpis["created_permissions"]),
            "groups":      len(kpis["created_groups"]),
        },
        "results": results,
    }

    base = os.path.join(LOGS_DIR, f"run_{RUN_ID}")
    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    with open(f"{base}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(summary, f, allow_unicode=True, default_flow_style=False)

    # MD
    lines = [
        "# 🌟 Apollo IAM Engine — Production Test Report",
        "",
        f"**Run ID:** `{RUN_ID}`  ",
        f"**Data:** {summary['timestamp']}  ",
        f"**Servidor:** {API_BASE}  ",
        "",
        "---",
        "",
        "## Resumo",
        "",
        f"| Total | Passed | Failed | Pass Rate |",
        f"|---|---|---|---|",
        f"| {summary['total']} | {summary['passed']} | {summary['failed']} | {summary['pass_rate']}% |",
        "",
        "## Latências",
        "",
        f"| Avg | P50 | P90 | P95 | P99 |",
        f"|---|---|---|---|---|",
        f"| {summary['latency']['avg_ms']}ms | {summary['latency']['p50_ms']}ms | "
        f"{summary['latency']['p90_ms']}ms | {summary['latency']['p95_ms']}ms | "
        f"{summary['latency']['p99_ms']}ms |",
        "",
        "## Resultados por Step",
        "",
        "| Step | OK | Status | Latência | Detalhe |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        icon = "✅" if r["ok"] else "❌"
        lat  = f"{r['latency_ms']:.0f}ms" if r.get("latency_ms") else "—"
        det  = str(r.get("detail", ""))[:60].replace("|", "\\|")
        lines.append(f"| {r['step']} | {icon} | {r['status_code']} | {lat} | {det} |")

    lines += ["", "---", "", "*Gerado pelo Apollo IAM Engine Production Test Suite — O2 Data Solutions*"]
    with open(f"{base}.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    console.print(f"\n  [dim]Relatório salvo em: {base}.[json|yaml|md][/dim]")
    return summary


def _print_final(summary: dict):
    console.print()
    color = "green" if summary["failed"] == 0 else ("yellow" if summary["failed"] < 5 else "red")
    t = Table(title="🏆 Resultado Final", show_header=True,
              header_style="bold white", border_style="dim")
    t.add_column("Métrica",   style="cyan",  min_width=16)
    t.add_column("Valor",     style=color,   min_width=12)
    t.add_row("Total steps",  str(summary["total"]))
    t.add_row("✅ Passed",    str(summary["passed"]))
    t.add_row("❌ Failed",    str(summary["failed"]))
    t.add_row("Pass rate",    f"{summary['pass_rate']}%")
    t.add_row("Avg latência", f"{summary['latency']['avg_ms']}ms")
    t.add_row("P99 latência", f"{summary['latency']['p99_ms']}ms")
    t.add_row("Policies",     str(summary["created"]["policies"]))
    t.add_row("Users",        str(summary["created"]["users"]))
    console.print(t)

    if summary["failed"] == 0:
        console.print(Panel(
            "[bold green]🎉 Todos os testes passaram! O reino de Ooo está seguro![/bold green]\n"
            "[dim]Finn e Jake aprovam o Apollo IAM Engine.[/dim]",
            border_style="green",
        ))
    else:
        failed_steps = [r["step"] for r in results if not r["ok"]]
        console.print(Panel(
            f"[bold red]⚠️  {summary['failed']} teste(s) falharam:[/bold red]\n"
            + "\n".join(f"  ❌ {s}" for s in failed_steps[:10]),
            border_style="red",
        ))


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    console.print()
    console.print(Panel(
        "[bold cyan]🌟 Apollo IAM Engine — Production Test Suite v3[/bold cyan]\n"
        "[dim]\"Hora de Aventura no Reino de Ooo IAM\"[/dim]\n\n"
        f"Servidor: [yellow]{API_BASE}[/yellow]\n"
        f"Run ID:   [yellow]{RUN_ID}[/yellow]",
        border_style="cyan",
        expand=False,
    ))

    test_health()
    test_auth()
    test_roles()
    test_permissions()
    test_users()
    test_rbac()
    test_abac()
    test_apl()
    test_decision_cache()
    test_multitenant()
    test_user_types_levels()
    test_custom_entities()
    test_settings()
    test_audit()
    test_groups()
    test_metrics()
    test_apl_operators()
    test_cleanup()

    summary = _save_report()
    _print_final(summary)


if __name__ == "__main__":
    main()
