"""
policy_dsl.py
╔══════════════════════════════════════════════════════════════════════════════╗
║  Apollo IAM — Policy DSL Engine v2 (proprietária)                          ║
║  "O Grimório de Jake — versão hardcore do Reino de Ooo"                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Novidades v2:
  ① Variáveis dinâmicas (templating) — {{subject_id}}, {{tenant_id}}, etc.
  ② Hierarquia de recursos — empresa/123/depto/5/cotacao/9 com herança
  ③ Policy composition — scope global → tenant → user (override em cascata)

Formato de policy:
{
  "id": "pol-001",
  "name": "Vendedores podem criar cotações",
  "version": "2.0",
  "tenant_id": "tenant-abc",
  "scope": "tenant",                  # "global" | "tenant" | "user"
  "subject_id": null,                 # para scope=user: ID do sujeito
  "inherits": ["pol-base-global"],    # herança de policies pai
  "effect": "allow",
  "priority": 10,
  "actions": ["cotacao:create"],
  "resources": ["empresa/*/cotacao/*"],
  "conditions": [
    {"field": "resource.owner_id", "op": "eq",  "value": "{{subject_id}}"},
    {"field": "user_level",        "op": "gte",  "value": 3},
    {"field": "roles",             "op": "contains", "value": "vendedor"}
  ],
  "condition_logic": "AND"
}

Variáveis de template disponíveis em "value":
  {{subject_id}}   → ctx.subject_id
  {{tenant_id}}    → ctx.tenant_id
  {{action}}       → ctx.action
  {{resource}}     → ctx.resource
  {{subject.*}}    → qualquer campo de ctx.subject

Operadores (14):
  eq, neq, gt, gte, lt, lte, in, not_in, contains, not_contains,
  starts_with, ends_with, regex, exists, not_exists

O2 Data Solutions
"""
from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import yaml


# ══════════════════════════════════════════════════════════════════════════════
# Enums
# ══════════════════════════════════════════════════════════════════════════════

class Effect(str, Enum):
    ALLOW = "allow"
    DENY  = "deny"

class ConditionLogic(str, Enum):
    AND = "AND"
    OR  = "OR"

class PolicyScope(str, Enum):
    """Nível de composição da policy."""
    GLOBAL = "global"   # aplica a todos os tenants
    TENANT = "tenant"   # aplica a um tenant específico
    USER   = "user"     # aplica a um sujeito específico (override máximo)

class Op(str, Enum):
    EQ          = "eq"
    NEQ         = "neq"
    GT          = "gt"
    GTE         = "gte"
    LT          = "lt"
    LTE         = "lte"
    IN          = "in"
    NOT_IN      = "not_in"
    CONTAINS    = "contains"
    NOT_CONTAINS= "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH   = "ends_with"
    REGEX       = "regex"
    EXISTS      = "exists"
    NOT_EXISTS  = "not_exists"


# ══════════════════════════════════════════════════════════════════════════════
# ① Templating — resolve {{variáveis}} no valor das condições
# ══════════════════════════════════════════════════════════════════════════════

_TEMPLATE_RE = re.compile(r"\{\{([^}]+)\}\}")


def _resolve_template(value: Any, ctx: "EvalContext") -> Any:
    """
    Substitui {{variável}} pelo valor real do contexto.

    Variáveis disponíveis:
      {{subject_id}}   → ctx.subject_id
      {{tenant_id}}    → ctx.tenant_id
      {{action}}       → ctx.action
      {{resource}}     → ctx.resource
      {{subject.X}}    → ctx.subject.get("X")
      {{extra.X}}      → ctx.extra.get("X")

    Se o valor não for string, retorna sem alteração.
    Se a variável não existir no contexto, retorna None.
    """
    if not isinstance(value, str):
        return value

    # substituição simples: valor é só um template → retorna o tipo original
    m = _TEMPLATE_RE.fullmatch(value.strip())
    if m:
        return _resolve_var(m.group(1).strip(), ctx)

    # substituição parcial: template dentro de string maior
    def _replace(match: re.Match) -> str:
        resolved = _resolve_var(match.group(1).strip(), ctx)
        return str(resolved) if resolved is not None else ""

    return _TEMPLATE_RE.sub(_replace, value)


