"""
benchmark-stress.py
╔══════════════════════════════════════════════════════════════════════════════╗
║   🌟 APOLLO IAM ENGINE — STRESS & BENCHMARK TEST SUITE 🌟                  ║
║   Hora de Aventura com Finn e Jake no Reino de Ooo IAM                      ║
║   "Matemática!" — BMO                                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Suite completa de stress test com rampa 1→5→10→25→50→100→200→500 req
simultâneos para login, validate, check, APL evaluate e cenário misto.
Detecta breaking point automaticamente (erro > 50%).
Exibe métricas em tempo real: P50/P90/P95/P99, RPS, taxa de erro.
Salva relatório em JSON, YAML e MD em benchmark-stress-logs/.

O2 Data Solutions
"""
from __future__ import annotations

import asyncio
import json
import os
import ssl
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
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

# ── resolve raiz e importa config ────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from src.infrastructure.config.security_config import (
    get_api_port,
    get_certs_dir,
    is_mtls_enabled,
)

_MTLS  = is_mtls_enabled()
_PORT  = get_api_port() if _MTLS else 8000
_PROTO = "https" if _MTLS else "http"
BASE   = f"{_PROTO}://localhost:{_PORT}"

LOGS_DIR = os.path.join(_HERE, "benchmark-stress-logs")
RUN_ID   = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(LOGS_DIR, exist_ok=True)

ADMIN_USER = "admin"
ADMIN_PASS = "admin"

# Rampa de concorrência conforme spec
RAMP_LEVELS = [1, 5, 10, 25, 50, 100, 200, 500]
BREAK_THRESHOLD = 50.0   # % de erro para declarar breaking point


# ── SSL ───────────────────────────────────────────────────────────────────────
def _ssl_ctx() -> ssl.SSLContext | bool:
    if not _MTLS:
        return False
    certs = get_certs_dir()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(cafile=str(certs / "ca" / "ca.crt"))
    ctx.load_cert_chain(
        certfile=str(certs / "client" / "client.crt"),
        keyfile=str(certs / "client" / "client.key"),
    )
    ctx.check_hostname = False
    return ctx

_SSL = _ssl_ctx()

# ── resultado de uma requisição ───────────────────────────────────────────────
class ReqResult:
    __slots__ = ("ok", "status", "latency_ms", "error")
    def __init__(self, ok: bool, status: int, latency_ms: float, error: str = ""):
        self.ok         = ok
        self.status     = status
        self.latency_ms = latency_ms
        self.error      = error

# ── estado global do benchmark ────────────────────────────────────────────────
_admin_token: str = ""
_test_user   = f"stress_{uuid.uuid4().hex[:6]}"
_test_pass   = "StressPass123!"
_test_token: str = ""
_apl_policy_id: str = ""   # policy criada para stress APL

# ── helpers de display ────────────────────────────────────────────────────────
def _hdr(title: str):
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]"))

def _ok(msg: str):
    console.print(f"  {Fore.GREEN}✔{Style.RESET_ALL}  {msg}")

def _err(msg: str):
    console.print(f"  {Fore.RED}✘{Style.RESET_ALL}  {msg}")

def _info(msg: str):
    console.print(f"  {Fore.CYAN}ℹ{Style.RESET_ALL}  {msg}")

def _warn(msg: str):
    console.print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL}  {msg}")

# ── cliente HTTP assíncrono ───────────────────────────────────────────────────
def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=BASE,
        verify=_SSL,
        timeout=httpx.Timeout(30.0, connect=5.0),
    )


