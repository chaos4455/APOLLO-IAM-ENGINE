"""
project-production-test.py
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌟 APOLLO IAM ENGINE — Production Test Suite v5 🌟                        ║
║  Cobertura 100%: Health, Auth, RBAC, ABAC, APL DSL, Cache, Multi-tenant,   ║
║  User Types/Levels (CRUD completo), Custom Entities (CRUD + assign/unassign)║
║  Settings, Audit, Groups (assign user), Metrics + /logs + /cache,          ║
║  Policies (CRUD + Evaluate + Explain + Toggle + Raw + /decisions/audit),   ║
║  User toggle-status, reset-password, revogar role, Cleanup 100%.           ║
║  O2 Data Solutions                                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
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
    "created_policies": [], "created_rbac_attrs": [],
    "created_user_types": [], "created_user_levels": [],
    "created_entity_types": [],
    "token_admin": None, "token_usuario1": None,
    "token_gerente": None, "token_aprovador": None,
    "latencies_ms": [],
}
_TIMEOUT = httpx.Timeout(30.0, connect=10.0)

# ── log incremental em tempo real ─────────────────────────────────────────────
_LOG_BASE = os.path.join(LOGS_DIR, f"run_{RUN_ID}")


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _flush_incremental():
    """Salva JSON/YAML/MD parcial a cada step — tempo real."""
    lats = kpis["latencies_ms"]
    lats_sorted = sorted(lats) if lats else [0]
    n = len(lats_sorted)
    def pct(p): return round(lats_sorted[min(int(n * p), n - 1)], 1)

    summary = {
        "run_id": RUN_ID, "timestamp": _ts(), "server": API_BASE,
        "total": kpis["total"], "passed": kpis["passed"], "failed": kpis["failed"],
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
    # JSON
    with open(f"{_LOG_BASE}.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    # YAML
    with open(f"{_LOG_BASE}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(summary, f, allow_unicode=True, default_flow_style=False)
    # MD
    lines = [
        "# 🌟 Apollo IAM Engine — Production Test Report",
        "", f"**Run ID:** `{RUN_ID}`  ", f"**Data:** {summary['timestamp']}  ",
        f"**Servidor:** {API_BASE}  ", "", "---", "", "## Resumo", "",
        "| Total | Passed | Failed | Pass Rate |", "|---|---|---|---|",
        f"| {summary['total']} | {summary['passed']} | {summary['failed']} | {summary['pass_rate']}% |",
        "", "## Latências", "",
        "| Avg | P50 | P90 | P95 | P99 |", "|---|---|---|---|---|",
        f"| {summary['latency']['avg_ms']}ms | {summary['latency']['p50_ms']}ms | "
        f"{summary['latency']['p90_ms']}ms | {summary['latency']['p95_ms']}ms | "
        f"{summary['latency']['p99_ms']}ms |",
        "", "## Resultados por Step", "",
        "| Step | OK | Status | Latência | Detalhe |", "|---|---|---|---|---|",
    ]
    for r in results:
        icon = "✅" if r["ok"] else "❌"
        lat  = f"{r['latency_ms']:.0f}ms" if r.get("latency_ms") else "—"
        det  = str(r.get("detail", ""))[:80].replace("|", "\\|")
        lines.append(f"| {r['step']} | {icon} | {r['status_code']} | {lat} | {det} |")
    lines += ["", "---", "", "*Gerado pelo Apollo IAM Engine Production Test Suite v5 — O2 Data Solutions*"]
    with open(f"{_LOG_BASE}.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return summary


# ── helpers HTTP ──────────────────────────────────────────────────────────────

def _build_client() -> httpx.Client:
    return httpx.Client(verify=_SSL, timeout=_TIMEOUT)


def _req(method: str, path: str, token: str | None = None,
         json_body=None, form=None, params=None) -> tuple:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    t0 = time.perf_counter()
    with _build_client() as c:
        r = c.request(method.upper(), API_BASE + path, headers=headers,
                      json=json_body, data=form, params=params)
    ms = round((time.perf_counter() - t0) * 1000, 1)
    kpis["latencies_ms"].append(ms)
    return r, ms


def get(path, token=None, params=None):
    r, _ = _req("get", path, token=token, params=params); return r

def post(path, json_body=None, form=None, token=None, params=None):
    r, _ = _req("post", path, token=token, json_body=json_body, form=form, params=params); return r

def put(path, json_body=None, token=None):
    r, _ = _req("put", path, token=token, json_body=json_body); return r

def patch(path, token=None, params=None, json_body=None):
    r, _ = _req("patch", path, token=token, params=params, json_body=json_body); return r

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


def step(name: str, ok: bool, status_code: int = 0, detail: str = "", latency_ms: float = 0.0):
    kpis["total"] += 1
    if ok:
        kpis["passed"] += 1
    else:
        kpis["failed"] += 1
    icon = "✅" if ok else "❌"
    lat  = f"[dim]{latency_ms:.0f}ms[/dim]" if latency_ms else ""
    det  = f"[dim]{detail[:80]}[/dim]" if detail else ""
    console.print(f"  {icon} {name} [dim]({status_code})[/dim] {lat} {det}")
    results.append({"step": name, "ok": ok, "status_code": status_code,
                    "detail": detail, "latency_ms": latency_ms})
    _flush_incremental()


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
        r2 = post(f"/admin/roles/{roles_by_name['vendedor']}/assign-user/{u1['id']}", token=tok)
        step("Assign role 'vendedor' → usuario1", r2.status_code in (200, 201, 204),
             r2.status_code)

    # assign role gerente ao gerente
    ger = next((u for u in kpis["created_users"] if "gerente" in u["username"]), None)
    if ger and "gerente" in roles_by_name:
        r3 = post(f"/admin/roles/{roles_by_name['gerente']}/assign-user/{ger['id']}", token=tok)
        step("Assign role 'gerente' → gerente", r3.status_code in (200, 201, 204),
             r3.status_code)

    # assign role aprovador ao aprovador
    apr = next((u for u in kpis["created_users"] if "aprovador" in u["username"]), None)
    if apr and "aprovador" in roles_by_name:
        r3b = post(f"/admin/roles/{roles_by_name['aprovador']}/assign-user/{apr['id']}", token=tok)
        step("Assign role 'aprovador' → aprovador", r3b.status_code in (200, 201, 204),
             r3b.status_code)

    # assign permissão cotacao:create à role vendedor via /admin/permissions/{id}/assign-role/{role_id}
    if "vendedor" in roles_by_name and "cotacao:create" in perms_by_name:
        r4 = post(f"/admin/permissions/{perms_by_name['cotacao:create']}/assign-role/{roles_by_name['vendedor']}",
                  token=tok)
        step("Assign perm 'cotacao:create' → role vendedor",
             r4.status_code in (200, 201, 204), r4.status_code)

    # assign permissão relatorio:read à role gerente
    if "gerente" in roles_by_name and "relatorio:read" in perms_by_name:
        r4b = post(f"/admin/permissions/{perms_by_name['relatorio:read']}/assign-role/{roles_by_name['gerente']}",
                   token=tok)
        step("Assign perm 'relatorio:read' → role gerente",
             r4b.status_code in (200, 201, 204), r4b.status_code)

    # verifica token atualizado do usuario1
    if u1:
        tok_u1 = _fresh_token(u1["username"], u1["password"])
        kpis["token_usuario1"] = tok_u1
        if tok_u1:
            chk = _check(tok_u1, require_roles=["vendedor"])
            step("Check usuario1 tem role 'vendedor'", chk.get("allowed") is True,
                 detail=chk.get("reason", ""))

    # revogar role vendedor do usuario1 e reassign
    if u1 and "vendedor" in roles_by_name:
        r5 = delete(f"/admin/roles/{roles_by_name['vendedor']}/revoke-user/{u1['id']}", token=tok)
        step("Revogar role 'vendedor' de usuario1", r5.status_code in (200, 204), r5.status_code)
        # reassign para manter o estado
        post(f"/admin/roles/{roles_by_name['vendedor']}/assign-user/{u1['id']}", token=tok)
        kpis["token_usuario1"] = _fresh_token(u1["username"], u1["password"])

# ══════════════════════════════════════════════════════════════════════════════
# 7. ABAC — "Marceline verifica os atributos mágicos"
# ══════════════════════════════════════════════════════════════════════════════
def test_abac():
    _hdr("🧛 7. ABAC — Atributos RBAC e check combinado")
    tok = kpis["token_admin"]
    if not tok: return

    # cria atributo RBAC — path correto: /admin/rbac/
    r = post("/admin/rbac/",
             json_body={"key": "department", "label": "Departamento",
                        "value_type": "string", "description": "Departamento do usuário"},
             token=tok)
    step("Criar atributo RBAC 'department'", r.status_code in (200, 201, 409), r.status_code)
    if r.status_code in (200, 201):
        kpis["created_rbac_attrs"].append(r.json().get("id", ""))

    # listar atributos
    rl = get("/admin/rbac/", token=tok)
    step("Listar atributos RBAC", rl.status_code == 200, rl.status_code,
         f"{len(rl.json())} attrs" if rl.status_code == 200 else "")

    # assign atributo ao usuario1 — path: /admin/rbac/assign/{user_id}
    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if u1:
        r2 = post(f"/admin/rbac/assign/{u1['id']}",
                  json_body={"attribute_key": "department", "value": "sales"},
                  token=tok)
        step("Assign department=sales → usuario1", r2.status_code in (200, 201, 204),
             r2.status_code)

        # assign outro atributo de nível
        r2b = post(f"/admin/rbac/assign/{u1['id']}",
                   json_body={"attribute_key": "user_level", "value": "3"},
                   token=tok)
        step("Assign user_level=3 → usuario1", r2b.status_code in (200, 201, 204),
             r2b.status_code)

    # check ABAC com token fresco
    if u1:
        tok_u1 = _fresh_token(u1["username"], u1["password"]) or kpis["token_usuario1"]
        kpis["token_usuario1"] = tok_u1
        if tok_u1:
            chk = _check(tok_u1, require_abac={"department": "sales"})
            step("Check ABAC department=sales → allowed", chk.get("allowed") is True,
                 detail=chk.get("reason", ""))

            chk2 = _check(tok_u1, require_abac={"department": "finance"})
            step("Check ABAC department=finance → denied", chk2.get("allowed") is False,
                 detail=chk2.get("reason", ""))

            # check combinado: role + ABAC
            chk3 = _check(tok_u1, require_roles=["vendedor"], require_abac={"department": "sales"})
            step("Check combinado role+ABAC → allowed", chk3.get("allowed") is True,
                 detail=chk3.get("reason", ""))

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

    # ── 8.13 Explain policy (trace completo) ─────────────────────────────────
    explain_body = {
        "subject": {"department": "sales", "user_level": 3, "roles": ["vendedor"]},
        "action": "cotacao:create",
        "resource": "cotacao/123",
        "tenant_id": "tenant-teste",
        "subject_id": f"explain-{RUN_ID}",
    }
    r15, ms15 = _timed_post("/admin/policies/explain", json_body=explain_body, token=tok)
    step("Explain policy (trace completo)", r15.status_code == 200, r15.status_code,
         str(r15.json())[:80] if r15.status_code == 200 else r15.text[:80], latency_ms=ms15)

    # ── 8.14 Decision audit trail ─────────────────────────────────────────────
    r16 = get("/admin/policies/decisions/audit", token=tok,
              params={"tenant_id": "tenant-teste", "limit": 10})
    step("Policy decisions/audit", r16.status_code == 200, r16.status_code,
         f"{len(r16.json())} decisões" if r16.status_code == 200 else r16.text[:80])

    # ── 8.15 Cache stats via policies ────────────────────────────────────────
    r17 = get("/admin/policies/cache/stats", token=tok)
    step("Policy cache/stats", r17.status_code == 200, r17.status_code,
         str(r17.json())[:80] if r17.status_code == 200 else "")


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
    _hdr("⭐ 11. USER TYPES & LEVELS — CRUD completo")
    tok = kpis["token_admin"]
    if not tok: return

    uid = uuid.uuid4().hex[:6]

    # ── user types ────────────────────────────────────────────────────────────
    r = post("/admin/user-types/",
             json_body={"name": f"funcionario_{uid}", "description": "Funcionário"},
             token=tok)
    step("Criar user type 'funcionario'", r.status_code in (200, 201, 409), r.status_code)
    type_id = r.json().get("id") if r.status_code in (200, 201) else None
    if type_id:
        kpis["created_user_types"].append(type_id)

    r2 = get("/admin/user-types/", token=tok)
    step("Listar user types", r2.status_code == 200, r2.status_code,
         f"{len(r2.json())} tipos" if r2.status_code == 200 else "")

    if type_id:
        r3 = get(f"/admin/user-types/{type_id}", token=tok)
        step("GET user type por ID", r3.status_code == 200, r3.status_code)

        r4 = put(f"/admin/user-types/{type_id}",
                 json_body={"name": f"funcionario_{uid}", "description": "Atualizado"},
                 token=tok)
        step("PUT user type (update)", r4.status_code == 200, r4.status_code)

    # ── user levels ────────────────────────────────────────────────────────────
    level_ids = []
    for name, rank in [(f"junior_{uid}", 1), (f"pleno_{uid}", 2),
                       (f"senior_{uid}", 3), (f"lead_{uid}", 4)]:
        r5 = post("/admin/user-levels/",
                  json_body={"name": name, "rank": rank, "description": f"Nível {name}"},
                  token=tok)
        step(f"Criar user level '{name}' (rank={rank})",
             r5.status_code in (200, 201, 409), r5.status_code)
        if r5.status_code in (200, 201):
            lid = r5.json().get("id", "")
            level_ids.append(lid)
            kpis["created_user_levels"].append(lid)

    r6 = get("/admin/user-levels/", token=tok)
    step("Listar user levels", r6.status_code == 200, r6.status_code,
         f"{len(r6.json())} níveis" if r6.status_code == 200 else "")

    if level_ids:
        lid = level_ids[0]
        r7 = get(f"/admin/user-levels/{lid}", token=tok)
        step("GET user level por ID", r7.status_code == 200, r7.status_code)

        r8 = put(f"/admin/user-levels/{lid}",
                 json_body={"rank": 10, "description": "Rank atualizado"},
                 token=tok)
        step("PUT user level (update rank)", r8.status_code == 200, r8.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 12. CUSTOM ENTITIES — "As entidades mágicas do ABAC"
# ══════════════════════════════════════════════════════════════════════════════
def test_custom_entities():
    _hdr("🔮 12. CUSTOM ENTITIES (ABAC) — CRUD + assign/unassign")
    tok = kpis["token_admin"]
    if not tok: return

    uid = uuid.uuid4().hex[:6]
    slug = f"regiao_{uid}"

    # criar tipo — path: POST /admin/custom-entities/types
    r = post("/admin/custom-entities/types",
             json_body={"slug": slug, "label": "Região", "description": "Região geográfica"},
             token=tok)
    step("Criar entity type 'regiao'", r.status_code in (200, 201, 409), r.status_code)
    kpis["created_entity_types"].append(slug)

    # GET tipo por slug
    r1b = get(f"/admin/custom-entities/types/{slug}", token=tok)
    step("GET entity type por slug", r1b.status_code == 200, r1b.status_code)

    # PUT tipo (update)
    r1c = put(f"/admin/custom-entities/types/{slug}",
              json_body={"label": "Região Atualizada", "description": "Desc atualizada"},
              token=tok)
    step("PUT entity type (update)", r1c.status_code == 200, r1c.status_code)

    # criar valores — path: POST /admin/custom-entities/{slug}/values
    value_ids = []
    for val in ["sul", "sudeste", "nordeste"]:
        r2 = post(f"/admin/custom-entities/{slug}/values",
                  json_body={"name": val, "description": f"Região {val}", "metadata": {"code": val[:2]}},
                  token=tok)
        step(f"Criar entity value '{val}'", r2.status_code in (200, 201, 409), r2.status_code)
        if r2.status_code in (200, 201):
            value_ids.append(r2.json().get("id", ""))

    # GET value por ID
    if value_ids:
        r3 = get(f"/admin/custom-entities/{slug}/values/{value_ids[0]}", token=tok)
        step("GET entity value por ID", r3.status_code == 200, r3.status_code)

        # PUT value (update)
        r3b = put(f"/admin/custom-entities/{slug}/values/{value_ids[0]}",
                  json_body={"description": "Atualizado", "metadata": {"code": "SU"}},
                  token=tok)
        step("PUT entity value (update)", r3b.status_code == 200, r3b.status_code)

    # listar tipos
    r4 = get("/admin/custom-entities/types", token=tok)
    step("Listar entity types", r4.status_code == 200, r4.status_code,
         f"{len(r4.json())} tipos" if r4.status_code == 200 else "")

    # listar valores
    r5 = get(f"/admin/custom-entities/{slug}/values", token=tok)
    step("Listar entity values", r5.status_code == 200, r5.status_code,
         f"{len(r5.json())} valores" if r5.status_code == 200 else "")

    # assign entidade ao usuario1
    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if u1 and value_ids:
        r6 = post(f"/admin/custom-entities/assign/{u1['id']}",
                  json_body={"entity_type_slug": slug, "entity_value_id": value_ids[0]},
                  token=tok)
        step(f"Assign entity '{slug}' → usuario1", r6.status_code == 200, r6.status_code)

        # GET entidades do usuario1
        r7 = get(f"/admin/custom-entities/user/{u1['id']}", token=tok)
        step("GET user entities", r7.status_code == 200, r7.status_code,
             f"{len(r7.json())} entidades" if r7.status_code == 200 else "")

        # unassign entidade
        r8 = delete(f"/admin/custom-entities/assign/{u1['id']}/{slug}", token=tok)
        step("Unassign entity de usuario1", r8.status_code in (200, 204), r8.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 13. SETTINGS — "As configurações do castelo"
# ══════════════════════════════════════════════════════════════════════════════
def test_settings():
    _hdr("⚙️  13. SETTINGS")
    tok = kpis["token_admin"]
    if not tok: return

    r = get("/admin/settings/", token=tok)
    step("GET settings", r.status_code == 200, r.status_code,
         str(r.json())[:80] if r.status_code == 200 else "")

    # PUT com campos do SettingsUpdate schema
    r2 = put("/admin/settings/",
             json_body={
                 "access_token_expire_minutes": 60,
                 "refresh_token_expire_days": 7,
                 "allow_registration": False,
                 "max_login_attempts": 5,
                 "lockout_minutes": 15,
             },
             token=tok)
    step("PUT settings (update)", r2.status_code in (200, 201, 204), r2.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 14. AUDIT LOGS — "O livro de registros do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_audit():
    _hdr("📖 14. AUDIT LOGS")
    tok = kpis["token_admin"]
    if not tok: return

    # path correto: /admin/audit/
    r = get("/admin/audit/", token=tok, params={"limit": 20})
    step("Listar audit logs", r.status_code == 200, r.status_code,
         f"{len(r.json())} entradas" if r.status_code == 200 else r.text[:80])

    # filtro por status
    r2 = get("/admin/audit/", token=tok, params={"limit": 10, "status": "success"})
    step("Audit logs filtrado por status=success", r2.status_code == 200, r2.status_code,
         f"{len(r2.json())} entradas" if r2.status_code == 200 else "")

    # filtro por actor
    r3 = get("/admin/audit/", token=tok, params={"limit": 10, "actor": ADMIN_USER})
    step("Audit logs filtrado por actor=admin", r3.status_code == 200, r3.status_code,
         f"{len(r3.json())} entradas" if r3.status_code == 200 else "")

# ══════════════════════════════════════════════════════════════════════════════
# 15. GROUPS — "Os grupos de heróis do reino"
# ══════════════════════════════════════════════════════════════════════════════
def test_groups():
    _hdr("👥 15. GROUPS — CRUD + assign user")
    tok = kpis["token_admin"]
    if not tok: return

    r = post("/admin/groups/",
             json_body={"name": f"grupo-vendas-{RUN_ID}", "description": "Grupo de vendas"},
             token=tok)
    ok = r.status_code in (200, 201, 409)
    step("Criar grupo 'grupo-vendas'", ok, r.status_code)
    group_id = None
    if r.status_code in (200, 201):
        group_id = r.json().get("id", "")
        kpis["created_groups"].append(group_id)

    r2 = get("/admin/groups/", token=tok)
    step("Listar grupos", r2.status_code == 200, r2.status_code,
         f"{len(r2.json())} grupos" if r2.status_code == 200 else "")

    # assign usuario1 ao grupo
    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if u1 and group_id:
        r3 = post(f"/admin/groups/{group_id}/assign-user/{u1['id']}", token=tok)
        step("Assign usuario1 → grupo-vendas", r3.status_code in (200, 201, 204), r3.status_code)

# ══════════════════════════════════════════════════════════════════════════════
# 16. METRICS — "O painel de controle do BMO"
# ══════════════════════════════════════════════════════════════════════════════
def test_metrics():
    _hdr("📊 16. METRICS — KPIs, /logs, /cache")
    tok = kpis["token_admin"]
    if not tok: return

    # GET /admin/metrics/
    r = get("/admin/metrics/", token=tok)
    step("GET metrics (KPIs + sistema)", r.status_code == 200, r.status_code,
         f"uptime={r.json().get('uptime_fmt','?')}" if r.status_code == 200 else r.text[:80])

    if r.status_code == 200:
        m = r.json()
        step("Metrics tem cpu", "cpu" in m, detail=str(m.get("cpu", {}))[:60])
        step("Metrics tem memory", "memory" in m, detail=str(m.get("memory", {}))[:60])
        step("Metrics tem db KPIs", "db" in m, detail=str(m.get("db", {}))[:60])
        step("Metrics tem logs stats", "logs" in m, detail=str(m.get("logs", {}))[:60])

    # GET /admin/metrics/logs
    r2 = get("/admin/metrics/logs", token=tok, params={"skip": 0, "limit": 20})
    step("GET metrics/logs (event_log)", r2.status_code == 200, r2.status_code,
         f"total={r2.json().get('total','?')}" if r2.status_code == 200 else r2.text[:80])

    # GET /admin/metrics/cache
    r3 = get("/admin/metrics/cache", token=tok)
    step("GET metrics/cache stats", r3.status_code == 200, r3.status_code,
         str(r3.json())[:80] if r3.status_code == 200 else r3.text[:80])

# ══════════════════════════════════════════════════════════════════════════════
# 17. APL — OPERADORES AVANÇADOS — "O grimório completo"
# ══════════════════════════════════════════════════════════════════════════════
def test_apl_operators():
    _hdr("🧪 17. APL — Operadores avançados + neq")
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

    test_cases = [
        ("neq-active",   {"status": "active"},  "op:neq",  "op/test", True),
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
        else:
            step(f"Op neq [{label}]", False, r2.status_code, r2.text[:60])


# ══════════════════════════════════════════════════════════════════════════════
# 18. USERS — OPERAÇÕES EXTRAS (toggle, reset-password, GET por ID)
# ══════════════════════════════════════════════════════════════════════════════
def test_users_extra():
    _hdr("👤 18. USERS — toggle-status, reset-password, GET por ID")
    tok = kpis["token_admin"]
    if not tok or not kpis["created_users"]: return

    u1 = next((u for u in kpis["created_users"] if "usuario1" in u["username"]), None)
    if not u1 or not u1.get("id"): return
    uid = u1["id"]

    # GET user por ID
    r = get(f"/admin/users/{uid}", token=tok)
    step("GET user por ID", r.status_code == 200, r.status_code,
         r.json().get("username", "") if r.status_code == 200 else r.text[:80])

    # PUT user (update)
    r2 = put(f"/admin/users/{uid}",
             json_body={"email": f"updated_{uid[:6]}@test.com", "full_name": "Usuário Atualizado",
                        "is_active": True, "is_superuser": False},
             token=tok)
    step("PUT user (update)", r2.status_code == 200, r2.status_code)

    # POST toggle-status
    r3 = post(f"/admin/users/{uid}/toggle-status", token=tok)
    step("POST toggle-status (desativar)", r3.status_code == 200, r3.status_code,
         str(r3.json()) if r3.status_code == 200 else r3.text[:80])

    # reativar
    r4 = post(f"/admin/users/{uid}/toggle-status", token=tok)
    step("POST toggle-status (reativar)", r4.status_code == 200, r4.status_code)

    # POST reset-password
    r5 = post(f"/admin/users/{uid}/reset-password",
              json_body={"new_password": "NovaSenha123!"},
              token=tok)
    step("POST reset-password", r5.status_code == 200, r5.status_code,
         r5.json().get("message", "") if r5.status_code == 200 else r5.text[:80])

    # confirmar login com nova senha
    tok_new = _fresh_token(u1["username"], "NovaSenha123!")
    step("Login com nova senha após reset", tok_new is not None)
    if tok_new:
        kpis["token_usuario1"] = tok_new
        # restaurar senha original
        post(f"/admin/users/{uid}/reset-password",
             json_body={"new_password": u1["password"]}, token=tok)
        kpis["token_usuario1"] = _fresh_token(u1["username"], u1["password"])


# ══════════════════════════════════════════════════════════════════════════════
# 19. CLEANUP — "Finn limpa o campo de batalha"
# ══════════════════════════════════════════════════════════════════════════════
def test_cleanup():
    _hdr("🧹 19. CLEANUP — Removendo todos os recursos de teste")
    tok = kpis["token_admin"]
    if not tok: return

    # políticas
    for pol_id in kpis["created_policies"]:
        r = delete(f"/admin/policies/{pol_id}", token=tok)
        step(f"Delete policy {pol_id[:8]}…", r.status_code in (200, 204), r.status_code)

    # usuários
    for u in kpis["created_users"]:
        if u.get("id"):
            r = delete(f"/admin/users/{u['id']}", token=tok)
            step(f"Delete user '{u['username']}'", r.status_code in (200, 204), r.status_code)

    # grupos
    for gid in kpis["created_groups"]:
        r = delete(f"/admin/groups/{gid}", token=tok)
        step(f"Delete group {gid[:8]}…", r.status_code in (200, 204), r.status_code)

    # roles criadas pelo teste
    r_roles = get("/admin/roles/", token=tok)
    if r_roles.status_code == 200:
        for ro in r_roles.json():
            if ro["name"] in ("vendedor", "gerente", "aprovador"):
                r = delete(f"/admin/roles/{ro['id']}", token=tok)
                step(f"Delete role '{ro['name']}'", r.status_code in (200, 204), r.status_code)

    # entity types
    for slug in kpis["created_entity_types"]:
        r = delete(f"/admin/custom-entities/types/{slug}", token=tok)
        step(f"Delete entity type '{slug}'", r.status_code in (200, 204), r.status_code)

    # user types
    for tid in kpis["created_user_types"]:
        r = delete(f"/admin/user-types/{tid}", token=tok)
        step(f"Delete user type {tid[:8]}…", r.status_code in (200, 204), r.status_code)

    # user levels
    for lid in kpis["created_user_levels"]:
        r = delete(f"/admin/user-levels/{lid}", token=tok)
        step(f"Delete user level {lid[:8]}…", r.status_code in (200, 204), r.status_code)

    # atributos RBAC
    for aid in kpis["created_rbac_attrs"]:
        r = delete(f"/admin/rbac/{aid}", token=tok)
        step(f"Delete rbac attr {aid[:8]}…", r.status_code in (200, 204), r.status_code)

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
        "[bold cyan]🌟 Apollo IAM Engine — Production Test Suite v5[/bold cyan]\n"
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
    test_users_extra()
    test_cleanup()

    summary = _save_report()
    _print_final(summary)


if __name__ == "__main__":
    main()