def _resolve_var(var: str, ctx: "EvalContext") -> Any:
    """Resolve uma variável de template para seu valor no contexto."""
    if var == "subject_id":
        return ctx.subject_id
    if var == "tenant_id":
        return ctx.tenant_id
    if var == "action":
        return ctx.action
    if var == "resource":
        return ctx.resource
    if var.startswith("subject."):
        key = var[len("subject."):]
        return ctx.subject.get(key)
    if var.startswith("extra."):
        key = var[len("extra."):]
        return ctx.extra.get(key)
    # fallback: tenta subject direto
    return ctx.subject.get(var)


# ══════════════════════════════════════════════════════════════════════════════
# ② Hierarquia de recursos — parse e match de caminhos hierárquicos
# ══════════════════════════════════════════════════════════════════════════════

def _resource_segments(resource: str) -> list[str]:
    """
    Divide um recurso hierárquico em segmentos.
    "empresa/123/depto/5/cotacao/9" → ["empresa/123", "empresa/123/depto/5", ...]
    Retorna todos os prefixos ancestrais + o próprio recurso.
    """
    parts = resource.strip("/").split("/")
    segments: list[str] = []
    for i in range(1, len(parts) + 1):
        segments.append("/".join(parts[:i]))
    return segments


def _match_resource_hierarchical(patterns: list[str], resource: str) -> bool:
    """
    Match hierárquico: uma pattern pode corresponder ao recurso OU a qualquer
    ancestral dele no caminho.

    Exemplos:
      pattern "empresa/*"         → match "empresa/123/depto/5/cotacao/9" ✓
      pattern "empresa/*/cotacao/*" → match "empresa/123/cotacao/9"       ✓
      pattern "cotacao/*"         → match "empresa/123/cotacao/9"          ✓ (segmento)
      pattern "*"                 → match qualquer coisa                   ✓
    """
    if not patterns:
        return False

    # segmentos do recurso (do mais específico ao mais geral)
    segments = _resource_segments(resource)

    for pattern in patterns:
        if pattern == "*":
            return True
        # match direto (glob padrão)
        if fnmatch.fnmatch(resource, pattern):
            return True
        # match em qualquer segmento ancestral
        for seg in segments:
            if fnmatch.fnmatch(seg, pattern):
                return True
        # match de sufixo: "cotacao/*" deve bater em "empresa/123/cotacao/9"
        # via fnmatch no último par de segmentos
        parts = resource.strip("/").split("/")
        pat_parts = pattern.strip("/").split("/")
        if len(pat_parts) <= len(parts):
            tail = "/".join(parts[len(parts) - len(pat_parts):])
            if fnmatch.fnmatch(tail, pattern):
                return True

    return False


# ══════════════════════════════════════════════════════════════════════════════
# Modelos de dados
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PolicyCondition:
    field: str
    op: Op
    value: Any = None   # pode conter {{template}}

    @classmethod
    def from_dict(cls, d: dict) -> "PolicyCondition":
        return cls(
            field=d["field"],
            op=Op(d["op"]),
            value=d.get("value"),
        )


