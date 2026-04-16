from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    role_names: list[str] = []

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    group_id: Optional[str]
    type_id: Optional[str]
    level_id: Optional[str]
    roles: list[str]
    created_at: str
    updated_at: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ResetPasswordRequest(BaseModel):
    new_password: str
