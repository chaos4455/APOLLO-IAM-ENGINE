from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.exceptions.rbac_exceptions import AttributeNotFoundError


class DeleteRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, attr_id: str) -> None:
        if not self._repo.find_by_id(attr_id):
            raise AttributeNotFoundError(attr_id)
        self._repo.delete(attr_id)