@dataclass
class Policy:
    id: str
    name: str
    effect: Effect
    actions: list[str]
    resources: list[str]
    conditions: list[PolicyCondition] = field(default_factory=list)
    condition_logic: ConditionLogic = ConditionLogic.AND
    priority: int = 100
    tenant_id: str | None = None
    version: str = "2.0"
    description: str = ""
    enabled: bool = True
    # ── v2: composition ───────────────────────────────────────────────────────
    scope: PolicyScope = PolicyScope.TENANT
    subject_id: str | None = None       # scope=user: ID do sujeito alvo
    inherits: list[str] = field(default_factory=list)  # IDs de policies pai

    @classmethod
    def from_dict(cls, d: dict) -> "Policy":
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            effect=Effect(d.get("effect", "allow")),
            actions=d.get("actions", ["*"]),
            resources=d.get("resources", ["*"]),
            conditions=[PolicyCondition.from_dict(c) for c in d.get("conditions", [])],
            condition_logic=ConditionLogic(d.get("condition_logic", "AND").upper()),
            priority=int(d.get("priority", 100)),
            tenant_id=d.get("tenant_id"),
            version=str(d.get("version", "2.0")),
            description=d.get("description", ""),
            enabled=bool(d.get("enabled", True)),
            scope=PolicyScope(d.get("scope", "tenant")),
            subject_id=d.get("subject_id"),
            inherits=d.get("inherits", []),
        )

    def to_dict(self) -> dict:
        return {
            "id":              self.id,
            "name":            self.name,
            "effect":          self.effect.value,
            "actions":         self.actions,
            "resources":       self.resources,
            "conditions":      [{"field": c.field, "op": c.op.value, "value": c.value}
                                 for c in self.conditions],
            "condition_logic": self.condition_logic.value,
            "priority":        self.priority,
            "tenant_id":       self.tenant_id,
            "version":         self.version,
            "description":     self.description,
            "enabled":         self.enabled,
            "scope":           self.scope.value,
            "subject_id":      self.subject_id,
            "inherits":        self.inherits,
        }


@dataclass
class EvalContext:
    """
    Contexto de avaliação — atributos do sujeito + request.
    subject_id é necessário para templating e cache.
    """
    subject: dict[str, Any]
    action: str
    resource: str
    tenant_id: str | None = None
    subject_id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any:
        """
        Resolve campo do contexto.
        Suporta notação pontilhada: "resource.owner_id" → extra["resource"]["owner_id"]
        """
        if key == "action":
            return self.action
        if key == "resource":
            return self.resource
        if key == "tenant_id":
            return self.tenant_id
        if key == "subject_id":
            return self.subject_id
        # notação pontilhada para campos aninhados
        if "." in key:
            parts = key.split(".", 1)
            root = parts[0]
            rest = parts[1]
            container = self.subject.get(root, self.extra.get(root))
            if isinstance(container, dict):
                return container.get(rest)
            return None
        return self.subject.get(key, self.extra.get(key))


@dataclass
class ConditionTrace:
    """
    Rastreamento de uma condição individual — o coração da explainability.
    Mostra exatamente por que uma condição passou ou falhou.
    """
    field: str
    op: str
    value_template: Any          # valor original (pode ter {{template}})
    value_resolved: Any          # valor após resolução de template
    actual: Any                  # valor real do contexto
    passed: bool
    reason: str                  # ex: "department('sales') eq 'sales' → True"

    def to_dict(self) -> dict:
        return {
            "field":          self.field,
            "op":             self.op,
            "value_template": self.value_template,
            "value_resolved": self.value_resolved,
            "actual":         self.actual,
            "passed":         self.passed,
            "reason":         self.reason,
        }


@dataclass
class PolicyTrace:
    """Rastreamento completo de uma policy durante a avaliação."""
    policy_id: str
    policy_name: str
    scope: str
    effect: str
    priority: int
    skip_reason: str | None          # None = não pulada
    action_match: bool | None
    resource_match: bool | None
    conditions_logic: str | None
    conditions: list[ConditionTrace] = field(default_factory=list)
    conditions_passed: bool | None = None
    applicable: bool = False

    def to_dict(self) -> dict:
        return {
            "policy_id":         self.policy_id,
            "policy_name":       self.policy_name,
            "scope":             self.scope,
            "effect":            self.effect,
            "priority":          self.priority,
            "skip_reason":       self.skip_reason,
            "action_match":      self.action_match,
            "resource_match":    self.resource_match,
            "conditions_logic":  self.conditions_logic,
            "conditions":        [c.to_dict() for c in self.conditions],
            "conditions_passed": self.conditions_passed,
            "applicable":        self.applicable,
        }


