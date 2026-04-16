from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    resource: str
    action: str
    description: str = ""

class PermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: str
    description: str

class AssignPermissionRequest(BaseModel):
    permission_id: str
