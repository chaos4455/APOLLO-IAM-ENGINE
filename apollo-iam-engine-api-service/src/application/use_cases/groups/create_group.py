from src.application.dtos.group_dto import CreateGroupDTO, GroupOutputDTO
from src.domain.ports.group_repository import GroupRepository
from src.domain.entities.group import Group
import uuid


class CreateGroupUseCase:
    def __init__(self, groups: GroupRepository):
        self._groups = groups

    def execute(self, dto: CreateGroupDTO) -> GroupOutputDTO:
        g = Group(id=str(uuid.uuid4()), name=dto.name, description=dto.description)
        saved = self._groups.save(g)
        return GroupOutputDTO(id=saved.id, name=saved.name,
                              description=saved.description, is_active=saved.is_active)