@dataclass
class EvalResult:
    allowed: bool
    effect: Effect | None
    matched_policy: str | None
    reason: str
    # v2: rastreabilidade da composição
    composition_chain: list[str] = field(default_factory=list)
    # v3: explainability estruturada
    decision: str = ""           # "allow" | "deny" | "no_match"
    matched_rule: str | None = None   # nome da policy que decidiu
    failing_condition: str | None = None  # condição que causou deny/no_match
    traces: list[PolicyTrace] = field(default_factory=list)

    def __post_init__(self):
        if not self.decision:
            if self.allowed:
                self.decision = "allow"
            elif self.effect == Effect.DENY:
                self.decision = "deny"
            else:
                self.decision = "no_match"

    def to_audit_dict(self) -> dict:
        """Formato compacto para audit log — sem traces completos."""
        return {
            "decision":          self.decision,
            "allowed":           self.allowed,
            "effect":            self.effect.value if self.effect else None,
            "matched_policy":    self.matched_policy,
            "matched_rule":      self.matched_rule,
            "reason":            self.reason,
            "failing_condition": self.failing_condition,
            "chain":             self.composition_chain,
        }

    def to_explain_dict(self) -> dict:
        """Formato completo para /explain — inclui traces por condição."""
        return {
            **self.to_audit_dict(),
            "traces": [t.to_dict() for t in self.traces],
        }

    @classmethod
    def deny(cls, reason: str, policy_id: str | None = None,
             policy_name: str | None = None,
             failing_condition: str | None = None,
             chain: list[str] | None = None,
             traces: list[PolicyTrace] | None = None) -> "EvalResult":
        return cls(
            allowed=False, effect=Effect.DENY, matched_policy=policy_id,
            reason=reason, decision="deny",
            matched_rule=policy_name, failing_condition=failing_condition,
            composition_chain=chain or [], traces=traces or [],
        )

    @classmethod
    def allow(cls, reason: str, policy_id: str | None = None,
              policy_name: str | None = None,
              chain: list[str] | None = None,
              traces: list[PolicyTrace] | None = None) -> "EvalResult":
        return cls(
            allowed=True, effect=Effect.ALLOW, matched_policy=policy_id,
            reason=reason, decision="allow",
            matched_rule=policy_name,
            composition_chain=chain or [], traces=traces or [],
        )

    @classmethod
    def no_match(cls, traces: list[PolicyTrace] | None = None) -> "EvalResult":
        return cls(
            allowed=False, effect=None, matched_policy=None,
            reason="Nenhuma policy aplicável encontrada (default deny).",
            decision="no_match", traces=traces or [],
        )


# ══════════════════════════════════════════════════════════════════════════════
# Avaliador de condições (com templating)
# ══════════════════════════════════════════════════════════════════════════════

def _coerce(a: Any, b: Any) -> tuple[Any, Any]:
    try:
        if isinstance(a, (int, float)):
            return a, type(a)(b)
        if isinstance(b, (int, float)):
            return type(b)(a), b
    except (TypeError, ValueError):
        pass
    return str(a), str(b)