# ── setup: login admin + criar usuário de teste + policy APL ──────────────────
async def setup():
    global _admin_token, _test_token, _apl_policy_id
    _hdr("🏰 SETUP — Finn prepara o campo de batalha")
    async with _client() as c:
        # login admin
        r = await c.post("/auth/token", data={"username": ADMIN_USER, "password": ADMIN_PASS})
        if r.status_code != 200:
            _err(f"Login admin falhou: {r.status_code} {r.text}")
            sys.exit(1)
        _admin_token = r.json()["access_token"]
        _ok(f"Admin logado. Token: {_admin_token[:20]}...")

        # cria usuário de teste
        payload = {
            "username": _test_user,
            "password": _test_pass,
            "email": f"{_test_user}@stress.test",
            "full_name": "Stress Test User",
            "is_active": True,
        }
        r2 = await c.post(
            "/admin/users/",
            json=payload,
            headers={"Authorization": f"Bearer {_admin_token}"},
        )
        if r2.status_code in (200, 201):
            _ok(f"Usuário de teste criado: {_test_user}")
        elif r2.status_code == 409:
            _warn(f"Usuário {_test_user} já existe — reutilizando.")
        else:
            _err(f"Falha ao criar usuário: {r2.status_code} {r2.text}")

        # login do usuário de teste
        r3 = await c.post("/auth/token", data={"username": _test_user, "password": _test_pass})
        if r3.status_code == 200:
            _test_token = r3.json()["access_token"]
            _ok(f"Usuário de teste logado. Token: {_test_token[:20]}...")
        else:
            _err(f"Login usuário de teste falhou: {r3.status_code}")

        # cria policy APL para stress de evaluate
        pol_payload = {
            "name": f"stress-policy-{RUN_ID}",
            "description": "Policy criada pelo stress test — pode remover",
            "effect": "allow",
            "priority": 50,
            "actions": ["stress:*", "cotacao:*"],
            "resources": ["stress/*", "cotacao/*"],
            "conditions": [
                {"field": "department", "op": "eq", "value": "stress"},
            ],
            "condition_logic": "AND",
            "tenant_id": "tenant-stress",
            "enabled": True,
        }
        r4 = await c.post(
            "/admin/policies/",
            json=pol_payload,
            headers={"Authorization": f"Bearer {_admin_token}"},
        )
        if r4.status_code in (200, 201):
            _apl_policy_id = r4.json().get("id", "")
            _ok(f"Policy APL criada: {_apl_policy_id}")
        else:
            _warn(f"Falha ao criar policy APL: {r4.status_code} {r4.text[:80]}")

        # reload engine
        await c.post(
            "/admin/policies/reload",
            headers={"Authorization": f"Bearer {_admin_token}"},
        )
        _ok("Engine APL recarregado.")


# ── disparadores de requisição ────────────────────────────────────────────────

async def _fire_login(client: httpx.AsyncClient, username: str, password: str) -> ReqResult:
    t0 = time.perf_counter()
    try:
        r = await client.post("/auth/token", data={"username": username, "password": password})
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


async def _fire_validate(client: httpx.AsyncClient, token: str) -> ReqResult:
    t0 = time.perf_counter()
    try:
        r = await client.post("/auth/validate", json={"token": token})
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


async def _fire_check(client: httpx.AsyncClient, token: str) -> ReqResult:
    t0 = time.perf_counter()
    try:
        r = await client.post("/auth/check", json={
            "token": token,
            "require_roles": ["admin"],
        })
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


