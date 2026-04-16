from src.application.dtos.group_dto import GroupOutputDTO
from src.domain.ports.group_repository import GroupRepository


class ListGroupsUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self) -> list[GroupOutputDTO]:
        return [GroupOutputDTO(id=g.id, name=g.name, description=g.description,
                               is_active=g.is_active)
                for g in self._groups.list_all()]
