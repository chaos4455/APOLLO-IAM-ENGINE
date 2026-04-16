from __future__ import annotations
from src.domain.ports.role_repository import RoleRepository
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


class UpdateRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, role_id: str, name: str | None = None, description: str | None = None):
        role = self._roles.find_by_id(role_id)
        if not role:
            raise RoleNotFoundError(role_id)
        if name: role.name = name
        if description is not None: role.description = description
        return self._roles.save(role)
