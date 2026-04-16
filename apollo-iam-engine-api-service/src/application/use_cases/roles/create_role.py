from src.application.dtos.role_dto import CreateRoleDTO, RoleOutputDTO
from src.domain.ports.role_repository import RoleRepository
from src.domain.entities.role import Role
import uuid


class CreateRoleUseCase:
    def __init__(self, roles: RoleRepository):
        self._roles = roles

    def execute(self, dto: CreateRoleDTO) -> RoleOutputDTO:
        role = Role(id=str(uuid.uuid4()), name=dto.name, description=dto.description)
        saved = self._roles.save(role)
        return RoleOutputDTO(id=saved.id, name=saved.name, description=saved.description,
                             is_active=saved.is_active, permissions=saved.permissions)
