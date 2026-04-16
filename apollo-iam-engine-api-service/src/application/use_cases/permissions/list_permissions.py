from src.application.dtos.permission_dto import PermissionOutputDTO
from src.domain.ports.permission_repository import PermissionRepository


class ListPermissionsUseCase:
    def __init__(self, perms: PermissionRepository):
        self._perms = perms

    def execute(self) -> list[PermissionOutputDTO]:
        return [PermissionOutputDTO(id=p.id, name=p.name, resource=p.resource,
                                    action=p.action, description=p.description)
                for p in self._perms.list_all()]
