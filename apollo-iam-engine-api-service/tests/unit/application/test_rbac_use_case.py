import pytest
from unittest.mock import MagicMock
from src.application.use_cases.roles.create_role import CreateRoleUseCase
from src.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.use_cases.permissions.create_permission import CreatePermissionUseCase
from src.application.use_cases.groups.create_group import CreateGroupUseCase
from src.application.dtos.role_dto import CreateRoleDTO
from src.application.dtos.permission_dto import CreatePermissionDTO
from src.application.dtos.group_dto import CreateGroupDTO
from src.domain.entities.role import Role
from src.domain.exceptions.rbac_exceptions import RoleNotFoundError


def test_create_role():
    repo = MagicMock()
    repo.save.side_effect = lambda r: r
    uc = CreateRoleUseCase(repo)
    result = uc.execute(CreateRoleDTO(name="editor", description="Editor role"))
    assert result.name == "editor"


def test_delete_role_not_found():
    repo = MagicMock()
    repo.find_by_id.return_value = None
    uc = DeleteRoleUseCase(repo)
    with pytest.raises(RoleNotFoundError):
        uc.execute("nonexistent-id")


def test_create_permission():
    repo = MagicMock()
    repo.save.side_effect = lambda p: p
    uc = CreatePermissionUseCase(repo)
    result = uc.execute(CreatePermissionDTO(name="docs:read", resource="docs", action="read"))
    assert result.name == "docs:read"
    assert result.resource == "docs"


def test_create_group():
    repo = MagicMock()
    repo.save.side_effect = lambda g: g
    uc = CreateGroupUseCase(repo)
    result = uc.execute(CreateGroupDTO(name="TI", description="Time de TI"))
    assert result.name == "TI"
