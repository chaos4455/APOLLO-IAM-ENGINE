from dataclasses import dataclass


@dataclass
class CreateRoleDTO:
    name: str
    description: str = ""


@dataclass
class RoleOutputDTO:
    id: str
    name: str
    description: str
    is_active: bool
    permissions: list[str]
