from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CreateUserDTO:
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None
    role_names: list[str] = field(default_factory=list)


@dataclass
class UpdateUserDTO:
    user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    group_id: Optional[str] = None
    type_id: Optional[str] = None
    level_id: Optional[str] = None


@dataclass
class UserOutputDTO:
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
