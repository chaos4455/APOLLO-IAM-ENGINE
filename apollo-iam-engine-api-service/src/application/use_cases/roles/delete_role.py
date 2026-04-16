from src.domain.ports.role_repository import RoleRepository
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


class DeleteRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, role_id: str) -> None:
        if not self._roles.find_by_id(role_id):
            raise RoleNotFoundError(role_id)
        self._roles.delete(role_id)
