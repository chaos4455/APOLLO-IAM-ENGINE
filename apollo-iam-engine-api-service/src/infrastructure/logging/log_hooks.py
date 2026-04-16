"""
log_hooks.py
Funções de conveniência para logar eventos de negócio do Apollo IAM Engine.
Cada operação tem sua função tipada com suporte a tenant_id, session_id e duration_ms.
"""
from __future__ import annotations
from typing import Any
from src.infrastructure.logging.event_logger import log_event


# ── Auth ──────────────────────────────────────────────────────────────────────

def log_login_success(username: str, ip: str = "", user_id: str = "",
                      tenant_id: str | None = None, duration_ms: float | None = None):
    log_event("auth.login_success", actor=username, resource="auth",
              resource_id=user_id, tenant_id=tenant_id, duration_ms=duration_ms,
              tags=["auth", "login", "success"],
              detail={"ip": ip})


def log_login_failed(username: str, ip: str = "", reason: str = "",
                     tenant_id: str | None = None):
    log_event("auth.login_failed", actor=username, resource="auth",
              status="failure", tenant_id=tenant_id,
              tags=["auth", "login", "failure"],
              detail={"ip": ip, "reason": reason})


def log_logout(username: str, jti: str = "", tenant_id: str | None = None):
    log_event("auth.logout", actor=username, resource="auth",
              tenant_id=tenant_id, tags=["auth", "logout"],
              detail={"jti": jti})


def log_token_refresh(username: str, tenant_id: str | None = None):
    log_event("auth.token_refresh", actor=username, resource="auth",
              tenant_id=tenant_id, tags=["auth", "refresh"])


def log_token_validated(username: str, jti: str = "", tenant_id: str | None = None,
                        duration_ms: float | None = None):
    log_event("auth.token_validated", actor=username, resource="auth",
              tenant_id=tenant_id, duration_ms=duration_ms,
              tags=["auth", "validate"],
              detail={"jti": jti})


def log_token_invalid(reason: str, tenant_id: str | None = None):
    log_event("auth.token_invalid", actor="anonymous", resource="auth",
              status="failure", tenant_id=tenant_id,
              tags=["auth", "failure"],
              detail={"reason": reason})


def log_abac_check(actor: str, allowed: bool, reason: str,
                   detail: dict | None = None,
                   tenant_id: str | None = None,
                   duration_ms: float | None = None):
    log_event(
        "auth.abac_check",
        actor=actor, resource="auth/check",
        status="success" if allowed else "failure",
        tenant_id=tenant_id, duration_ms=duration_ms,
        tags=["auth", "check", "rbac", "abac", "success" if allowed else "failure"],
        detail={"allowed": allowed, "reason": reason, **(detail or {})},
    )


# ── Policy DSL ────────────────────────────────────────────────────────────────

def log_policy_created(actor: str, policy_id: str, name: str,
                       effect: str = "allow", tenant_id: str | None = None):
    log_event("policy.created", actor=actor, resource="policies",
              resource_id=policy_id, tenant_id=tenant_id,
              tags=["policy", "dsl", effect],
              detail={"name": name, "effect": effect})


def log_policy_deleted(actor: str, policy_id: str, name: str = "",
                       tenant_id: str | None = None):
    log_event("policy.deleted", actor=actor, resource="policies",
              resource_id=policy_id, tenant_id=tenant_id,
              tags=["policy", "dsl"],
              detail={"name": name})


def log_policy_toggled(actor: str, policy_id: str, enabled: bool,
                       tenant_id: str | None = None):
    log_event("policy.toggled", actor=actor, resource="policies",
              resource_id=policy_id, tenant_id=tenant_id,
              tags=["policy", "dsl"],
              detail={"enabled": enabled})


def log_policy_evaluated(actor: str, policy_id: str | None, allowed: bool,
                         action: str, resource: str,
                         tenant_id: str | None = None,
                         duration_ms: float | None = None):
    log_event(
        "policy.evaluated",
        actor=actor, resource=resource,
        resource_id=policy_id, tenant_id=tenant_id,
        status="success" if allowed else "failure",
        duration_ms=duration_ms,
        tags=["policy", "eval", "allow" if allowed else "deny"],
        detail={"allowed": allowed, "action": action, "matched_policy": policy_id},
    )


