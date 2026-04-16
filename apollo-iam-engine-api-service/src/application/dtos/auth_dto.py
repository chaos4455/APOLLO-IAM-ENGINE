from dataclasses import dataclass
from typing import Optional


@dataclass
class LoginInputDTO:
    username: str
    password: str
    ip_address: str = ""


@dataclass
class TokenOutputDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
