"""
upgradev2.py
Script único de upgrade do Apollo IAM Engine.
Executa tudo automaticamente:
  1. Cria metrics/logs.html (template faltando → erro 500 na rota /admin/metrics/logs)
  2. Cria rate_limit_middleware.py (rate limiting em memória por IP + por rota)
  3. Cria request_queue_middleware.py (pool/fila de requisições em memória)
  4. Atualiza API main.py com rate limit + fila
  5. Atualiza webapp main.py com rate limit
  6. Melhora security_headers_middleware.py (headers adicionais)
  7. Atualiza dashboard.html com link para métricas
  8. Verifica e reporta tudo

Execute: python upgradev2.py
O2 Data Solutions
"""

from __future__ import annotations
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

from colorama import init, Fore, Style
init(autoreset=True)

_HERE = Path(__file__).parent.resolve()
_SRC  = _HERE / "src"

ok_count   = 0
fail_count = 0
log_lines: list[str] = []


def _ok(msg: str):
    global ok_count
    ok_count += 1
    print(f"  {Fore.GREEN}✅ {msg}{Style.RESET_ALL}")
    log_lines.append(f"[OK]  {msg}")


def _fail(msg: str, exc: Exception = None):
    global fail_count
    fail_count += 1
    detail = f" — {exc}" if exc else ""
    print(f"  {Fore.RED}❌ {msg}{detail}{Style.RESET_ALL}")
    log_lines.append(f"[ERR] {msg}{detail}")


def _info(msg: str):
    print(f"  {Fore.CYAN}ℹ  {msg}{Style.RESET_ALL}")
    log_lines.append(f"[INF] {msg}")


def write_file(path: Path, content: str, label: str):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        _ok(label)
    except Exception as e:
        _fail(label, e)


def patch_file(path: Path, old: str, new: str, label: str):
    """Substitui old por new no arquivo. Idempotente."""
    try:
        if not path.exists():
            _fail(f"{label} — arquivo não encontrado: {path}")
            return
        text = path.read_text(encoding="utf-8")
        if new.strip() in text:
            _info(f"{label} — já aplicado, pulando")
            return
        if old not in text:
            _fail(f"{label} — trecho alvo não encontrado em {path.name}")
            return
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        _ok(label)
    except Exception as e:
        _fail(label, e)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. metrics/logs.html — template faltando (causa o erro 500)
# ═══════════════════════════════════════════════════════════════════════════════

