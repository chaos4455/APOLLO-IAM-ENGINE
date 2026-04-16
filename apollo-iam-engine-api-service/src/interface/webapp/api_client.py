"""
api_client.py
Cliente HTTP centralizado do webapp — resolve URL da API e mTLS automaticamente.
"""
from __future__ import annotations
import ssl
from pathlib import Path
import httpx
from src.infrastructure.config.security_config import (
    is_mtls_enabled, get_certs_dir, get_api_port,
)


def _build_client() -> httpx.AsyncClient:
    if is_mtls_enabled():
        certs = get_certs_dir()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(cafile=str(certs / "ca" / "ca.crt"))
        ctx.load_cert_chain(
            certfile=str(certs / "client" / "client.crt"),
            keyfile=str(certs / "client" / "client.key"),
        )
        ctx.check_hostname = False
        port = get_api_port()
        base = f"https://localhost:{port}"
        return httpx.AsyncClient(base_url=base, verify=ctx, timeout=15.0)
    return httpx.AsyncClient(base_url="http://localhost:8000", timeout=15.0)


def api_client() -> httpx.AsyncClient:
    return _build_client()


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
