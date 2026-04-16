from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenPayload:
    sub: str                           # username
    user_id: str = ""
    is_superuser: bool = False
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    group: str | None = None           # group name
    group_id: str | None = None        # group id
    user_type: str | None = None       # UserType name
    user_level: str | None = None      # UserLevel name
    user_level_rank: int = 0           # UserLevel rank (para comparacao numerica)
    rbac: dict[str, Any] = field(default_factory=dict)   # RBAC attributes key→value
    abac: dict[str, Any] = field(default_factory=dict)   # ABAC attributes (custom entities + extras)
    exp: int = 0
    iat: int = 0
    jti: str = ""

    # ── helpers de avaliacao ABAC ─────────────────────────────────────────────

    def has_role(self, role: str) -> bool:
        return role in self.roles

    def has_any_role(self, *roles: str) -> bool:
        return any(r in self.roles for r in roles)

    def has_permission(self, perm: str) -> bool:
        return perm in self.permissions

    def abac_match(self, key: str, value: Any) -> bool:
        """Verifica se um atributo ABAC do usuario tem o valor esperado."""
        return str(self.abac.get(key, "")) == str(value)

    def abac_in(self, key: str, values: list) -> bool:
        """Verifica se o atributo ABAC esta em uma lista de valores permitidos."""
        return str(self.abac.get(key, "")) in [str(v) for v in values]

    def level_gte(self, rank: int) -> bool:
        """Verifica se o nivel do usuario e >= ao rank exigido."""
        return self.user_level_rank >= rank
