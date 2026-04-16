from src.domain.ports.permission_repository import PermissionRepository
from src.domain.exceptions.rbac_exceptions import PermissionNotFoundError


class DeletePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, perm_id: str) -> None:
        if not self._perms.find_by_id(perm_id):
            raise PermissionNotFoundError(perm_id)
        self._perms.delete(perm_id)
