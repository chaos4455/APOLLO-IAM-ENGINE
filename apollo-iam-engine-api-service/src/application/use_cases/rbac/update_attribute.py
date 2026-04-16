from __future__ import annotations
from src.domain.ports.rbac_attribute_repository import RbacAttributeRepository
from src.domain.exceptions.rbac_exceptions import AttributeNotFoundError


class UpdateRbacAttributeUseCase:
    def __init__(self, repo: RbacAttributeRepository):
        self._repo = repo

    def execute(self, attr_id: str, **kwargs):
        attr = self._repo.find_by_id(attr_id)
        if not attr:
            raise AttributeNotFoundError(attr_id)
        for k, v in kwargs.items():
            if v is not None:
                setattr(attr, k, v)
        return self._repo.save(attr)
