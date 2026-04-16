from src.application.dtos.permission_dto import CreatePermissionDTO, PermissionOutputDTO
from src.domain.ports.permission_repository import PermissionRepository
from src.domain.entities.permission import Permission
import uuid


class CreatePermissionUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self, dto: CreatePermissionDTO) -> PermissionOutputDTO:
        p = Permission(id=str(uuid.uuid4()), name=dto.name, resource=dto.resource,
                       action=dto.action, description=dto.description)
        saved = self._perms.save(p)
        return PermissionOutputDTO(id=saved.id, name=saved.name, resource=saved.resource,
                                   action=saved.action, description=saved.description)
