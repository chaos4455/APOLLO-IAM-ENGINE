"""
log_hooks.py
Funções de conveniência para logar eventos de negócio do Apollo IAM Engine.
Cada operação (create, update, delete, assign, login, logout…) tem sua função.
"""
from __future__ import annotations
from typing import Any
from src.infrastructure.logging.event_logger import log_event


# ── Auth ──────────────────────────────────────────────────────────────────────

def log_login_success(username: str, ip: str = "", user_id: str = ""):
    log_event("auth.login_success", actor=username, resource="auth",
              resource_id=user_id, detail={"ip": ip})


def log_login_failed(username: str, ip: str = "", reason: str = ""):
    log_event("auth.login_failed", actor=username, resource="auth",
              status="failure", detail={"ip": ip, "reason": reason})


def log_logout(username: str, jti: str = ""):
    log_event("auth.logout", actor=username, resource="auth",
              detail={"jti": jti})


def log_token_refresh(username: str):
    log_event("auth.token_refresh", actor=username, resource="auth")


def log_token_validated(username: str, jti: str = ""):
    log_event("auth.token_validated", actor=username, resource="auth",
              detail={"jti": jti})


def log_token_invalid(reason: str):
    log_event("auth.token_invalid", actor="anonymous", resource="auth",
              status="failure", detail={"reason": reason})


def log_abac_check(actor: str, allowed: bool, reason: str, detail: dict | None = None):
    log_event(
        "auth.abac_check",
        actor=actor, resource="auth/check",
        status="success" if allowed else "failure",
        detail={"allowed": allowed, "reason": reason, **(detail or {})},
    )


# ── Users ─────────────────────────────────────────────────────────────────────

def log_user_created(actor: str, user_id: str, username: str):
    log_event("user.created", actor=actor, resource="users",
              resource_id=user_id, detail={"username": username})


def log_user_updated(actor: str, user_id: str, fields: list[str]):
    log_event("user.updated", actor=actor, resource="users",
              resource_id=user_id, detail={"fields": fields})


def log_user_deleted(actor: str, user_id: str, username: str = ""):
    log_event("user.deleted", actor=actor, resource="users",
              resource_id=user_id, detail={"username": username})


def log_user_toggled(actor: str, user_id: str, new_status: bool):
    log_event("user.status_toggled", actor=actor, resource="users",
              resource_id=user_id, detail={"is_active": new_status})


def log_password_changed(actor: str, user_id: str):
    log_event("user.password_changed", actor=actor, resource="users",
              resource_id=user_id)


def log_password_reset(actor: str, user_id: str):
    log_event("user.password_reset", actor=actor, resource="users",
              resource_id=user_id)


# ── Roles ─────────────────────────────────────────────────────────────────────

def log_role_created(actor: str, role_id: str, name: str):
    log_event("role.created", actor=actor, resource="roles",
              resource_id=role_id, detail={"name": name})


def log_role_updated(actor: str, role_id: str, name: str):
    log_event("role.updated", actor=actor, resource="roles",
              resource_id=role_id, detail={"name": name})


def log_role_deleted(actor: str, role_id: str, name: str = ""):
    log_event("role.deleted", actor=actor, resource="roles",
              resource_id=role_id, detail={"name": name})


def log_role_assigned(actor: str, user_id: str, role_id: str):
    log_event("role.assigned_to_user", actor=actor, resource="roles",
              resource_id=role_id, detail={"user_id": user_id})


def log_role_revoked(actor: str, user_id: str, role_id: str):
    log_event("role.revoked_from_user", actor=actor, resource="roles",
              resource_id=role_id, detail={"user_id": user_id})


# ── Permissions ───────────────────────────────────────────────────────────────

def log_permission_created(actor: str, perm_id: str, name: str):
    log_event("permission.created", actor=actor, resource="permissions",
              resource_id=perm_id, detail={"name": name})


def log_permission_updated(actor: str, perm_id: str, name: str):
    log_event("permission.updated", actor=actor, resource="permissions",
              resource_id=perm_id, detail={"name": name})


def log_permission_deleted(actor: str, perm_id: str, name: str = ""):
    log_event("permission.deleted", actor=actor, resource="permissions",
              resource_id=perm_id, detail={"name": name})


def log_permission_assigned_to_role(actor: str, perm_id: str, role_id: str):
    log_event("permission.assigned_to_role", actor=actor, resource="permissions",
              resource_id=perm_id, detail={"role_id": role_id})


# ── Groups ────────────────────────────────────────────────────────────────────