def log_policy_reloaded(actor: str, count: int):
    log_event("policy.engine_reloaded", actor=actor, resource="policies",
              tags=["policy", "engine"],
              detail={"loaded_count": count})


def log_decision_cache_hit(actor: str, action: str, resource: str,
                           tenant_id: str | None = None):
    log_event("policy.cache_hit", actor=actor, resource=resource,
              tenant_id=tenant_id, tags=["policy", "cache", "hit"],
              detail={"action": action})


def log_decision_audit(
    actor: str,
    subject_id: str,
    tenant_id: str | None,
    action: str,
    resource: str,
    decision: str,
    matched_policy: str | None = None,
    matched_rule: str | None = None,
    reason: str = "",
    failing_condition: str | None = None,
    chain: list[str] | None = None,
    duration_ms: float | None = None,
    from_cache: bool = False,
) -> str:
    """
    Registra uma decisão de policy no audit trail dedicado (decision_audit).
    Wrapper tipado sobre event_logger.log_decision.
    Retorna o uid da entrada criada.
    """
    from src.infrastructure.logging.event_logger import log_decision
    return log_decision(
        actor=actor, subject_id=subject_id, tenant_id=tenant_id,
        action=action, resource=resource, decision=decision,
        matched_policy=matched_policy, matched_rule=matched_rule,
        reason=reason, failing_condition=failing_condition,
        chain=chain, duration_ms=duration_ms, from_cache=from_cache,
    )


# ── Users ─────────────────────────────────────────────────────────────────────

def log_user_created(actor: str, user_id: str, username: str,
                     tenant_id: str | None = None):
    log_event("user.created", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "create"],
              detail={"username": username})


def log_user_updated(actor: str, user_id: str, fields: list[str],
                     tenant_id: str | None = None):
    log_event("user.updated", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "update"],
              detail={"fields": fields})


def log_user_deleted(actor: str, user_id: str, username: str = "",
                     tenant_id: str | None = None):
    log_event("user.deleted", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "delete"],
              detail={"username": username})


def log_user_toggled(actor: str, user_id: str, new_status: bool,
                     tenant_id: str | None = None):
    log_event("user.status_toggled", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "toggle"],
              detail={"is_active": new_status})


def log_password_changed(actor: str, user_id: str, tenant_id: str | None = None):
    log_event("user.password_changed", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "password"])


def log_password_reset(actor: str, user_id: str, tenant_id: str | None = None):
    log_event("user.password_reset", actor=actor, resource="users",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["user", "password", "reset"])


# ── Roles ─────────────────────────────────────────────────────────────────────

def log_role_created(actor: str, role_id: str, name: str,
                     tenant_id: str | None = None):
    log_event("role.created", actor=actor, resource="roles",
              resource_id=role_id, tenant_id=tenant_id,
              tags=["role", "rbac", "create"],
              detail={"name": name})


def log_role_updated(actor: str, role_id: str, name: str,
                     tenant_id: str | None = None):
    log_event("role.updated", actor=actor, resource="roles",
              resource_id=role_id, tenant_id=tenant_id,
              tags=["role", "rbac", "update"],
              detail={"name": name})


def log_role_deleted(actor: str, role_id: str, name: str = "",
                     tenant_id: str | None = None):
    log_event("role.deleted", actor=actor, resource="roles",
              resource_id=role_id, tenant_id=tenant_id,
              tags=["role", "rbac", "delete"],
              detail={"name": name})


def log_role_assigned(actor: str, user_id: str, role_id: str,
                      tenant_id: str | None = None):
    log_event("role.assigned_to_user", actor=actor, resource="roles",
              resource_id=role_id, tenant_id=tenant_id,
              tags=["role", "rbac", "assign"],
              detail={"user_id": user_id})


def log_role_revoked(actor: str, user_id: str, role_id: str,
                     tenant_id: str | None = None):
    log_event("role.revoked_from_user", actor=actor, resource="roles",
              resource_id=role_id, tenant_id=tenant_id,
              tags=["role", "rbac", "revoke"],
              detail={"user_id": user_id})


