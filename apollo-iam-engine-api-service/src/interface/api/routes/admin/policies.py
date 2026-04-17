"""
policies.py
Rotas admin para gerenciamento e avaliação de policies Apollo DSL v2.
Novidades: scope, subject_id, inherits, /explain, /evaluate com templating.
O2 Data Solutions
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.application.services.policy_service import PolicyService
from src.infrastructure.database.connection import get_db
from src.interface.api.dependencies import get_current_user
from src.domain.value_objects.token_payload import TokenPayload
from src.infrastructure.logging.event_logger import query_decisions

router = APIRouter(prefix="/admin/policies", tags=["Policies DSL"])


# ── schemas ───────────────────────────────────────────────────────────────────

class PolicyConditionSchema(BaseModel):
    field: str
    op: str
    value: Any = None   # suporta {{template}}


class PolicyCreateRequest(BaseModel):
    id: Optional[str] = None
    name: str
    description: str = ""
    version: str = "2.0"
    tenant_id: Optional[str] = None
    effect: str = "allow"
    priority: int = 100
    actions: list[str] = ["*"]
    resources: list[str] = ["*"]
    conditions: list[PolicyConditionSchema] = []
    condition_logic: str = "AND"
    enabled: bool = True
    # v2: composition
    scope: str = "tenant"                   # "global" | "tenant" | "user"
    subject_id: Optional[str] = None        # scope=user: ID do sujeito
    inherits: list[str] = []                # IDs de policies pai


class PolicyEvalRequest(BaseModel):
    subject: dict[str, Any]
    action: str
    resource: str
    tenant_id: Optional[str] = None
    subject_id: str = ""
    use_cache: bool = True


class PolicyExplainRequest(BaseModel):
    """Mesmo payload do evaluate, mas retorna rastreamento completo."""
    subject: dict[str, Any]
    action: str
    resource: str
    tenant_id: Optional[str] = None
    subject_id: str = ""


class PolicyRawRequest(BaseModel):
    format: str = "json"   # "json" | "yaml"
    content: str


# ── rotas ─────────────────────────────────────────────────────────────────────

def _require_super(current_user: TokenPayload):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Apenas superusuários podem gerenciar policies.")


@router.post("/", status_code=201, summary="Criar policy (JSON estruturado)")
async def create_policy(
    body: PolicyCreateRequest,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    _require_super(current_user)
    return PolicyService(db).create_policy(body.model_dump())


@router.post("/raw", status_code=201, summary="Criar policy via JSON/YAML raw string")
async def create_policy_raw(
    body: PolicyRawRequest,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    _require_super(current_user)
    svc = PolicyService(db)
    try:
        if body.format == "yaml":
            return svc.create_from_yaml(body.content)
        return svc.create_from_json(body.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao parsear policy: {e}")


@router.get("/", summary="Listar policies")
async def list_policies(
    tenant_id: Optional[str] = None,
    scope: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return PolicyService(db).list_policies(tenant_id=tenant_id, scope=scope)


@router.get("/cache/stats", summary="Stats do cache de decisão")
async def cache_stats(
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    return PolicyService(db).cache_stats()


@router.get("/decisions/audit", summary="Consultar audit trail de decisões de policy")
async def audit_decisions(
    tenant_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    decision: Optional[str] = None,   # allow | deny | no_match
    action: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Retorna o histórico auditável de todas as decisões de policy.
    Filtrável por tenant_id, subject_id, decision (allow/deny/no_match), action.
    """
    return query_decisions(
        tenant_id=tenant_id,
        subject_id=subject_id,
        decision=decision,
        action=action,
        limit=min(limit, 500),
        offset=offset,
    )


@router.get("/{policy_id}", summary="Obter policy por ID")
async def get_policy(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    p = PolicyService(db).get_policy(policy_id)
    if not p:
        raise HTTPException(status_code=404, detail="Policy não encontrada.")
    return p


@router.delete("/{policy_id}", status_code=204, summary="Remover policy")
async def delete_policy(
    policy_id: str,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    _require_super(current_user)
    if not PolicyService(db).delete_policy(policy_id):
        raise HTTPException(status_code=404, detail="Policy não encontrada.")


@router.patch("/{policy_id}/toggle", summary="Ativar/desativar policy")
async def toggle_policy(
    policy_id: str,
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    _require_super(current_user)
    if not PolicyService(db).toggle_policy(policy_id, enabled):
        raise HTTPException(status_code=404, detail="Policy não encontrada.")
    return {"policy_id": policy_id, "enabled": enabled}


@router.post("/evaluate", summary="Avaliar policy para um contexto (com templating + hierarquia)")
async def evaluate_policy(
    body: PolicyEvalRequest,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    svc    = PolicyService(db)
    result = svc.evaluate(
        subject=body.subject,
        action=body.action,
        resource=body.resource,
        tenant_id=body.tenant_id,
        subject_id=body.subject_id,
        use_cache=body.use_cache,
        actor=current_user.sub,
    )
    return {
        "decision":          result.decision,
        "allowed":           result.allowed,
        "effect":            result.effect.value if result.effect else None,
        "matched_policy":    result.matched_policy,
        "matched_rule":      result.matched_rule,
        "reason":            result.reason,
        "failing_condition": result.failing_condition,
        "composition_chain": result.composition_chain,
    }


@router.post("/explain", summary="Explicação detalhada da avaliação (debug/audit)")
async def explain_policy(
    body: PolicyExplainRequest,
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    """
    Retorna rastreamento completo: cada policy testada, por que passou/falhou,
    valores resolvidos de templates, failing_condition, chain de composição.
    """
    return PolicyService(db).explain(
        subject=body.subject,
        action=body.action,
        resource=body.resource,
        tenant_id=body.tenant_id,
        subject_id=body.subject_id,
    )


@router.post("/reload", summary="Recarregar policies do banco no engine")
async def reload_policies(
    db: Session = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user),
):
    _require_super(current_user)
    count = PolicyService(db).reload_from_db()
    return {"loaded": count}
