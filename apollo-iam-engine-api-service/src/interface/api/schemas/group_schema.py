from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    description: str = ""

class GroupResponse(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