def _eval_condition(cond: PolicyCondition, ctx: EvalContext) -> bool:
    actual   = ctx.get(cond.field)
    # ① resolve template no valor esperado
    expected = _resolve_template(cond.value, ctx)

    if cond.op == Op.EXISTS:
        return actual is not None
    if cond.op == Op.NOT_EXISTS:
        return actual is None
    if actual is None:
        return False

    op = cond.op
    if op == Op.EQ:
        a, b = _coerce(actual, expected)
        return a == b
    if op == Op.NEQ:
        a, b = _coerce(actual, expected)
        return a != b
    if op in (Op.GT, Op.GTE, Op.LT, Op.LTE):
        try:
            a, b = float(actual), float(expected)
        except (TypeError, ValueError):
            return False
        return {Op.GT: a > b, Op.GTE: a >= b, Op.LT: a < b, Op.LTE: a <= b}[op]
    if op == Op.IN:
        return actual in (expected if isinstance(expected, list) else [expected])
    if op == Op.NOT_IN:
        return actual not in (expected if isinstance(expected, list) else [expected])
    if op == Op.CONTAINS:
        if isinstance(actual, list):
            return expected in actual
        return str(expected) in str(actual)
    if op == Op.NOT_CONTAINS:
        if isinstance(actual, list):
            return expected not in actual
        return str(expected) not in str(actual)
    if op == Op.STARTS_WITH:
        return str(actual).startswith(str(expected))
    if op == Op.ENDS_WITH:
        return str(actual).endswith(str(expected))
    if op == Op.REGEX:
        return bool(re.match(str(expected), str(actual)))
    return False


def _eval_conditions(policy: Policy, ctx: EvalContext) -> bool:
    if not policy.conditions:
        return True
    results = [_eval_condition(c, ctx) for c in policy.conditions]
    if policy.condition_logic == ConditionLogic.AND:
        return all(results)
    return any(results)


def _trace_condition(cond: PolicyCondition, ctx: EvalContext) -> ConditionTrace:
    """
    Avalia uma condição e retorna um ConditionTrace com explicação legível.
    Mostra: field, op, valor template, valor resolvido, valor real, resultado.
    """
    actual   = ctx.get(cond.field)
    resolved = _resolve_template(cond.value, ctx)
    passed   = _eval_condition(cond, ctx)

    # monta reason legível para humanos
    if cond.op in (Op.EXISTS, Op.NOT_EXISTS):
        reason = (
            f"'{cond.field}' {cond.op.value} → "
            f"actual={'<presente>' if actual is not None else '<ausente>'} → "
            f"{'✓' if passed else '✗'}"
        )
    else:
        tmpl_note = f" [template: {cond.value!r}]" if cond.value != resolved else ""
        reason = (
            f"'{cond.field}'({actual!r}) {cond.op.value} {resolved!r}"
            f"{tmpl_note} → {'✓' if passed else '✗'}"
        )

    return ConditionTrace(
        field=cond.field,
        op=cond.op.value,
        value_template=cond.value,
        value_resolved=resolved,
        actual=actual,
        passed=passed,
        reason=reason,
    )


def _trace_conditions(policy: Policy, ctx: EvalContext) -> tuple[bool, list[ConditionTrace]]:
    """Avalia todas as condições e retorna (passed, [ConditionTrace])."""
    if not policy.conditions:
        return True, []
    traces = [_trace_condition(c, ctx) for c in policy.conditions]
    if policy.condition_logic == ConditionLogic.AND:
        passed = all(t.passed for t in traces)
    else:
        passed = any(t.passed for t in traces)
    return passed, traces


def _match_glob(patterns: list[str], value: str) -> bool:
    return any(fnmatch.fnmatch(value, p) or p == "*" for p in patterns)


# ══════════════════════════════════════════════════════════════════════════════
# ③ Policy Composition — herança e override em cascata
# ══════════════════════════════════════════════════════════════════════════════

_SCOPE_ORDER = {
    PolicyScope.GLOBAL: 0,
    PolicyScope.TENANT: 1,
    PolicyScope.USER:   2,
}


def _scope_priority(p: Policy) -> tuple[int, int]:
    """Ordena por scope (global < tenant < user) e depois por priority numérica."""
    return (_SCOPE_ORDER[p.scope], p.priority)