LOGS_HTML = """\
{% extends "base.html" %}
{% block title %}Event Logs{% endblock %}
{% block head %}
<style>
.log-filters{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;align-items:center}
.log-filters input,.log-filters select{
  background:var(--bg-card);border:1px solid var(--border);color:var(--text);
  border-radius:var(--radius);padding:6px 10px;font-size:.83rem;outline:none}
.log-filters input:focus,.log-filters select:focus{border-color:var(--primary)}
.log-table-wrap{overflow-x:auto}
.log-table{width:100%;border-collapse:collapse;font-size:.83rem}
.log-table th{background:var(--bg-sidebar);color:var(--text-muted);font-weight:600;
  text-transform:uppercase;letter-spacing:.06em;padding:9px 12px;text-align:left;
  border-bottom:1px solid var(--border);white-space:nowrap}
.log-table td{padding:8px 12px;border-bottom:1px solid var(--border);vertical-align:middle}
.log-table tr:hover td{background:rgba(255,255,255,.03)}
.log-table tr:last-child td{border-bottom:none}
.mono{font-family:monospace;font-size:.8rem}
.badge-ok{background:rgba(34,197,94,.15);color:#22c55e;border-radius:4px;
  padding:2px 7px;font-size:.72rem;font-weight:600}
.badge-fail{background:rgba(239,68,68,.15);color:#ef4444;border-radius:4px;
  padding:2px 7px;font-size:.72rem;font-weight:600}
.pager{display:flex;gap:8px;align-items:center;margin-top:16px;flex-wrap:wrap}
.pager a,.pager span{padding:5px 12px;border-radius:var(--radius);font-size:.82rem;
  border:1px solid var(--border);text-decoration:none;color:var(--text)}
.pager a:hover{border-color:var(--primary);color:var(--primary)}
.pager .active{background:var(--primary);color:#fff;border-color:var(--primary)}
.total-badge{font-size:.8rem;color:var(--text-muted);margin-left:auto}
</style>
{% endblock %}
{% block content %}
<div class="page-header">
  <h1 class="page-title">🗂️ Event Logs</h1>
  <a href="/admin/metrics" class="btn btn-outline btn-sm">← Métricas</a>
</div>

<div class="card">
  <!-- filtros client-side -->
  <div class="log-filters">
    <input id="f-actor"    placeholder="Filtrar actor..."   oninput="filterLogs()" style="width:140px"/>
    <input id="f-action"   placeholder="Filtrar ação..."    oninput="filterLogs()" style="width:160px"/>
    <input id="f-resource" placeholder="Filtrar recurso..." oninput="filterLogs()" style="width:130px"/>
    <select id="f-status" onchange="filterLogs()">
      <option value="">Todos status</option>
      <option value="success">✓ success</option>
      <option value="failure">✗ failure</option>
    </select>
    <button class="btn btn-outline btn-sm" onclick="clearFilters()">✕ Limpar</button>
    <span class="total-badge" id="count-badge">{{ data.total }} registros</span>
  </div>

  <div class="log-table-wrap">
    <table class="log-table" id="log-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Ação</th>
          <th>Actor</th>
          <th>Recurso</th>
          <th>IP</th>
          <th>Status</th>
          <th>Data/Hora</th>
          <th>Detalhe</th>
        </tr>
      </thead>
      <tbody id="log-body">
        {% for log in data.logs %}
        <tr data-actor="{{ log.actor or '' }}"
            data-action="{{ log.action or '' }}"
            data-resource="{{ log.resource or '' }}"
            data-status="{{ log.status or '' }}">
          <td class="text-muted mono">{{ loop.index + skip }}</td>
          <td><span class="mono">{{ log.action }}</span></td>
          <td>{{ log.actor or '—' }}</td>
          <td><span class="badge badge-muted">{{ log.resource or '—' }}</span></td>
          <td class="mono text-muted">{{ log.ip_address or '—' }}</td>
          <td>
            {% if log.status == 'success' %}
              <span class="badge-ok">✓ ok</span>
            {% else %}
              <span class="badge-fail">✗ falha</span>
            {% endif %}
          </td>
          <td class="text-muted mono" style="white-space:nowrap">
            {{ log.created_at[:19] if log.created_at else '—' }}
          </td>
          <td class="text-muted" style="max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
              title="{{ log.detail or '' }}">
            {{ log.detail[:60] if log.detail else '—' }}
          </td>
        </tr>
        {% else %}
        <tr><td colspan="8" style="text-align:center;padding:32px;color:var(--text-muted)">
          Nenhum log encontrado.
        </td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <!-- paginação -->
  <div class="pager">
    {% if skip > 0 %}
    <a href="/admin/metrics/logs?skip={{ [skip - limit, 0]|max }}&limit={{ limit }}">← Anterior</a>
    {% else %}
    <span style="opacity:.4">← Anterior</span>
    {% endif %}

    <span class="active">{{ (skip // limit) + 1 }}</span>

    {% if skip + limit < data.total %}
    <a href="/admin/metrics/logs?skip={{ skip + limit }}&limit={{ limit }}">Próximo →</a>
    {% else %}
    <span style="opacity:.4">Próximo →</span>
    {% endif %}

    <span class="total-badge">
      {{ skip + 1 }}–{{ [skip + limit, data.total]|min }} de {{ data.total }}
    </span>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function filterLogs() {
  const actor    = document.getElementById('f-actor').value.toLowerCase();
  const action   = document.getElementById('f-action').value.toLowerCase();
  const resource = document.getElementById('f-resource').value.toLowerCase();
  const status   = document.getElementById('f-status').value.toLowerCase();
  const rows = document.querySelectorAll('#log-body tr[data-actor]');
  let visible = 0;
  rows.forEach(r => {
    const match =
      (!actor    || r.dataset.actor.toLowerCase().includes(actor)) &&
      (!action   || r.dataset.action.toLowerCase().includes(action)) &&
      (!resource || r.dataset.resource.toLowerCase().includes(resource)) &&
      (!status   || r.dataset.status === status);
    r.style.display = match ? '' : 'none';
    if (match) visible++;
  });
  const badge = document.getElementById('count-badge');
  if (badge) badge.textContent = visible + ' registros (filtrado)';
}

function clearFilters() {
  ['f-actor','f-action','f-resource'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('f-status').value = '';
  filterLogs();
  const badge = document.getElementById('count-badge');
  if (badge) badge.textContent = '{{ data.total }} registros';
}
</script>
{% endblock %}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Rate Limit Middleware (em memória, por IP + por rota)
# ═══════════════════════════════════════════════════════════════════════════════

RATE_LIMIT_MW = """\
\"\"\"
rate_limit_middleware.py
Rate limiting em memória — sliding window por IP.
Configuração por rota via RATE_LIMIT_RULES.
O2 Data Solutions
\"\"\"
from __future__ import annotations
import time
import asyncio
from collections import defaultdict, deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# ── regras por prefixo de rota (requests / janela em segundos) ────────────────
RATE_LIMIT_RULES: list[tuple[str, int, int]] = [
    # (prefixo,          max_requests, window_seconds)
    ("/auth/token",      10,  60),   # login: 10 tentativas/min por IP
    ("/auth/refresh",    20,  60),
    ("/auth/check",      60,  60),
    ("/auth/",           30,  60),
    ("/admin/metrics",   60,  60),
    ("/admin/",         120,  60),
    ("/",               200,  60),   # fallback global
]