# ── Permissions ───────────────────────────────────────────────────────────────

def log_permission_created(actor: str, perm_id: str, name: str,
                           tenant_id: str | None = None):
    log_event("permission.created", actor=actor, resource="permissions",
              resource_id=perm_id, tenant_id=tenant_id,
              tags=["permission", "rbac", "create"],
              detail={"name": name})


def log_permission_updated(actor: str, perm_id: str, name: str,
                           tenant_id: str | None = None):
    log_event("permission.updated", actor=actor, resource="permissions",
              resource_id=perm_id, tenant_id=tenant_id,
              tags=["permission", "rbac", "update"],
              detail={"name": name})


def log_permission_deleted(actor: str, perm_id: str, name: str = "",
                           tenant_id: str | None = None):
    log_event("permission.deleted", actor=actor, resource="permissions",
              resource_id=perm_id, tenant_id=tenant_id,
              tags=["permission", "rbac", "delete"],
              detail={"name": name})


def log_permission_assigned_to_role(actor: str, perm_id: str, role_id: str,
                                    tenant_id: str | None = None):
    log_event("permission.assigned_to_role", actor=actor, resource="permissions",
              resource_id=perm_id, tenant_id=tenant_id,
              tags=["permission", "rbac", "assign"],
              detail={"role_id": role_id})


# ── Groups ────────────────────────────────────────────────────────────────────

def log_group_created(actor: str, group_id: str, name: str,
                      tenant_id: str | None = None):
    log_event("group.created", actor=actor, resource="groups",
              resource_id=group_id, tenant_id=tenant_id,
              tags=["group", "create"],
              detail={"name": name})


def log_group_updated(actor: str, group_id: str, name: str,
                      tenant_id: str | None = None):
    log_event("group.updated", actor=actor, resource="groups",
              resource_id=group_id, tenant_id=tenant_id,
              tags=["group", "update"],
              detail={"name": name})


def log_group_deleted(actor: str, group_id: str, name: str = "",
                      tenant_id: str | None = None):
    log_event("group.deleted", actor=actor, resource="groups",
              resource_id=group_id, tenant_id=tenant_id,
              tags=["group", "delete"],
              detail={"name": name})


def log_user_assigned_to_group(actor: str, user_id: str, group_id: str,
                                tenant_id: str | None = None):
    log_event("group.user_assigned", actor=actor, resource="groups",
              resource_id=group_id, tenant_id=tenant_id,
              tags=["group", "assign"],
              detail={"user_id": user_id})


# ── RBAC Attributes ───────────────────────────────────────────────────────────

def log_rbac_attr_created(actor: str, attr_id: str, key: str,
                          tenant_id: str | None = None):
    log_event("rbac.attribute_created", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, tenant_id=tenant_id,
              tags=["rbac", "attribute", "create"],
              detail={"key": key})


def log_rbac_attr_updated(actor: str, attr_id: str, key: str,
                          tenant_id: str | None = None):
    log_event("rbac.attribute_updated", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, tenant_id=tenant_id,
              tags=["rbac", "attribute", "update"],
              detail={"key": key})


def log_rbac_attr_deleted(actor: str, attr_id: str, key: str = "",
                          tenant_id: str | None = None):
    log_event("rbac.attribute_deleted", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, tenant_id=tenant_id,
              tags=["rbac", "attribute", "delete"],
              detail={"key": key})


def log_rbac_attr_assigned(actor: str, user_id: str, key: str, value: str,
                           tenant_id: str | None = None):
    log_event("rbac.attribute_assigned_to_user", actor=actor, resource="rbac_attributes",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["rbac", "attribute", "assign"],
              detail={"key": key, "value": value})


# ── Custom Entities (ABAC) ────────────────────────────────────────────────────

def log_entity_type_created(actor: str, entity_id: str, slug: str,
                            tenant_id: str | None = None):
    log_event("entity.type_created", actor=actor, resource="custom_entities",
              resource_id=entity_id, tenant_id=tenant_id,
              tags=["abac", "entity", "create"],
              detail={"slug": slug})