def _resolve_inherited_conditions(
    policy: Policy,
    all_policies: dict[str, Policy],
    visited: set[str] | None = None,
) -> list[PolicyCondition]:
    """
    Resolve condições herdadas recursivamente.
    Retorna condições do pai + condições próprias (filho sobrescreve).
    Detecta ciclos via `visited`.
    """
    if visited is None:
        visited = set()
    if policy.id in visited:
        return list(policy.conditions)
    visited.add(policy.id)

    inherited: list[PolicyCondition] = []
    for parent_id in policy.inherits:
        parent = all_policies.get(parent_id)
        if parent and parent.enabled:
            inherited.extend(
                _resolve_inherited_conditions(parent, all_policies, visited)
            )

    # condições próprias sobrescrevem herdadas (por field)
    own_fields = {c.field for c in policy.conditions}
    merged = [c for c in inherited if c.field not in own_fields]
    merged.extend(policy.conditions)
    return merged


# ══════════════════════════════════════════════════════════════════════════════
# Engine principal
# ══════════════════════════════════════════════════════════════════════════════

class PolicyEngine:
    """
    Motor de avaliação de policies Apollo IAM v3.

    Regras de prioridade:
    1. Deny explícito sempre vence Allow.
    2. Scope user > tenant > global (override em cascata).
    3. Entre policies do mesmo scope/efeito, menor priority = maior precedência.
    4. Sem policy aplicável → default deny.
    5. Variáveis {{template}} resolvidas em tempo de avaliação.
    6. Recursos hierárquicos: empresa/*/cotacao/* bate em empresa/123/cotacao/9.
    7. Cada avaliação produz ConditionTrace por condição — explainability nativa.
    """

    def __init__(self):
        self._policies: list[Policy] = []
        self._by_id: dict[str, Policy] = {}

    def load_policy(self, policy: Policy) -> None:
        self._policies = [p for p in self._policies if p.id != policy.id]
        self._policies.append(policy)
        self._by_id[policy.id] = policy
        self._policies.sort(key=_scope_priority)

    def load_from_dict(self, d: dict) -> Policy:
        p = Policy.from_dict(d)
        self.load_policy(p)
        return p

    def load_from_json(self, raw: str) -> Policy:
        return self.load_from_dict(json.loads(raw))

    def load_from_yaml(self, raw: str) -> Policy:
        return self.load_from_dict(yaml.safe_load(raw))

    def load_many(self, policies: list[dict]) -> list[Policy]:
        return [self.load_from_dict(p) for p in policies]

    def remove_policy(self, policy_id: str) -> bool:
        before = len(self._policies)
        self._policies = [p for p in self._policies if p.id != policy_id]
        self._by_id.pop(policy_id, None)
        return len(self._policies) < before

    def clear(self) -> None:
        self._policies.clear()
        self._by_id.clear()

    def list_policies(self, tenant_id: str | None = None) -> list[Policy]:
        if tenant_id is None:
            return list(self._policies)
        return [p for p in self._policies
                if p.tenant_id == tenant_id or p.tenant_id is None]

    def evaluate(self, ctx: EvalContext) -> EvalResult:
        """
        Avalia o contexto. Produz traces por condição para explainability.
        Retorna EvalResult com decision, reason, failing_condition e traces.
        """
        applicable_traces: list[PolicyTrace] = []
        skipped_traces: list[PolicyTrace] = []

        for p in self._policies:
            pt = self._eval_policy(p, ctx)
            if pt.skip_reason:
                skipped_traces.append(pt)
            else:
                applicable_traces.append(pt)

        all_traces = skipped_traces + applicable_traces
        applicable = [t for t in applicable_traces if t.applicable]

        if not applicable:
            return EvalResult.no_match(traces=all_traces)

        chain = [t.policy_id for t in applicable]

        # Deny explícito — prioridade absoluta
        for pt in applicable:
            if pt.effect == "deny":
                failing = self._first_failing(pt)
                return EvalResult.deny(
                    reason=f"Negado pela policy '{pt.policy_name}' "
                           f"(id={pt.policy_id}, scope={pt.scope}).",
                    policy_id=pt.policy_id,
                    policy_name=pt.policy_name,
                    failing_condition=failing,
                    chain=chain,
                    traces=all_traces,
                )

        # Allow — scope mais específico vence
        for pt in applicable:
            if pt.effect == "allow":
                return EvalResult.allow(
                    reason=f"Permitido pela policy '{pt.policy_name}' "
                           f"(id={pt.policy_id}, scope={pt.scope}).",
                    policy_id=pt.policy_id,
                    policy_name=pt.policy_name,
                    chain=chain,
                    traces=all_traces,
                )

        return EvalResult.no_match(traces=all_traces)

    def _eval_policy(self, p: Policy, ctx: EvalContext) -> PolicyTrace:
        """Avalia uma policy e retorna PolicyTrace completo."""
        # filtros de skip
        if not p.enabled:
            return PolicyTrace(p.id, p.name, p.scope.value, p.effect.value,
                               p.priority, skip_reason="disabled",
                               action_match=None, resource_match=None,
                               conditions_logic=None)
        if p.tenant_id is not None and p.tenant_id != ctx.tenant_id:
            return PolicyTrace(p.id, p.name, p.scope.value, p.effect.value,
                               p.priority, skip_reason="tenant_mismatch",
                               action_match=None, resource_match=None,
                               conditions_logic=None)
        if p.scope == PolicyScope.USER and p.subject_id and p.subject_id != ctx.subject_id:
            return PolicyTrace(p.id, p.name, p.scope.value, p.effect.value,
                               p.priority, skip_reason="subject_mismatch",
                               action_match=None, resource_match=None,
                               conditions_logic=None)

        action_ok   = _match_glob(p.actions, ctx.action)
        resource_ok = _match_resource_hierarchical(p.resources, ctx.resource)
        effective   = self._with_inherited_conditions(p)
        cond_passed, cond_traces = _trace_conditions(effective, ctx)
        applicable  = action_ok and resource_ok and cond_passed

        return PolicyTrace(
            policy_id=p.id,
            policy_name=p.name,
            scope=p.scope.value,
            effect=p.effect.value,
            priority=p.priority,
            skip_reason=None,
            action_match=action_ok,
            resource_match=resource_ok,
            conditions_logic=effective.condition_logic.value,
            conditions=cond_traces,
            conditions_passed=cond_passed,
            applicable=applicable,
        )

    @staticmethod
    def _first_failing(pt: PolicyTrace) -> str | None:
        """Retorna a reason da primeira condição que falhou."""
        for ct in pt.conditions:
            if not ct.passed:
                return ct.reason
        return None

    def _with_inherited_conditions(self, policy: Policy) -> Policy:
        if not policy.inherits:
            return policy
        merged_conditions = _resolve_inherited_conditions(policy, self._by_id)
        import copy
        p = copy.copy(policy)
        p.conditions = merged_conditions
        return p

    def evaluate_batch(self, contexts: list[EvalContext]) -> list[EvalResult]:
        return [self.evaluate(ctx) for ctx in contexts]

    def explain(self, ctx: EvalContext) -> dict:
        """
        Retorna explicação estruturada completa — inclui traces por condição,
        valores de template resolvidos, e decisão final.
        """
        result = self.evaluate(ctx)
        return {
            "decision": {
                "decision":          result.decision,
                "allowed":           result.allowed,
                "effect":            result.effect.value if result.effect else None,
                "matched_policy":    result.matched_policy,
                "matched_rule":      result.matched_rule,
                "reason":            result.reason,
                "failing_condition": result.failing_condition,
                "chain":             result.composition_chain,
            },
            "context": {
                "action":     ctx.action,
                "resource":   ctx.resource,
                "tenant_id":  ctx.tenant_id,
                "subject_id": ctx.subject_id,
                "subject":    ctx.subject,
            },
            "traces": [t.to_dict() for t in result.traces],
        }


# ── singleton global ──────────────────────────────────────────────────────────
_global_engine: PolicyEngine | None = None


def get_policy_engine() -> PolicyEngine:
    global _global_engine
    if _global_engine is None:
        _global_engine = PolicyEngine()
    return _global_engine
