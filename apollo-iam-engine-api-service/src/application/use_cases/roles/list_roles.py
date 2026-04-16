from src.application.dtos.role_dto import RoleOutputDTO
from src.domain.ports.role_repository import RoleRepository


class ListRolesUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self) -> list[RoleOutputDTO]:
        return [RoleOutputDTO(id=r.id, name=r.name, description=r.description,
                              is_active=r.is_active, permissions=r.permissions)
                for r in self._roles.list_all()]
