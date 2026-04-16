"""
project-production-test.py
╔══════════════════════════════════════════════════════════════════════════════╗
║  🌟 APOLLO IAM ENGINE — Production Test Suite v4 🌟                        ║
║  Cobertura 100%: Health, Auth, RBAC, ABAC, APL DSL, Cache, Multi-tenant,   ║
║  User Types/Levels, Custom Entities, Settings, Audit, Groups, Metrics,     ║
║  Policies (CRUD + Evaluate + Explain + Toggle + Raw + Scope + Inherit),    ║
║  Stress, Cleanup, Relatório JSON/YAML/MD incremental em tempo real.        ║
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
    lines += ["", "---", "", "*Gerado pelo Apollo IAM Engine Production Test Suite v4 — O2 Data Solutions*"]
    with open(f"{_LOG_BASE}.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return summary

