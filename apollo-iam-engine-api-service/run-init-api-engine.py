"""
run-init-api-engine.py
Sobe Apollo IAM Engine API + WebApp com mTLS (RSA-2048).

Fluxo de inicialização:
  1. Carrega config/security.yaml
  2. Gera/verifica PKI interna (CA + server cert + client cert) em certs/
  3. Cria ssl.SSLContext com mTLS completo (TLS 1.2+, CERT_REQUIRED, ciphers fortes)
  4. Sobe API   em https://0.0.0.0:8443  — uvicorn.run() com ssl_context
  5. Sobe WebApp em https://0.0.0.0:8444 — uvicorn.run() com ssl_context
  6. Watchdog reinicia automaticamente se qualquer serviço cair

Nota sobre reload:
  - mTLS ON  → reload=False (ssl_context não é serializável entre subprocessos)
              Para dev com hot-reload, use MTLS_ENABLED=false no .env
  - mTLS OFF → reload=True  (HTTP, desenvolvimento local)

Execute: python run-init-api-engine.py
O2 Data Solutions
"""

import os
import sys
import ssl
import multiprocessing
import threading
import time
import asyncio
from datetime import datetime
from pathlib import Path

from colorama import init
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

init(autoreset=True)
console = Console()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.infrastructure.config.security_config import (
    load_security_config, get_certs_dir, get_api_port,
    get_webapp_port, get_client_auth_mode, is_mtls_enabled,
)
from src.infrastructure.security.cert_manager import ensure_certs, CertPaths

_SEC_CFG     = load_security_config()
_CERTS: CertPaths | None = None
_API_PORT    = get_api_port()
_WEBAPP_PORT = get_webapp_port()
_MTLS_ON     = is_mtls_enabled()

# ── 1. Bootstrap PKI ──────────────────────────────────────────────────────────

def _bootstrap_certs() -> None:
    global _CERTS
    if not _MTLS_ON:
        console.print("[bold yellow]⚠  mTLS desabilitado — rodando em HTTP (dev mode)[/bold yellow]")
        return
    console.print()
    console.print(Rule("[bold cyan]🔐 Bootstrap PKI — mTLS[/bold cyan]", style="cyan"))
    _CERTS = ensure_certs(certs_dir=get_certs_dir(), security_cfg=_SEC_CFG)
    console.print()
    t = Table(border_style="dim", show_header=True, header_style="bold white")
    t.add_column("Arquivo",    style="bold cyan",  min_width=14)
    t.add_column("Caminho",    style="bold green", min_width=54)
    t.add_row("CA cert",       str(_CERTS.ca_crt))
    t.add_row("Server key",    str(_CERTS.server_key))
    t.add_row("Server cert",   str(_CERTS.server_crt))
    t.add_row("Client key",    str(_CERTS.client_key))
    t.add_row("Client cert",   str(_CERTS.client_crt))
    t.add_row("Client P12",    str(_CERTS.client_p12))
    console.print(t)
    console.print()


# ── 2. SSLContext com mTLS completo ───────────────────────────────────────────

def _build_ssl_context(certs: CertPaths) -> ssl.SSLContext:
    """
    SSLContext de servidor com mTLS:
      - TLS 1.2 mínimo (TLS 1.3 preferido automaticamente)
      - Cipher suites fortes: ECDHE+AES-GCM, ECDHE+CHACHA20
      - Sem RC4, 3DES, NULL, EXPORT, MD5
      - Verificação de certificado do cliente (CERT_REQUIRED por padrão)
      - CA interna como único trust anchor
    """
    mode = get_client_auth_mode()

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.set_ciphers(
        "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20"
        ":!aNULL:!eNULL:!EXPORT:!DES:!3DES:!RC4:!MD5:!PSK:!SRP"
    )
    ctx.load_cert_chain(
        certfile=str(certs.server_crt),
        keyfile=str(certs.server_key),
    )
    ctx.load_verify_locations(cafile=str(certs.ca_crt))
    ctx.check_hostname = False

    if mode == "required":
        ctx.verify_mode = ssl.CERT_REQUIRED
    elif mode == "optional":
        ctx.verify_mode = ssl.CERT_OPTIONAL
    else:
        ctx.verify_mode = ssl.CERT_NONE

    return ctx


# ── 3. Worker de serviço ──────────────────────────────────────────────────────

