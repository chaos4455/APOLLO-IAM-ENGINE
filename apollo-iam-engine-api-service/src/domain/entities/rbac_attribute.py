from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class RbacAttribute:
    """Atributo RBAC dinâmico e expansível (ex: department, cost_center, system_access)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    key: str = ""          # ex: "department"
    label: str = ""        # ex: "Departamento"
    value_type: str = "string"  # string | integer | boolean | list
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
