from src.domain.ports.group_repository import GroupRepository
from src.domain.exceptions.rbac_exceptions import GroupNotFoundError


class DeleteGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, group_id: str) -> None:
        if not self._groups.find_by_id(group_id):
            raise GroupNotFoundError(group_id)
        self._groups.delete(group_id)