def _worker(app_module: str, host: str, port: int,
            mtls_on: bool, certs_dir_str: str, sec_cfg: dict) -> None:
    """
    Roda em processo filho via multiprocessing.
    Usa ssl_keyfile/certfile/ca_certs do uvicorn + configura verify_mode
    diretamente no SSLContext via uvicorn.Config.
    """
    import uvicorn
    from uvicorn.config import Config
    from uvicorn.main import Server
    from src.infrastructure.config.security_config import get_client_auth_mode

    kwargs: dict = {
        "app":       app_module,
        "host":      host,
        "port":      port,
        "log_level": "info",
        "reload":    not mtls_on,
    }

    if not mtls_on:
        kwargs["reload_dirs"] = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")]
        uvicorn.run(**kwargs)
        return

    # suprime ConnectionResetError do Windows (WinError 10054) — ruído do ProactorEventLoop
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # mTLS: carrega certs e constrói SSLContext manualmente,
    # depois injeta no Config do uvicorn antes de servir.
    from pathlib import Path
    from src.infrastructure.security.cert_manager import ensure_certs

    certs = ensure_certs(Path(certs_dir_str), sec_cfg)
    mode  = get_client_auth_mode()

    # Cria o Config sem ssl — vamos injetar o contexto depois
    kwargs["ssl_keyfile"]  = str(certs.server_key)
    kwargs["ssl_certfile"] = str(certs.server_crt)
    kwargs["ssl_ca_certs"] = str(certs.ca_crt)

    config = Config(**kwargs)
    config.load()   # inicializa o config (carrega app, etc.)

    # Pega o SSLContext que o uvicorn criou e reforça as configurações
    if config.ssl:
        config.ssl.minimum_version = ssl.TLSVersion.TLSv1_2
        try:
            config.ssl.set_ciphers(
                "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20"
                ":!aNULL:!eNULL:!EXPORT:!DES:!3DES:!RC4:!MD5:!PSK:!SRP"
            )
        except ssl.SSLError:
            pass  # fallback: mantém ciphers padrão do uvicorn
        config.ssl.check_hostname = False
        if mode == "required":
            config.ssl.verify_mode = ssl.CERT_REQUIRED
        elif mode == "optional":
            config.ssl.verify_mode = ssl.CERT_OPTIONAL
        else:
            config.ssl.verify_mode = ssl.CERT_NONE

    server = Server(config=config)
    server.run()


# ── 4. Gerenciamento de processos ─────────────────────────────────────────────

_running = True
_procs: dict[str, multiprocessing.Process] = {}
_lock = threading.Lock()
SERVICES: dict = {}


def _build_services() -> dict:
    proto = "https" if _MTLS_ON else "http"
    return {
        "API": {
            "module": "src.interface.api.main:app",
            "host":   "0.0.0.0",
            "port":   _API_PORT if _MTLS_ON else 8000,
            "color":  "bold cyan",
            "proto":  proto,
        },
        "WEBAPP": {
            "module": "src.interface.webapp.main:app",
            "host":   "0.0.0.0",
            "port":   _WEBAPP_PORT if _MTLS_ON else 8080,
            "color":  "bold magenta",
            "proto":  proto,
        },
    }


def _start(name: str) -> multiprocessing.Process:
    cfg = SERVICES[name]
    ts = datetime.now().strftime("%H:%M:%S")
    proto_badge = "[bold green]HTTPS/mTLS[/bold green]" if _MTLS_ON else "[yellow]HTTP (dev)[/yellow]"
    console.print(
        f"[dim]{ts}[/dim] [{cfg['color']}][{name}][/{cfg['color']}] "
        f"[bold green]▶ Iniciando...[/bold green] "
        f"porta {cfg['port']} {proto_badge}"
    )
    p = multiprocessing.Process(
        target=_worker,
        args=(
            cfg["module"],
            cfg["host"],
            cfg["port"],
            _MTLS_ON,
            str(get_certs_dir()),
            _SEC_CFG,
        ),
        daemon=True,
        name=name,
    )
    p.start()
    return p


def _watchdog(name: str) -> None:
    global _running
    while _running:
        time.sleep(3)
        proc = _procs.get(name)
        if proc is None:
            continue
        if not proc.is_alive() and _running:
            ts = datetime.now().strftime("%H:%M:%S")
            console.print(
                f"[dim]{ts}[/dim] [{SERVICES[name]['color']}][{name}][/{SERVICES[name]['color']}] "
                f"[bold yellow]⚠️  Processo encerrou (exit={proc.exitcode}). "
                f"Reiniciando em 3s...[/bold yellow]"
            )
            time.sleep(3)
            if _running:
                with _lock:
                    _procs[name] = _start(name)


# ── 5. Banner ─────────────────────────────────────────────────────────────────

