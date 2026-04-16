"""
security_config.py
Carrega config/security.yaml e expõe como dict/objeto.
O2 Data Solutions
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml


def _find_security_yaml() -> Path:
    """Procura config/security.yaml a partir da raiz do projeto."""
    # sobe até encontrar config/security.yaml
    here = Path(__file__).resolve()
    for parent in [here.parent, here.parent.parent,
                   here.parent.parent.parent,
                   here.parent.parent.parent.parent]:
        candidate = parent / "config" / "security.yaml"
        if candidate.exists():
            return candidate
    # fallback: cwd
    return Path("config") / "security.yaml"


@lru_cache(maxsize=1)
def load_security_config() -> dict:
    path = _find_security_yaml()
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_tls_config() -> dict:
    return load_security_config().get("tls", {})


def get_seed_config() -> dict:
    return load_security_config().get("seed", {})


def get_security_headers_config() -> dict:
    return load_security_config().get("security_headers", {})


def is_mtls_enabled() -> bool:
    return get_tls_config().get("enabled", False)


def get_certs_dir() -> Path:
    cfg = get_tls_config()
    raw = cfg.get("certs_dir", "certs")
    p = Path(raw)
    if not p.is_absolute():
        # resolve relativo à raiz do projeto
        root = _find_security_yaml().parent.parent
        p = root / raw
    return p.resolve()


def get_api_port() -> int:
    return get_tls_config().get("api_port", 8443)


def get_webapp_port() -> int:
    return get_tls_config().get("webapp_port", 8444)


def get_client_auth_mode() -> str:
    """'required' | 'optional' | 'disabled'"""
    return get_tls_config().get("client_auth", "required")