# ── whitelist de IPs que nunca são limitados ──────────────────────────────────
WHITELIST_IPS: set[str] = {"127.0.0.1", "::1"}

# ── rotas que nunca são limitadas ─────────────────────────────────────────────
SKIP_PATHS: set[str] = {"/health", "/docs", "/redoc", "/openapi.json", "/static"}

_windows: dict[str, deque] = defaultdict(deque)
_lock = asyncio.Lock()


def _get_rule(path: str) -> tuple[int, int]:
    for prefix, max_req, window in RATE_LIMIT_RULES:
        if path.startswith(prefix):
            return max_req, window
    return 200, 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    \"\"\"
    Sliding window rate limiter em memória.
    Retorna 429 com header Retry-After quando o limite é excedido.
    \"\"\"

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path

        # skip static e rotas isentas
        for skip in SKIP_PATHS:
            if path.startswith(skip):
                return await call_next(request)

        ip = (request.headers.get("X-Forwarded-For") or
              (request.client.host if request.client else "unknown")).split(",")[0].strip()

        if ip in WHITELIST_IPS:
            return await call_next(request)

        max_req, window = _get_rule(path)
        key = f"{ip}:{path}"
        now = time.monotonic()

        async with _lock:
            dq = _windows[key]
            # remove timestamps fora da janela
            while dq and dq[0] < now - window:
                dq.popleft()

            if len(dq) >= max_req:
                retry_after = int(window - (now - dq[0])) + 1
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit excedido. Tente novamente em breve.",
                        "retry_after_seconds": retry_after,
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

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"]     = str(max_req)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"]    = str(window)
        return response
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Request Queue / Connection Pool Middleware (em memória)
# ═══════════════════════════════════════════════════════════════════════════════