async def _fire_apl_evaluate(client: httpx.AsyncClient, token: str) -> ReqResult:
    """Stress do endpoint /admin/policies/evaluate — APL engine."""
    t0 = time.perf_counter()
    try:
        r = await client.post(
            "/admin/policies/evaluate",
            json={
                "subject": {"department": "stress", "roles": ["vendedor"], "user_level": 3},
                "action": "cotacao:create",
                "resource": "cotacao/stress-123",
                "tenant_id": "tenant-stress",
                "subject_id": f"stress-subj-{uuid.uuid4().hex[:8]}",
                "use_cache": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


async def _fire_apl_evaluate_cached(client: httpx.AsyncClient, token: str) -> ReqResult:
    """APL evaluate com subject_id fixo — força cache hit."""
    t0 = time.perf_counter()
    try:
        r = await client.post(
            "/admin/policies/evaluate",
            json={
                "subject": {"department": "stress", "roles": ["vendedor"], "user_level": 3},
                "action": "cotacao:read",
                "resource": "cotacao/cached-resource",
                "tenant_id": "tenant-stress",
                "subject_id": "stress-cached-subject",
                "use_cache": True,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


async def _fire_refresh(client: httpx.AsyncClient, refresh_token: str) -> ReqResult:
    t0 = time.perf_counter()
    try:
        r = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(r.status_code == 200, r.status_code, ms)
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return ReqResult(False, 0, ms, str(e))


# ── análise de resultados ─────────────────────────────────────────────────────
def _analyze(results: list[ReqResult]) -> dict:
    if not results:
        return {
            "total": 0, "ok": 0, "errors": 0, "error_rate": 0.0,
            "avg_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0,
            "p50_ms": 0.0, "p90_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0,
            "status_dist": {},
        }
    latencies = sorted(r.latency_ms for r in results)
    ok_count  = sum(1 for r in results if r.ok)
    err_count = len(results) - ok_count
    status_dist: dict[int, int] = defaultdict(int)
    for r in results:
        status_dist[r.status] += 1

    n = len(latencies)
    def _pct(p: float) -> float:
        return latencies[min(int(n * p), n - 1)]

    return {
        "total":       n,
        "ok":          ok_count,
        "errors":      err_count,
        "error_rate":  round(err_count / n * 100, 2),
        "avg_ms":      round(sum(latencies) / n, 2),
        "min_ms":      round(latencies[0], 2),
        "max_ms":      round(latencies[-1], 2),
        "p50_ms":      round(_pct(0.50), 2),
        "p90_ms":      round(_pct(0.90), 2),
        "p95_ms":      round(_pct(0.95), 2),
        "p99_ms":      round(_pct(0.99), 2),
        "status_dist": dict(status_dist),
    }


def _print_stats(label: str, stats: dict, concurrency: int, duration_s: float):
    rps   = round(stats["total"] / duration_s, 2) if duration_s > 0 else 0
    er    = stats.get("error_rate", 0)
    color = "green" if er < 5 else ("yellow" if er < 20 else "red")
    t = Table(title=f"[bold]{label}[/bold] — {concurrency} req simultâneos", show_header=True,
              header_style="bold white", border_style="dim")
    t.add_column("Métrica",       style="cyan",  min_width=16)
    t.add_column("Valor",         style=color,   min_width=14)
    t.add_row("Total reqs",       str(stats["total"]))
    t.add_row("OK",               str(stats["ok"]))
    t.add_row("Erros",            str(stats["errors"]))
    t.add_row("Taxa de erro",     f"{er}%")
    t.add_row("RPS",              str(rps))
    t.add_row("Avg latência",     f"{stats['avg_ms']} ms")
    t.add_row("Min latência",     f"{stats['min_ms']} ms")
    t.add_row("Max latência",     f"{stats['max_ms']} ms")
    t.add_row("P50",              f"{stats['p50_ms']} ms")
    t.add_row("P90",              f"{stats['p90_ms']} ms")
    t.add_row("P95",              f"{stats['p95_ms']} ms")
    t.add_row("P99",              f"{stats['p99_ms']} ms")
    t.add_row("Status dist",      str(stats["status_dist"]))
    console.print(t)


# ── runner de carga com rampa ─────────────────────────────────────────────────
async def _run_concurrent(
    label: str,
    fire_fn,
    concurrency: int,
) -> tuple[dict, float]:
    """
    Dispara `concurrency` requisições simultâneas.
    Retorna (stats, duration_s).
    """
    t_start = time.perf_counter()
    async with _client() as c:
        tasks   = [fire_fn(c) for _ in range(concurrency)]
        results = await asyncio.gather(*tasks)
    duration = time.perf_counter() - t_start
    stats    = _analyze(list(results))
    _print_stats(label, stats, concurrency, duration)
    return stats, duration


# ── cenários de stress ────────────────────────────────────────────────────────

async def stress_login() -> list[dict]:
    _hdr("⚔️  STRESS — Login (/auth/token) — Finn vs Lich King")
    _info(f"Usuário: {_test_user} | Rampa: {RAMP_LEVELS}")
    report = []
    for level in RAMP_LEVELS:
        console.print(f"\n  [yellow]→ {level} logins simultâneos[/yellow]")
        stats, dur = await _run_concurrent(
            f"LOGIN x{level}",
            lambda c, u=_test_user, p=_test_pass: _fire_login(c, u, p),
            concurrency=level,
        )
        report.append({"scenario": "login", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


async def stress_validate() -> list[dict]:
    _hdr("🔮 STRESS — Validate Token (/auth/validate) — Magia de Marceline")
    if not _test_token:
        _err("Sem token de teste. Pulando.")
        return []
    report = []
    for level in RAMP_LEVELS:
        console.print(f"\n  [yellow]→ {level} validates simultâneos[/yellow]")
        stats, dur = await _run_concurrent(
            f"VALIDATE x{level}",
            lambda c, tok=_test_token: _fire_validate(c, tok),
            concurrency=level,
        )
        report.append({"scenario": "validate", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


async def stress_check() -> list[dict]:
    _hdr("🛡️  STRESS — Check RBAC+ABAC (/auth/check) — Escudo de Bubblegum")
    if not _admin_token:
        _err("Sem token admin. Pulando.")
        return []
    report = []
    for level in RAMP_LEVELS:
        console.print(f"\n  [yellow]→ {level} checks simultâneos[/yellow]")
        stats, dur = await _run_concurrent(
            f"CHECK x{level}",
            lambda c, tok=_admin_token: _fire_check(c, tok),
            concurrency=level,
        )
        report.append({"scenario": "check", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


async def stress_apl_evaluate() -> list[dict]:
    _hdr("📜 STRESS — APL Evaluate (/admin/policies/evaluate) — Grimório de Jake")
    if not _admin_token:
        _err("Sem token admin. Pulando.")
        return []
    report = []
    for level in RAMP_LEVELS:
        console.print(f"\n  [yellow]→ {level} evaluates APL simultâneos[/yellow]")
        stats, dur = await _run_concurrent(
            f"APL-EVAL x{level}",
            lambda c, tok=_admin_token: _fire_apl_evaluate(c, tok),
            concurrency=level,
        )
        report.append({"scenario": "apl_evaluate", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


async def stress_apl_cache() -> list[dict]:
    """APL evaluate com subject_id fixo — mede ganho do cache de decisão."""
    _hdr("⚡ STRESS — APL Cache Hit (/admin/policies/evaluate cached) — BMO Turbo")
    if not _admin_token:
        _err("Sem token admin. Pulando.")
        return []
    report = []
    for level in RAMP_LEVELS:
        console.print(f"\n  [yellow]→ {level} cache-hit evaluates simultâneos[/yellow]")
        stats, dur = await _run_concurrent(
            f"APL-CACHE x{level}",
            lambda c, tok=_admin_token: _fire_apl_evaluate_cached(c, tok),
            concurrency=level,
        )
        report.append({"scenario": "apl_cache", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


async def stress_mixed() -> list[dict]:
    """Cenário misto: login + validate + check + APL evaluate simultâneos."""
    _hdr("🌈 STRESS — Cenário Misto — Festa no Castelo de Ooo")
    if not _test_token or not _admin_token:
        _err("Tokens ausentes. Pulando cenário misto.")
        return []
    report = []
    for level in [10, 25, 50, 100, 200, 500]:
        console.print(f"\n  [yellow]→ {level} reqs mistas simultâneas[/yellow]")
        t_start = time.perf_counter()
        async with _client() as c:
            q = level // 4
            rem = level - 3 * q
            tasks = (
                [_fire_login(c, _test_user, _test_pass)     for _ in range(q)] +
                [_fire_validate(c, _test_token)              for _ in range(q)] +
                [_fire_check(c, _admin_token)                for _ in range(q)] +
                [_fire_apl_evaluate(c, _admin_token)         for _ in range(rem)]
            )
            results = await asyncio.gather(*tasks)
        dur   = time.perf_counter() - t_start
        stats = _analyze(list(results))
        _print_stats(f"MIXED x{level}", stats, level, dur)
        report.append({"scenario": "mixed", "concurrency": level,
                        "duration_s": round(dur, 3), **stats})
        if stats["error_rate"] > BREAK_THRESHOLD:
            _warn(f"⚡ BREAKING POINT em {level} req simultâneos (erro {stats['error_rate']}%)")
            break
        await asyncio.sleep(0.3)
    return report


# ── relatório final ───────────────────────────────────────────────────────────
def _breaking_point(report: list[dict]) -> dict | None:
    for entry in report:
        if entry.get("error_rate", 0) > BREAK_THRESHOLD:
            return entry
    return None


def _save_report(all_data: dict):
    base = os.path.join(LOGS_DIR, f"stress_{RUN_ID}")
    with open(f"{base}.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    with open(f"{base}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(all_data, f, allow_unicode=True, default_flow_style=False)
    _write_md(all_data, f"{base}.md")
    _ok(f"Relatório salvo em: {base}.[json|yaml|md]")


def _write_md(data: dict, path: str):
    lines = [
        "# 🌟 Apollo IAM Engine — Stress Test Report",
        "",
        "> *\"Hora de Aventura com Finn e Jake no Reino de Ooo IAM\"*",
        "",
        f"**Run ID:** `{data['run_id']}`  ",
        f"**Data:** {data['timestamp']}  ",
        f"**Servidor:** {data['server']}  ",
        f"**Breaking threshold:** {BREAK_THRESHOLD}% de erro  ",
        "",
        "---",
        "",
    ]
    for scenario, entries in data["scenarios"].items():
        lines.append(f"## Cenário: `{scenario.upper()}`")
        lines.append("")
        lines.append("| Concorrência | Total | OK | Erros | Erro% | Avg ms | P50 | P90 | P95 | P99 | RPS |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for e in entries:
            rps = round(e["total"] / e["duration_s"], 1) if e.get("duration_s", 0) > 0 else 0
            bp  = " ⚡ BREAK" if e.get("error_rate", 0) > BREAK_THRESHOLD else ""
            lines.append(
                f"| {e['concurrency']} | {e['total']} | {e['ok']} | {e['errors']} "
                f"| {e['error_rate']}%{bp} | {e['avg_ms']} | {e['p50_ms']} "
                f"| {e['p90_ms']} | {e['p95_ms']} | {e['p99_ms']} | {rps} |"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "## 🔥 Breaking Points",
        "",
    ]
    for scenario, entries in data["scenarios"].items():
        bp = _breaking_point(entries)
        if bp:
            lines.append(
                f"- **{scenario}**: quebra em **{bp['concurrency']} req simultâneos** "
                f"(erro {bp['error_rate']}%, avg {bp['avg_ms']} ms, P99 {bp['p99_ms']} ms)"
            )
        else:
            last = entries[-1] if entries else {}
            lines.append(
                f"- **{scenario}**: ✅ estável até **{last.get('concurrency', 0)} req simultâneos** "
                f"(erro {last.get('error_rate', 0)}%, avg {last.get('avg_ms', 0)} ms)"
            )

    lines += [
        "",
        "---",
        "",
        "## 📊 Conclusão",
        "",
        data.get("conclusion", "N/A"),
        "",
        "---",
        "",
        "*Gerado automaticamente pelo Apollo IAM Engine Stress Suite — O2 Data Solutions*",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _print_final_report(all_data: dict):
    _hdr("📊 RELATÓRIO CONSOLIDADO — Finn e Jake vencem mais uma aventura")
    t = Table(title="Breaking Points por Cenário", show_header=True,
              header_style="bold white", border_style="dim")
    t.add_column("Cenário",        style="cyan",   min_width=16)
    t.add_column("Breaking Point", style="red",    min_width=20)
    t.add_column("Erro%",          style="yellow", min_width=8)
    t.add_column("Avg ms",         style="white",  min_width=10)
    t.add_column("P50 ms",         style="white",  min_width=10)
    t.add_column("P99 ms",         style="white",  min_width=10)
    for scenario, entries in all_data["scenarios"].items():
        bp = _breaking_point(entries)
        if bp:
            t.add_row(scenario, f"⚡ {bp['concurrency']} req",
                      f"{bp['error_rate']}%", f"{bp['avg_ms']} ms",
                      f"{bp['p50_ms']} ms", f"{bp['p99_ms']} ms")
        else:
            last = entries[-1] if entries else {}
            t.add_row(scenario, "✅ Estável",
                      f"{last.get('error_rate', 0)}%",
                      f"{last.get('avg_ms', 0)} ms",
                      f"{last.get('p50_ms', 0)} ms",
                      f"{last.get('p99_ms', 0)} ms")
    console.print(t)
    console.print(Panel(
        all_data.get("conclusion", ""),
        title="[bold green]🏆 Conclusão[/bold green]",
        border_style="green",
    ))


# ── main ──────────────────────────────────────────────────────────────────────
async def main():
    console.print()
    console.print(Panel(
        "[bold cyan]🌟 Apollo IAM Engine — Stress & Benchmark Test Suite[/bold cyan]\n"
        "[dim]\"Hora de Aventura com Finn e Jake no Reino de Ooo IAM\"[/dim]\n\n"
        f"Servidor:  [yellow]{BASE}[/yellow]\n"
        f"Run ID:    [yellow]{RUN_ID}[/yellow]\n"
        f"Rampa:     [yellow]{RAMP_LEVELS}[/yellow]\n"
        f"Break em:  [yellow]{BREAK_THRESHOLD}% de erro[/yellow]",
        border_style="cyan",
        expand=False,
    ))

    await setup()

    login_report    = await stress_login()
    validate_report = await stress_validate()
    check_report    = await stress_check()
    apl_report      = await stress_apl_evaluate()
    cache_report    = await stress_apl_cache()
    mixed_report    = await stress_mixed()

    # ── conclusão automática ──────────────────────────────────────────────────
    conclusions = []
    scenario_map = [
        ("login",        login_report),
        ("validate",     validate_report),
        ("check",        check_report),
        ("apl_evaluate", apl_report),
        ("apl_cache",    cache_report),
        ("mixed",        mixed_report),
    ]
    for scenario, report in scenario_map:
        if not report:
            conclusions.append(f"[{scenario.upper()}] Pulado (sem dados).")
            continue
        bp = _breaking_point(report)
        if bp:
            conclusions.append(
                f"[{scenario.upper()}] Breaking point em {bp['concurrency']} req simultâneos "
                f"(erro {bp['error_rate']}%, avg {bp['avg_ms']} ms, P99 {bp['p99_ms']} ms)."
            )
        else:
            last = report[-1]
            conclusions.append(
                f"[{scenario.upper()}] Estável até {last.get('concurrency', 0)} req simultâneos "
                f"(erro {last.get('error_rate', 0)}%, avg {last.get('avg_ms', 0)} ms, "
                f"P99 {last.get('p99_ms', 0)} ms)."
            )

    # compara APL sem cache vs com cache
    if apl_report and cache_report:
        last_apl   = apl_report[-1]
        last_cache = cache_report[-1]
        if last_apl.get("avg_ms", 0) > 0 and last_cache.get("avg_ms", 0) > 0:
            speedup = round(last_apl["avg_ms"] / last_cache["avg_ms"], 2)
            conclusions.append(
                f"[CACHE SPEEDUP] APL cache hit é {speedup}x mais rápido que avaliação completa "
                f"no nível {last_cache.get('concurrency', 0)} req simultâneos."
            )

    conclusion_text = "\n".join(conclusions)

    all_data = {
        "run_id":    RUN_ID,
        "timestamp": datetime.now().isoformat(),
        "server":    BASE,
        "ramp":      RAMP_LEVELS,
        "break_threshold_pct": BREAK_THRESHOLD,
        "scenarios": {
            "login":        login_report,
            "validate":     validate_report,
            "check":        check_report,
            "apl_evaluate": apl_report,
            "apl_cache":    cache_report,
            "mixed":        mixed_report,
        },
        "conclusion": conclusion_text,
    }

    _print_final_report(all_data)
    _save_report(all_data)


if __name__ == "__main__":
    asyncio.run(main())