def log_group_created(actor: str, group_id: str, name: str):
    log_event("group.created", actor=actor, resource="groups",
              resource_id=group_id, detail={"name": name})


def log_group_updated(actor: str, group_id: str, name: str):
    log_event("group.updated", actor=actor, resource="groups",
              resource_id=group_id, detail={"name": name})


def log_group_deleted(actor: str, group_id: str, name: str = ""):
    log_event("group.deleted", actor=actor, resource="groups",
              resource_id=group_id, detail={"name": name})


def log_user_assigned_to_group(actor: str, user_id: str, group_id: str):
    log_event("group.user_assigned", actor=actor, resource="groups",
              resource_id=group_id, detail={"user_id": user_id})


# ── RBAC Attributes ───────────────────────────────────────────────────────────

def log_rbac_attr_created(actor: str, attr_id: str, key: str):
    log_event("rbac.attribute_created", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, detail={"key": key})


def log_rbac_attr_updated(actor: str, attr_id: str, key: str):
    log_event("rbac.attribute_updated", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, detail={"key": key})


def log_rbac_attr_deleted(actor: str, attr_id: str, key: str = ""):
    log_event("rbac.attribute_deleted", actor=actor, resource="rbac_attributes",
              resource_id=attr_id, detail={"key": key})


def log_rbac_attr_assigned(actor: str, user_id: str, key: str, value: str):
    log_event("rbac.attribute_assigned_to_user", actor=actor, resource="rbac_attributes",
              resource_id=user_id, detail={"key": key, "value": value})


# ── Custom Entities (ABAC) ────────────────────────────────────────────────────

def log_entity_type_created(actor: str, entity_id: str, slug: str):
    log_event("entity.type_created", actor=actor, resource="custom_entities",
              resource_id=entity_id, detail={"slug": slug})


def log_entity_type_updated(actor: str, slug: str):
    log_event("entity.type_updated", actor=actor, resource="custom_entities",
              resource_id=slug)


def log_entity_type_deleted(actor: str, slug: str):
    log_event("entity.type_deleted", actor=actor, resource="custom_entities",
              resource_id=slug)


def log_entity_value_created(actor: str, value_id: str, slug: str, name: str):
    log_event("entity.value_created", actor=actor, resource="custom_entities",
              resource_id=value_id, detail={"slug": slug, "name": name})


def log_entity_value_updated(actor: str, value_id: str, slug: str):
    log_event("entity.value_updated", actor=actor, resource="custom_entities",
              resource_id=value_id, detail={"slug": slug})


def log_entity_value_deleted(actor: str, value_id: str, slug: str):
    log_event("entity.value_deleted", actor=actor, resource="custom_entities",
              resource_id=value_id, detail={"slug": slug})


def log_entity_assigned_to_user(actor: str, user_id: str, slug: str, value_name: str):
    log_event("entity.assigned_to_user", actor=actor, resource="custom_entities",
              resource_id=user_id, detail={"slug": slug, "value": value_name})


def log_entity_unassigned_from_user(actor: str, user_id: str, slug: str):
    log_event("entity.unassigned_from_user", actor=actor, resource="custom_entities",
              resource_id=user_id, detail={"slug": slug})


# ── User Types / Levels ───────────────────────────────────────────────────────

def log_user_type_created(actor: str, type_id: str, name: str):
    log_event("user_type.created", actor=actor, resource="user_types",
              resource_id=type_id, detail={"name": name})


def log_user_type_deleted(actor: str, type_id: str, name: str = ""):
    log_event("user_type.deleted", actor=actor, resource="user_types",
              resource_id=type_id, detail={"name": name})


def log_user_level_created(actor: str, level_id: str, name: str, rank: int):
    log_event("user_level.created", actor=actor, resource="user_levels",
              resource_id=level_id, detail={"name": name, "rank": rank})


def log_user_level_deleted(actor: str, level_id: str, name: str = ""):
    log_event("user_level.deleted", actor=actor, resource="user_levels",
              resource_id=level_id, detail={"name": name})


# ── Settings ──────────────────────────────────────────────────────────────────

def log_settings_read(actor: str):
    log_event("settings.read", actor=actor, resource="settings")


def log_settings_updated(actor: str, fields: dict[str, Any]):
    log_event("settings.updated", actor=actor, resource="settings",
              detail={"fields": fields})


# ── Audit Logs ────────────────────────────────────────────────────────────────

def log_audit_read(actor: str, count: int):
    log_event("audit.read", actor=actor, resource="audit_logs",
              detail={"count": count})
