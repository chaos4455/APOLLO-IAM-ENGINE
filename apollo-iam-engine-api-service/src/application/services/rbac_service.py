from __future__ import annotations
from sqlalchemy.orm import Session
from src.infrastructure.repositories.role_repository_impl import SqliteRoleRepository
from src.infrastructure.repositories.permission_repository_impl import SqlitePermissionRepository
from src.infrastructure.repositories.group_repository_impl import SqliteGroupRepository
from src.infrastructure.repositories.rbac_attribute_repository_impl import SqliteRbacAttributeRepository
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.list_roles import ListRolesUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.roles.assign_role_to_user import AssignRoleToUserUseCase
from src.application.use_cases.roles.revoke_role_from_user import RevokeRoleFromUserUseCase
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.permissions.list_permissions import ListPermissionsUseCase
from src.application.use_cases.permissions.delete_permission import DeletePermissionUseCase
from src.application.use_cases.permissions.assign_permission_to_role import AssignPermissionToRoleUseCase
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.use_cases.groups.list_groups import ListGroupsUseCase
from src.application.use_cases.groups.delete_group import DeleteGroupUseCase
from src.application.use_cases.groups.assign_user_to_group import AssignUserToGroupUseCase
from src.application.use_cases.rbac.create_attribute import CreateRbacAttributeUseCase
from src.application.use_cases.rbac.list_attributes import ListRbacAttributesUseCase
from src.application.use_cases.rbac.delete_attribute import DeleteRbacAttributeUseCase
from src.application.use_cases.rbac.assign_attribute_to_user import AssignAttributeToUserUseCase
from src.application.dtos.role_dto import CreateRoleDTO, RoleOutputDTO
from src.application.dtos.permission_dto import CreatePermissionDTO, PermissionOutputDTO
from src.application.dtos.group_dto import CreateGroupDTO, GroupOutputDTO
from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, RbacAttributeOutputDTO, AssignAttributeDTO


class RbacService:
    """Orquestra roles, permissões, grupos e atributos RBAC."""

    def __init__(self, db: Session):
        self._db = db
        self._roles = SqliteRoleRepository(db)
        self._perms = SqlitePermissionRepository(db)
        self._groups = SqliteGroupRepository(db)
        self._attrs = SqliteRbacAttributeRepository(db)

    # roles
    def create_role(self, dto: CreateRoleDTO) -> RoleOutputDTO:
        return CreateRoleUseCase(self._roles).execute(dto)

    def list_roles(self) -> list[RoleOutputDTO]:
        return ListRolesUseCase(self._roles).execute()

    def delete_role(self, role_id: str) -> None:
        DeleteRoleUseCase(self._roles).execute(role_id)

    def assign_role(self, user_id: str, role_id: str) -> None:
        AssignRoleToUserUseCase(self._db).execute(user_id, role_id)

    def revoke_role(self, user_id: str, role_id: str) -> None:
        RevokeRoleFromUserUseCase(self._db).execute(user_id, role_id)

    # permissions
    def create_permission(self, dto: CreatePermissionDTO) -> PermissionOutputDTO:
        return CreatePermissionUseCase(self._perms).execute(dto)

    def list_permissions(self) -> list[PermissionOutputDTO]:
        return ListPermissionsUseCase(self._perms).execute()

    def delete_permission(self, perm_id: str) -> None:
        DeletePermissionUseCase(self._perms).execute(perm_id)

    def assign_permission(self, role_id: str, perm_id: str) -> None:
        AssignPermissionToRoleUseCase(self._db).execute(role_id, perm_id)

    # groups
    def create_group(self, dto: CreateGroupDTO) -> GroupOutputDTO:
        return CreateGroupUseCase(self._groups).execute(dto)

    def list_groups(self) -> list[GroupOutputDTO]:
        return ListGroupsUseCase(self._groups).execute()

    def delete_group(self, group_id: str) -> None:
        DeleteGroupUseCase(self._groups).execute(group_id)

    def assign_user_to_group(self, user_id: str, group_id: str) -> None:
        AssignUserToGroupUseCase(self._db).execute(user_id, group_id)

    # rbac attributes
    def create_attribute(self, dto: CreateRbacAttributeDTO) -> RbacAttributeOutputDTO:
        return CreateRbacAttributeUseCase(self._attrs).execute(dto)

    def list_attributes(self) -> list[RbacAttributeOutputDTO]:
        return ListRbacAttributesUseCase(self._attrs).execute()

    def delete_attribute(self, attr_id: str) -> None:
        DeleteRbacAttributeUseCase(self._attrs).execute(attr_id)

    def assign_attribute(self, dto: AssignAttributeDTO) -> None:
        AssignAttributeToUserUseCase(self._db).execute(dto)
