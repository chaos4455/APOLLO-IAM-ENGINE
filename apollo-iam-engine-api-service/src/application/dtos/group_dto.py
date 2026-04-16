from dataclasses import dataclass


@dataclass
class CreateGroupDTO:
    name: str
    description: str = ""


@dataclass
class GroupOutputDTO:
    id: str
    name: str
    description: str
    is_active: bool
