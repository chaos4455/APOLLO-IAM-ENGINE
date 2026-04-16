from __future__ import annotations
from src.domain.ports.permission_repository import PermissionRepository
from src.domain.exceptions.rbac_exceptions import PermissionNotFoundError


class UpdatePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, perm_id: str, **kwargs):
        p = self._perms.find_by_id(perm_id)
        if not p:
            raise PermissionNotFoundError(perm_id)
        for k, v in kwargs.items():
            if v is not None:
                setattr(p, k, v)
        return self._perms.save(p)
