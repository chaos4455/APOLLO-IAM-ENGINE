from __future__ import annotations
from src.domain.ports.group_repository import GroupRepository
from src.domain.exceptions.rbac_exceptions import GroupNotFoundError


class UpdateGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, group_id: str, name: str | None = None, description: str | None = None):
        g = self._groups.find_by_id(group_id)
        if not g:
            raise GroupNotFoundError(group_id)
        if name: g.name = name
        if description is not None: g.description = description
        return self._groups.save(g)
