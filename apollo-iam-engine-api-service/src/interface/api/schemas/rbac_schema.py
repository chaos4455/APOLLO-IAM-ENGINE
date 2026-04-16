from pydantic import BaseModel


class RbacAttributeCreate(BaseModel):
    key: str
    label: str
    value_type: str = "string"
    description: str = ""

class RbacAttributeResponse(BaseModel):
    id: str
    key: str
    label: str
    value_type: str
    description: str
    is_active: bool

class AssignAttributeRequest(BaseModel):
    attribute_key: str
    value: str
