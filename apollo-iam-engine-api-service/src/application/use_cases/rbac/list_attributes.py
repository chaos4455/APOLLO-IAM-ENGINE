from src.application.dtos.rbac_dto import RbacAttributeOutputDTO
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository


class ListRbacAttributesUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self) -> list[RbacAttributeOutputDTO]:
        return [RbacAttributeOutputDTO(id=a.id, key=a.key, label=a.label,
                                       value_type=a.value_type, description=a.description,
                                       is_active=a.is_active)
                for a in self._repo.list_all()]