REQUEST_QUEUE_MW = """\
\"\"\"
request_queue_middleware.py
Pool de requisições em memória com fila de espera.
Limita concorrência máxima e enfileira o excedente.
O2 Data Solutions
\"\"\"
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
    \"\"\"
    Controla concorrência via asyncio.Semaphore.
    Requisições além do limite entram em fila com timeout.
    \"\"\"

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
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Patches nos main.py da API e WebApp
# ═══════════════════════════════════════════════════════════════════════════════

# Patch API main.py — adiciona imports e middlewares
API_MAIN_OLD_IMPORT = "from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware"
API_MAIN_NEW_IMPORT = """\
from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware
from src.infrastructure.security.rate_limit_middleware import RateLimitMiddleware
from src.infrastructure.security.request_queue_middleware import RequestQueueMiddleware"""

API_MAIN_OLD_MW = "app.add_middleware(RequestLogMiddleware)\napp.add_middleware(SecurityHeadersMiddleware)"
API_MAIN_NEW_MW = """\
app.add_middleware(RequestLogMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestQueueMiddleware)"""

# Patch WebApp main.py — adiciona imports e middlewares
WEBAPP_MAIN_OLD_IMPORT = "from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware"
WEBAPP_MAIN_NEW_IMPORT = """\
from src.infrastructure.security.security_headers_middleware import SecurityHeadersMiddleware
from src.infrastructure.security.rate_limit_middleware import RateLimitMiddleware
from src.infrastructure.security.request_queue_middleware import RequestQueueMiddleware"""

WEBAPP_MAIN_OLD_MW = "app.add_middleware(SecurityHeadersMiddleware)"
WEBAPP_MAIN_NEW_MW = """\
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestQueueMiddleware)"""

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Melhoria no security_headers_middleware — adiciona headers extras
# ═══════════════════════════════════════════════════════════════════════════════

SEC_HEADERS_OLD = '        response.headers["Permissions-Policy"]       = "geolocation=(), microphone=(), camera=()"'
SEC_HEADERS_NEW = '''\
        response.headers["Permissions-Policy"]       = "geolocation=(), microphone=(), camera=()"
        response.headers["Cross-Origin-Opener-Policy"]   = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"'''

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Patch no dashboard.html — adiciona card de métricas
# ═══════════════════════════════════════════════════════════════════════════════

DASH_OLD = '  <a href="/admin/user-levels" class="stat-card" style="text-decoration:none">'
DASH_NEW = '''\
  <a href="/admin/metrics" class="stat-card" style="text-decoration:none">
    <div class="stat-icon">📈</div>
    <div><div class="stat-value">KPIs</div><div class="stat-label">Métricas</div></div>
  </a>
  <a href="/admin/user-levels" class="stat-card" style="text-decoration:none">'''

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — executa tudo
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print()
    print(f"{Fore.CYAN}{'═'*60}")
    print(f"  🚀 Apollo IAM Engine — upgradev2.py")
    print(f"  O2 Data Solutions — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'═'*60}{Style.RESET_ALL}")
    print()

    # ── 1. metrics/logs.html ──────────────────────────────────────────────────
    print(f"{Fore.YELLOW}[1/6] Criando metrics/logs.html{Style.RESET_ALL}")
    logs_html_path = _SRC / "interface" / "webapp" / "templates" / "metrics" / "logs.html"
    write_file(logs_html_path, LOGS_HTML, "metrics/logs.html criado")

    # ── 2. rate_limit_middleware.py ───────────────────────────────────────────
    print(f"\n{Fore.YELLOW}[2/6] Criando rate_limit_middleware.py{Style.RESET_ALL}")
    rl_path = _SRC / "infrastructure" / "security" / "rate_limit_middleware.py"
    write_file(rl_path, RATE_LIMIT_MW, "rate_limit_middleware.py criado")

    # ── 3. request_queue_middleware.py ────────────────────────────────────────
    print(f"\n{Fore.YELLOW}[3/6] Criando request_queue_middleware.py{Style.RESET_ALL}")
    rq_path = _SRC / "infrastructure" / "security" / "request_queue_middleware.py"
    write_file(rq_path, REQUEST_QUEUE_MW, "request_queue_middleware.py criado")

    # ── 4. Patch API main.py ──────────────────────────────────────────────────
    print(f"\n{Fore.YELLOW}[4/6] Patchando API main.py (rate limit + fila){Style.RESET_ALL}")
    api_main = _SRC / "interface" / "api" / "main.py"
    patch_file(api_main, API_MAIN_OLD_IMPORT, API_MAIN_NEW_IMPORT,
               "API main.py — imports rate limit + queue")
    patch_file(api_main, API_MAIN_OLD_MW, API_MAIN_NEW_MW,
               "API main.py — middlewares rate limit + queue")

    # ── 5. Patch WebApp main.py ───────────────────────────────────────────────
    print(f"\n{Fore.YELLOW}[5/6] Patchando WebApp main.py (rate limit + fila){Style.RESET_ALL}")
    webapp_main = _SRC / "interface" / "webapp" / "main.py"
    patch_file(webapp_main, WEBAPP_MAIN_OLD_IMPORT, WEBAPP_MAIN_NEW_IMPORT,
               "WebApp main.py — imports rate limit + queue")
    patch_file(webapp_main, WEBAPP_MAIN_OLD_MW, WEBAPP_MAIN_NEW_MW,
               "WebApp main.py — middlewares rate limit + queue")

    # ── 6. Melhorias de segurança + dashboard ─────────────────────────────────
    print(f"\n{Fore.YELLOW}[6/6] Melhorias de segurança e dashboard{Style.RESET_ALL}")
    sec_mw = _SRC / "infrastructure" / "security" / "security_headers_middleware.py"
    patch_file(sec_mw, SEC_HEADERS_OLD, SEC_HEADERS_NEW,
               "security_headers_middleware.py — headers extras (COOP, CORP, Cache-Control)")

    dash_html = _SRC / "interface" / "webapp" / "templates" / "dashboard.html"
    patch_file(dash_html, DASH_OLD, DASH_NEW,
               "dashboard.html — card de métricas adicionado")

    # ── Relatório final ───────────────────────────────────────────────────────
    print()
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    total = ok_count + fail_count
    pct   = int(ok_count / total * 100) if total else 0
    color = Fore.GREEN if fail_count == 0 else Fore.YELLOW
    print(f"  {color}Resultado: {ok_count}/{total} operações OK ({pct}%){Style.RESET_ALL}")

    if fail_count:
        print(f"  {Fore.RED}⚠  {fail_count} operação(ões) falharam — veja acima{Style.RESET_ALL}")
    else:
        print(f"  {Fore.GREEN}🎉 Tudo aplicado com sucesso!{Style.RESET_ALL}")

    print()
    print(f"{Fore.CYAN}  O que foi feito:{Style.RESET_ALL}")
    print(f"  • metrics/logs.html — template criado (corrige erro 500 em /admin/metrics/logs)")
    print(f"  • rate_limit_middleware.py — sliding window por IP (10 logins/min, etc.)")
    print(f"  • request_queue_middleware.py — pool {50} concurrent + fila {200}")
    print(f"  • API + WebApp — middlewares registrados")
    print(f"  • security_headers_middleware.py — COOP, CORP, Cache-Control adicionados")
    print(f"  • dashboard.html — card de métricas adicionado")
    print()
    print(f"{Fore.CYAN}  Próximos passos:{Style.RESET_ALL}")
    print(f"  1. Reinicie o servidor: python run-init-api-engine.py")
    print(f"  2. Rode os testes:      python project-production-test.py")
    print(f"  3. Acesse métricas:     http://localhost:8080/admin/metrics")
    print(f"  4. Acesse logs:         http://localhost:8080/admin/metrics/logs")
    print(f"{Fore.CYAN}{'═'*60}{Style.RESET_ALL}")
    print()

    # salva log
    log_path = _HERE / "project-test-run-setup-logs" / f"upgradev2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path.parent.mkdir(exist_ok=True)
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"  Log salvo em: {log_path.name}")
    print()

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