def _print_banner() -> None:
    console.print()
    mtls_badge = "[bold green]mTLS ON[/bold green]" if _MTLS_ON else "[bold yellow]HTTP dev mode[/bold yellow]"
    console.print(Panel.fit(
        f"[bold orange1]🚀 APOLLO IAM ENGINE[/bold orange1]  {mtls_badge}\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="orange1",
        padding=(1, 4),
    ))
    console.print()

    proto       = "https" if _MTLS_ON else "http"
    api_port    = SERVICES["API"]["port"]
    webapp_port = SERVICES["WEBAPP"]["port"]

    t = Table(border_style="dim", show_header=True, header_style="bold white")
    t.add_column("Serviço",    style="bold cyan",  min_width=14)
    t.add_column("URL",        style="bold green", min_width=44)
    t.add_column("Info",       style="dim white",  min_width=32)
    t.add_row("🔌 API",       f"{proto}://localhost:{api_port}",          "REST API + JWT")
    t.add_row("📖 Docs",      f"{proto}://localhost:{api_port}/docs",     "Swagger UI")
    t.add_row("📘 ReDoc",     f"{proto}://localhost:{api_port}/redoc",    "ReDoc")
    t.add_row("🌐 WebApp",    f"{proto}://localhost:{webapp_port}/admin", "Painel Admin")
    t.add_row("❤️  Health",    f"{proto}://localhost:{api_port}/health",  "Health check")
    if _MTLS_ON and _CERTS:
        t.add_row("🔐 CA cert",   str(_CERTS.ca_crt),     "Instale no cliente/browser")
        t.add_row("🔑 Client P12",str(_CERTS.client_p12), "Import p/ Postman/curl/browser")
    console.print(t)
    console.print()

    if _MTLS_ON and _CERTS:
        mode = get_client_auth_mode()
        console.print(Panel.fit(
            f"[bold cyan]mTLS mode:[/bold cyan] [bold]{mode}[/bold]  "
            f"[dim](TLS 1.2+ | ECDHE+AES-GCM | ECDHE+CHACHA20)[/dim]\n\n"
            "[bold cyan]curl:[/bold cyan]\n"
            f"[dim]curl --cacert {_CERTS.ca_crt} \\\n"
            f"     --cert   {_CERTS.client_crt} \\\n"
            f"     --key    {_CERTS.client_key} \\\n"
            f"     {proto}://localhost:{api_port}/health[/dim]\n\n"
            "[bold cyan]Python httpx:[/bold cyan]\n"
            "[dim]import httpx, ssl\n"
            "ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)\n"
            f"ctx.load_verify_locations('{_CERTS.ca_crt}')\n"
            f"ctx.load_cert_chain('{_CERTS.client_crt}', '{_CERTS.client_key}')\n"
            f"r = httpx.get('{proto}://localhost:{api_port}/health', verify=ctx)[/dim]",
            border_style="cyan",
        ))
        console.print()
    else:
        console.print(Panel.fit(
            "[bold yellow]Hot-reload ativo[/bold yellow] — salve qualquer .py para recarregar\n"
            "[dim]Para ativar mTLS: MTLS_ENABLED=true no .env[/dim]",
            border_style="yellow",
        ))
        console.print()


# ── 6. Shutdown ───────────────────────────────────────────────────────────────

def _shutdown() -> None:
    global _running
    _running = False
    console.print()
    console.print(Rule("[bold red]Encerrando serviços...[/bold red]", style="red"))
    for name, proc in _procs.items():
        cfg = SERVICES[name]
        try:
            proc.terminate()
            proc.join(timeout=5)
            if proc.is_alive():
                proc.kill()
        except Exception:
            pass
        console.print(
            f"  [red]■[/red] [{cfg['color']}]{name}[/{cfg['color']}] encerrado."
        )
    console.print()
    console.print(Panel.fit(
        "[bold red]🛑 Apollo IAM Engine encerrado.[/bold red]\n"
        "[dim]O2 Data Solutions[/dim]",
        border_style="red",
    ))


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    multiprocessing.freeze_support()   # necessário no Windows

    _bootstrap_certs()
    SERVICES.update(_build_services())
    _print_banner()

    for name in SERVICES:
        _procs[name] = _start(name)

    for name in SERVICES:
        t = threading.Thread(target=_watchdog, args=(name,), daemon=True)
        t.start()

    console.print()
    console.print(Rule(
        "[dim]pressione [bold]Ctrl+C[/bold] para encerrar[/dim]",
        style="dim"
    ))
    console.print()

    try:
        while _running:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        _shutdown()