def log_entity_type_updated(actor: str, slug: str, tenant_id: str | None = None):
    log_event("entity.type_updated", actor=actor, resource="custom_entities",
              resource_id=slug, tenant_id=tenant_id,
              tags=["abac", "entity", "update"])


def log_entity_type_deleted(actor: str, slug: str, tenant_id: str | None = None):
    log_event("entity.type_deleted", actor=actor, resource="custom_entities",
              resource_id=slug, tenant_id=tenant_id,
              tags=["abac", "entity", "delete"])


def log_entity_value_created(actor: str, value_id: str, slug: str, name: str,
                             tenant_id: str | None = None):
    log_event("entity.value_created", actor=actor, resource="custom_entities",
              resource_id=value_id, tenant_id=tenant_id,
              tags=["abac", "entity", "value", "create"],
              detail={"slug": slug, "name": name})


def log_entity_value_updated(actor: str, value_id: str, slug: str,
                             tenant_id: str | None = None):
    log_event("entity.value_updated", actor=actor, resource="custom_entities",
              resource_id=value_id, tenant_id=tenant_id,
              tags=["abac", "entity", "value", "update"],
              detail={"slug": slug})


def log_entity_value_deleted(actor: str, value_id: str, slug: str,
                             tenant_id: str | None = None):
    log_event("entity.value_deleted", actor=actor, resource="custom_entities",
              resource_id=value_id, tenant_id=tenant_id,
              tags=["abac", "entity", "value", "delete"],
              detail={"slug": slug})


def log_entity_assigned_to_user(actor: str, user_id: str, slug: str, value_name: str,
                                tenant_id: str | None = None):
    log_event("entity.assigned_to_user", actor=actor, resource="custom_entities",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["abac", "entity", "assign"],
              detail={"slug": slug, "value": value_name})


def log_entity_unassigned_from_user(actor: str, user_id: str, slug: str,
                                    tenant_id: str | None = None):
    log_event("entity.unassigned_from_user", actor=actor, resource="custom_entities",
              resource_id=user_id, tenant_id=tenant_id,
              tags=["abac", "entity", "unassign"],
              detail={"slug": slug})


# ── User Types / Levels ───────────────────────────────────────────────────────

def log_user_type_created(actor: str, type_id: str, name: str,
                          tenant_id: str | None = None):
    log_event("user_type.created", actor=actor, resource="user_types",
              resource_id=type_id, tenant_id=tenant_id,
              tags=["user_type", "create"],
              detail={"name": name})


def log_user_type_deleted(actor: str, type_id: str, name: str = "",
                          tenant_id: str | None = None):
    log_event("user_type.deleted", actor=actor, resource="user_types",
              resource_id=type_id, tenant_id=tenant_id,
              tags=["user_type", "delete"],
              detail={"name": name})


def log_user_level_created(actor: str, level_id: str, name: str, rank: int,
                           tenant_id: str | None = None):
    log_event("user_level.created", actor=actor, resource="user_levels",
              resource_id=level_id, tenant_id=tenant_id,
              tags=["user_level", "create"],
              detail={"name": name, "rank": rank})


def log_user_level_deleted(actor: str, level_id: str, name: str = "",
                           tenant_id: str | None = None):
    log_event("user_level.deleted", actor=actor, resource="user_levels",
              resource_id=level_id, tenant_id=tenant_id,
              tags=["user_level", "delete"],
              detail={"name": name})


# ── Settings ──────────────────────────────────────────────────────────────────

def log_settings_read(actor: str, tenant_id: str | None = None):
    log_event("settings.read", actor=actor, resource="settings",
              tenant_id=tenant_id, tags=["settings", "read"])


def log_settings_updated(actor: str, fields: dict[str, Any],
                         tenant_id: str | None = None):
    log_event("settings.updated", actor=actor, resource="settings",
              tenant_id=tenant_id, tags=["settings", "update"],
              detail={"fields": fields})


# ── Audit Logs ────────────────────────────────────────────────────────────────

def log_audit_read(actor: str, count: int, tenant_id: str | None = None):
    log_event("audit.read", actor=actor, resource="audit_logs",
              tenant_id=tenant_id, tags=["audit", "read"],
              detail={"count": count})
