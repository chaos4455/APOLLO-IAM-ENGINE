"""
login.py
LoginUseCase com cache em memória para enriquecimento do token (RBAC/ABAC).
O2 Data Solutions
"""
from __future__ import annotations
from src.application.dtos.auth_dto import LoginInputDTO, TokenOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.ports.token_service import TokenService
from src.domain.ports.audit_logger import AuditLogger
from src.domain.value_objects.token_payload import TokenPayload
from src.domain.entities.audit_log import AuditLog
from src.domain.exceptions.auth_exceptions import InvalidCredentialsError, InactiveUserError
from src.infrastructure.config.settings import get_settings
import uuid

settings = get_settings()


def _enrich_from_db(db, user) -> dict:
    """
    Carrega roles, permissions, RBAC e ABAC do usuário a partir do banco.
    Retorna dict com todos os campos de enriquecimento.
    """
    from src.infrastructure.database.models.user_type_model import UserTypeModel
    from src.infrastructure.database.models.user_level_model import UserLevelModel
    from src.infrastructure.database.models.group_model import GroupModel
    from src.infrastructure.database.models.role_model import RoleModel
    from src.infrastructure.database.models.custom_entity_model import (
        UserCustomEntityModel, CustomEntityValueModel,
    )
    from src.infrastructure.database.models.user_model import user_rbac_values
    from src.infrastructure.database.models.rbac_attribute_model import RbacAttributeModel

    user_type_name = None
    user_level_name = None
    user_level_rank = 0
    permissions: list[str] = []
    group_name = None

    if user.type_id:
        t = db.query(UserTypeModel).filter_by(id=user.type_id).first()
        user_type_name = t.name if t else None

    if user.level_id:
        lv = db.query(UserLevelModel).filter_by(id=user.level_id).first()
        if lv:
            user_level_name = lv.name
            user_level_rank = lv.rank

    if user.group_id:
        g = db.query(GroupModel).filter_by(id=user.group_id).first()
        group_name = g.name if g else None

    # permissões de todas as roles do usuário
    for role_name in user.roles:
        rm = db.query(RoleModel).filter_by(name=role_name).first()
        if rm:
            for p in rm.permissions:
                pname = f"{p.resource}:{p.action}"
                if pname not in permissions:
                    permissions.append(pname)

    # RBAC attributes (key → value)
    rbac_rows = (
        db.query(user_rbac_values.c.value, RbacAttributeModel.key)
        .join(RbacAttributeModel,
              user_rbac_values.c.attribute_id == RbacAttributeModel.id)
        .filter(user_rbac_values.c.user_id == user.id)
        .all()
    )
    rbac_dict: dict = {key: value for value, key in rbac_rows}

    # ABAC — custom entities + rbac + type + level + group
    abac: dict = dict(rbac_dict)
    custom_rows = db.query(UserCustomEntityModel).filter_by(user_id=user.id).all()
    for cr in custom_rows:
        val = db.query(CustomEntityValueModel).filter_by(id=cr.entity_value_id).first()
        if val:
            abac[cr.entity_type_slug] = val.name
    if user_type_name:
        abac["user_type"] = user_type_name
    if user_level_name:
        abac["user_level"] = user_level_name
        abac["user_level_rank"] = user_level_rank
    if group_name:
        abac["group"] = group_name

    return {
        "user_type_name":  user_type_name,
        "user_level_name": user_level_name,
        "user_level_rank": user_level_rank,
        "permissions":     permissions,
        "group_name":      group_name,
        "rbac_dict":       rbac_dict,
        "abac":            abac,
    }


class LoginUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher,
                 tokens: TokenService, audit: AuditLogger, db=None):
        self._users = users
        self._hasher = hasher
        self._tokens = tokens
        self._audit = audit
        self._db = db

    def execute(self, dto: LoginInputDTO) -> TokenOutputDTO:
        user = (self._users.find_by_username(dto.username)
                or self._users.find_by_email(dto.username))
        if not user or not self._hasher.verify(dto.password, user.hashed_password):
            self._audit.log(AuditLog(
                id=str(uuid.uuid4()), actor=dto.username, action="login_failed",
                resource="auth", detail="Invalid credentials", ip_address=dto.ip_address,
                status="failure",
            ))
            raise InvalidCredentialsError("Credenciais invalidas.")
        if not user.is_active:
            raise InactiveUserError("Usuario inativo.")

        user_type_name = None
        user_level_name = None
        user_level_rank = 0
        permissions: list[str] = []
        group_name = None
        rbac_dict: dict = {}
        abac: dict = {}

        if self._db:
            from src.infrastructure.cache.memory_cache import user_enrichment_cache

            cached = user_enrichment_cache.get(user.id)
            if cached is not None:
                enriched = cached
            else:
                enriched = _enrich_from_db(self._db, user)
                # TTL de 5 minutos — dados de roles/RBAC mudam raramente
                user_enrichment_cache.set(user.id, enriched, ttl=300.0)

            user_type_name  = enriched["user_type_name"]
            user_level_name = enriched["user_level_name"]
            user_level_rank = enriched["user_level_rank"]
            permissions     = enriched["permissions"]
            group_name      = enriched["group_name"]
            rbac_dict       = enriched["rbac_dict"]
            abac            = enriched["abac"]
            user.rbac_attributes = rbac_dict

        payload = TokenPayload(
            sub=user.username,
            user_id=user.id,
            is_superuser=user.is_superuser,
            roles=user.roles,
            permissions=permissions,
            group=group_name,
            group_id=user.group_id,
            user_type=user_type_name,
            user_level=user_level_name,
            user_level_rank=user_level_rank,
            rbac=user.rbac_attributes,
            abac=abac,
        )
        access = self._tokens.create_access_token(payload)
        refresh = self._tokens.create_refresh_token(payload)
        self._audit.log(AuditLog(
            id=str(uuid.uuid4()), actor=user.username, action="login_success",
            resource="auth", ip_address=dto.ip_address,
        ))
        return TokenOutputDTO(
            access_token=access, refresh_token=refresh,
            expires_in=settings.access_token_expire_minutes * 60,
        )
