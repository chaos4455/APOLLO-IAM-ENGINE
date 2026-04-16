from dataclasses import dataclass


@dataclass
class CreatePermissionDTO:
    name: str
    resource: str
    action: str
    description: str = ""


@dataclass
class PermissionOutputDTO:
    id: str
    name: str
    resource: str
    action: str
    description: str
