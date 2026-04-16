from src.application.dtos.rbac_dto import CreateRbacAttributeDTO, RbacAttributeOutputDTO
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.entities.rbac_attribute import RbacAttribute
import uuid


class CreateRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, dto: CreateRbacAttributeDTO) -> RbacAttributeOutputDTO:
        attr = RbacAttribute(id=str(uuid.uuid4()), key=dto.key, label=dto.label,
                             value_type=dto.value_type, description=dto.description)
        saved = self._repo.save(attr)
        return RbacAttributeOutputDTO(id=saved.id, key=saved.key, label=saved.label,
                                      value_type=saved.value_type, description=saved.description,
                                      is_active=saved.is_active)
