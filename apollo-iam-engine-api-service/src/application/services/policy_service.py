"""
policy_service.py
Serviço de gerenciamento e avaliação de policies Apollo DSL v2.
Integra PolicyEngine + DecisionCache + persistência SQLite.
Suporta: templating, hierarquia de recursos, policy composition.
O2 Data Solutions
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Any

import yaml
from sqlalchemy.orm import Session

from src.domain.policy.policy_dsl import (
    EvalContext,
    EvalResult,
    Policy,
    PolicyEngine,
    get_policy_engine,
)
from src.infrastructure.cache.decision_cache import decision_cache
from src.infrastructure.database.models.policy_model import PolicyModel
from src.infrastructure.logging.event_logger import log_decision


class PolicyService:
    """
    Orquestra criação, listagem, remoção e avaliação de policies.
    Usa cache de decisão em memória com TTL por policy.
    """

    def __init__(self, db: Session):
        self._db     = db
        self._engine = get_policy_engine()

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def create_policy(self, data: dict) -> dict:
        """Cria policy a partir de dict (JSON ou YAML já parseado)."""
        if "id" not in data or not data["id"]:
            data["id"] = str(uuid.uuid4())

        policy = Policy.from_dict(data)

        model = PolicyModel(
            id=policy.id,
            name=policy.name,
            description=policy.description,
            version=policy.version,
            tenant_id=policy.tenant_id,
            effect=policy.effect.value,
            priority=policy.priority,
            actions=json.dumps(policy.actions),
            resources=json.dumps(policy.resources),
            conditions=json.dumps([
                {"field": c.field, "op": c.op.value, "value": c.value}
                for c in policy.conditions
            ]),
            condition_logic=policy.condition_logic.value,
            enabled=policy.enabled,
            scope=policy.scope.value,
            subject_id=policy.subject_id,
            inherits=json.dumps(policy.inherits),
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        self._engine.load_policy(policy)
        return policy.to_dict()

    def create_from_json(self, raw: str) -> dict:
        return self.create_policy(json.loads(raw))

    def create_from_yaml(self, raw: str) -> dict:
        return self.create_policy(yaml.safe_load(raw))

    def list_policies(self, tenant_id: str | None = None,
                      scope: str | None = None) -> list[dict]:
        q = self._db.query(PolicyModel)
        if tenant_id:
            q = q.filter(
                (PolicyModel.tenant_id == tenant_id) | (PolicyModel.tenant_id.is_(None))
            )
        if scope:
            q = q.filter(PolicyModel.scope == scope)
        return [m.to_policy_dict() for m in q.order_by(PolicyModel.priority).all()]

    def get_policy(self, policy_id: str) -> dict | None:
        m = self._db.query(PolicyModel).filter_by(id=policy_id).first()
        return m.to_policy_dict() if m else None

    def delete_policy(self, policy_id: str) -> bool:
        m = self._db.query(PolicyModel).filter_by(id=policy_id).first()
        if not m:
            return False
        self._db.delete(m)
        self._db.commit()
        self._engine.remove_policy(policy_id)
        decision_cache.clear()
        return True

    def toggle_policy(self, policy_id: str, enabled: bool) -> bool:
        m = self._db.query(PolicyModel).filter_by(id=policy_id).first()
        if not m:
            return False
        m.enabled = enabled
        self._db.commit()
        self._reload_engine()
        decision_cache.clear()
        return True

    # ── avaliação ─────────────────────────────────────────────────────────────

    def evaluate(
        self,
        subject: dict[str, Any],
        action: str,
        resource: str,
        tenant_id: str | None = None,
        subject_id: str = "",
        use_cache: bool = True,
        actor: str = "system",
    ) -> EvalResult:
        t0 = time.perf_counter()

        if use_cache and subject_id:
            cached = decision_cache.get(tenant_id, subject_id, action, resource)
            if cached:
                dur = round((time.perf_counter() - t0) * 1000, 2)
                result = EvalResult(
                    allowed=cached.allowed,
                    effect=None,
                    matched_policy=cached.matched_policy,
                    reason=f"[cache] {cached.reason}",
                    decision="allow" if cached.allowed else "deny",
                )
                log_decision(
                    actor=actor, subject_id=subject_id, tenant_id=tenant_id,
                    action=action, resource=resource,
                    decision=result.decision,
                    matched_policy=cached.matched_policy,
                    reason=result.reason,
                    duration_ms=dur, from_cache=True,
                )
                return result

        ctx    = EvalContext(subject=subject, action=action, resource=resource,
                             tenant_id=tenant_id, subject_id=subject_id)
        result = self._engine.evaluate(ctx)
        dur    = round((time.perf_counter() - t0) * 1000, 2)

        if use_cache and subject_id:
            decision_cache.set(
                tenant_id=tenant_id,
                subject_id=subject_id,
                action=action,
                resource=resource,
                allowed=result.allowed,
                effect=result.effect.value if result.effect else None,
                matched_policy=result.matched_policy,
                reason=result.reason,
            )

        # audit trail de decisão
        log_decision(
            actor=actor, subject_id=subject_id, tenant_id=tenant_id,
            action=action, resource=resource,
            decision=result.decision,
            matched_policy=result.matched_policy,
            matched_rule=result.matched_rule,
            reason=result.reason,
            failing_condition=result.failing_condition,
            chain=result.composition_chain,
            duration_ms=dur, from_cache=False,
        )

        return result

    def explain(
        self,
        subject: dict[str, Any],
        action: str,
        resource: str,
        tenant_id: str | None = None,
        subject_id: str = "",
    ) -> dict:
        """Retorna explicação detalhada da avaliação (debug/audit)."""
        ctx = EvalContext(subject=subject, action=action, resource=resource,
                          tenant_id=tenant_id, subject_id=subject_id)
        return self._engine.explain(ctx)

    # ── reload ────────────────────────────────────────────────────────────────

    def _reload_engine(self) -> None:
        self._engine.clear()
        models = self._db.query(PolicyModel).filter_by(enabled=True).all()
        for m in models:
            self._engine.load_from_dict(m.to_policy_dict())

    def reload_from_db(self) -> int:
        self._reload_engine()
        return len(self._engine.list_policies())

    # ── stats ─────────────────────────────────────────────────────────────────

    def cache_stats(self) -> dict:
        return decision_cache.stats()
