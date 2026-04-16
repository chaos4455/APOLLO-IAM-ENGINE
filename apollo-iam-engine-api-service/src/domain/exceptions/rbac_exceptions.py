class RoleNotFoundError(Exception):
    """Role não encontrada."""

class PermissionNotFoundError(Exception):
    """Permissão não encontrada."""

class GroupNotFoundError(Exception):
    """Grupo não encontrado."""

class AttributeNotFoundError(Exception):
    """Atributo RBAC não encontrado."""

class InsufficientPermissionsError(Exception):
    """Permissões insuficientes."""
