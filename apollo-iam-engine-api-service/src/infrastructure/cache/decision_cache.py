"""
decision_cache.py
Cache de decisão de policy — TTL por policy, multi-tenant, in-memory.
Chave: hash(tenant_id + subject_id + action + resource)
O2 Data Solutions
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any


@dataclass
class _DecisionEntry:
    allowed: bool
    effect: str | None
    matched_policy: str | None
    reason: str
    expires_at: float

    @property
    def alive(self) -> bool:
        return time.monotonic() < self.expires_at


class DecisionCache:
    """
    Cache de decisões de policy com TTL configurável por policy.
    Thread-safe. LRU eviction quando max_size excedido.
    """

    def __init__(self, max_size: int = 8192, default_ttl: float = 60.0):
        self._max_size   = max_size
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, _DecisionEntry] = OrderedDict()
        self._lock   = threading.Lock()
        self._hits   = 0
        self._misses = 0
        # TTL por policy_id (sobrescreve default)
        self._policy_ttls: dict[str, float] = {}

    # ── chave de cache ────────────────────────────────────────────────────────

    @staticmethod
    def make_key(
        tenant_id: str | None,
        subject_id: str,
        action: str,
        resource: str,
        subject: dict | None = None,
    ) -> str:
        """
        Chave de cache que inclui o contexto completo relevante.
        Problema anterior: ignorava roles/attributes do subject — podia retornar
        decisao errada para subjects diferentes com mesmo ID mas atributos distintos.
        Solucao: hash(tenant:subject_id:action:resource:subject_canonical)
        """
        # serializa subject de forma deterministica (sorted keys)
        subject_str = ""
        if subject:
            try:
                subject_str = json.dumps(subject, sort_keys=True, default=str)
            except Exception:
                subject_str = str(sorted(subject.items()) if subject else "")
        raw = f"{tenant_id or ''}:{subject_id}:{action}:{resource}:{subject_str}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # ── TTL por policy ────────────────────────────────────────────────────────

    def set_policy_ttl(self, policy_id: str, ttl: float) -> None:
        self._policy_ttls[policy_id] = ttl

    def _ttl_for(self, policy_id: str | None) -> float:
        if policy_id and policy_id in self._policy_ttls:
            return self._policy_ttls[policy_id]
        return self._default_ttl

    # ── operações ─────────────────────────────────────────────────────────────

    def get(
        self,
        tenant_id: str | None,
        subject_id: str,
        action: str,
        resource: str,
        subject: dict | None = None,
    ) -> _DecisionEntry | None:
        key = self.make_key(tenant_id, subject_id, action, resource, subject)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if not entry.alive:
                del self._store[key]
                self._misses += 1
                return None
            self._store.move_to_end(key)
            self._hits += 1
            return entry

    def set(
        self,
        tenant_id: str | None,
        subject_id: str,
        action: str,
        resource: str,
        allowed: bool,
        effect: str | None,
        matched_policy: str | None,
        reason: str,
        ttl: float | None = None,
        subject: dict | None = None,
    ) -> None:
        key = self.make_key(tenant_id, subject_id, action, resource, subject)
        effective_ttl = ttl if ttl is not None else self._ttl_for(matched_policy)
        entry = _DecisionEntry(
            allowed=allowed,
            effect=effect,
            matched_policy=matched_policy,
            reason=reason,
            expires_at=time.monotonic() + effective_ttl,
        )
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = entry
            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def invalidate_tenant(self, tenant_id: str) -> int:
        """Remove todas as decisões de um tenant."""
        prefix = hashlib.sha256(f"{tenant_id}:".encode()).hexdigest()[:8]
        # Não podemos filtrar por prefixo de hash — invalidamos tudo do tenant
        # via varredura (raro em produção; use com moderação)
        with self._lock:
            keys = list(self._store.keys())
            removed = 0
            for k in keys:
                e = self._store[k]
                # Não temos tenant_id na entry — invalidação total por segurança
                del self._store[k]
                removed += 1
            return removed

    def invalidate_subject(self, subject_id: str) -> None:
        """Invalida todas as decisões de um sujeito (usuário)."""
        # Como a chave é hash, precisamos varrer — aceitável para invalidação pontual
        with self._lock:
            self._store.clear()

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def purge_expired(self) -> int:
        with self._lock:
            expired = [k for k, e in self._store.items() if not e.alive]
            for k in expired:
                del self._store[k]
            return len(expired)

    def stats(self) -> dict:
        with self._lock:
            total = self._hits + self._misses
            return {
                "size":        len(self._store),
                "max_size":    self._max_size,
                "hits":        self._hits,
                "misses":      self._misses,
                "hit_rate":    round(self._hits / total, 4) if total else 0.0,
                "default_ttl": self._default_ttl,
            }


# ── singleton global ──────────────────────────────────────────────────────────
decision_cache = DecisionCache(max_size=8192, default_ttl=60.0)
