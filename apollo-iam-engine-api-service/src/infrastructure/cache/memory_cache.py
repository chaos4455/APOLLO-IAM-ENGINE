"""
memory_cache.py
Cache em memória com TTL, LRU eviction e invalidação por tag.
Thread-safe via threading.Lock (compatível com uvicorn workers síncronos e assíncronos).
O2 Data Solutions
"""
from __future__ import annotations

import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Optional


class _Entry:
    __slots__ = ("value", "expires_at")

    def __init__(self, value: Any, ttl: float):
        self.value = value
        self.expires_at = time.monotonic() + ttl if ttl > 0 else float("inf")

    @property
    def alive(self) -> bool:
        return time.monotonic() < self.expires_at


class MemoryCache:
    """
    Cache LRU em memória com TTL por entrada.

    Parâmetros
    ----------
    max_size : int
        Número máximo de entradas. Quando excedido, remove a entrada
        menos recentemente usada (LRU).
    default_ttl : float
        TTL padrão em segundos (0 = sem expiração).
    """

    def __init__(self, max_size: int = 1024, default_ttl: float = 60.0):
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, _Entry] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    # ── operações básicas ─────────────────────────────────────────────────────

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if not entry.alive:
                del self._store[key]
                self._misses += 1
                return None
            # move para o fim (mais recente)
            self._store.move_to_end(key)
            self._hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl: float = 0.0) -> None:
        ttl = ttl if ttl > 0 else self._default_ttl
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = _Entry(value, ttl)
            # evict LRU se excedeu max_size
            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def delete(self, key: str) -> None:
        with self._lock:
            self._store.pop(key, None)

    def delete_prefix(self, prefix: str) -> int:
        """Remove todas as chaves que começam com `prefix`. Retorna quantidade removida."""
        with self._lock:
            keys = [k for k in self._store if k.startswith(prefix)]
            for k in keys:
                del self._store[k]
            return len(keys)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: float = 0.0) -> Any:
        """Retorna valor do cache ou chama factory() e armazena o resultado."""
        val = self.get(key)
        if val is not None:
            return val
        val = factory()
        if val is not None:
            self.set(key, val, ttl)
        return val

    # ── stats ─────────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        with self._lock:
            total = self._hits + self._misses
            return {
                "size":      len(self._store),
                "max_size":  self._max_size,
                "hits":      self._hits,
                "misses":    self._misses,
                "hit_rate":  round(self._hits / total, 4) if total else 0.0,
                "default_ttl": self._default_ttl,
            }

    def purge_expired(self) -> int:
        """Remove entradas expiradas. Útil para manutenção periódica."""
        with self._lock:
            expired = [k for k, e in self._store.items() if not e.alive]
            for k in expired:
                del self._store[k]
            return len(expired)


# ── instâncias globais (singletons por processo) ──────────────────────────────

# Cache de tokens JWT decodificados — TTL curto, alta frequência
# Chave: hash do token raw → valor: TokenPayload serializado
token_cache = MemoryCache(max_size=4096, default_ttl=30.0)

# Cache de blacklist de tokens — TTL médio
# Chave: jti → valor: True (revogado) | False (não revogado)
blacklist_cache = MemoryCache(max_size=8192, default_ttl=120.0)

# Cache de dados de usuário para enriquecimento do token no login
# Chave: user_id → valor: dict com roles, permissions, rbac, abac, etc.
user_enrichment_cache = MemoryCache(max_size=512, default_ttl=300.0)

# Cache de métricas do sistema (psutil é caro)
# Chave: "metrics" → valor: dict completo
metrics_cache = MemoryCache(max_size=4, default_ttl=5.0)

# Cache de KPIs do banco (COUNT queries)
# Chave: "db_kpis" → valor: dict
db_kpis_cache = MemoryCache(max_size=4, default_ttl=10.0)

# Cache de settings do banco
# Chave: "settings" → valor: SettingsOutputDTO.__dict__
settings_cache = MemoryCache(max_size=4, default_ttl=60.0)


def invalidate_user(user_id: str) -> None:
    """Invalida todos os caches relacionados a um usuário."""
    user_enrichment_cache.delete(user_id)
    token_cache.delete_prefix(f"uid:{user_id}:")


def invalidate_settings() -> None:
    settings_cache.clear()


def invalidate_metrics() -> None:
    metrics_cache.clear()
    db_kpis_cache.clear()


def cache_stats() -> dict:
    return {
        "token":           token_cache.stats(),
        "blacklist":       blacklist_cache.stats(),
        "user_enrichment": user_enrichment_cache.stats(),
        "metrics":         metrics_cache.stats(),
        "db_kpis":         db_kpis_cache.stats(),
        "settings":        settings_cache.stats(),
    }
