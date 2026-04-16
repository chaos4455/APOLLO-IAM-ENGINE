from dataclasses import dataclass


@dataclass
class CreateRbacAttributeDTO:
    key: str
    label: str
    value_type: str = "string"
    description: str = ""


@dataclass
class RbacAttributeOutputDTO:
    id: str
    key: str
    label: str
    value_type: str
    description: str
    is_active: bool


@dataclass
class AssignAttributeDTO:
    user_id: str
    attribute_key: str
    value: str
