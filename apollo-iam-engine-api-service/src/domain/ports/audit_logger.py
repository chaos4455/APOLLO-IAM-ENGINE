from abc import ABC, abstractmethod
from src.domain.entities.audit_log import AuditLog


class AuditLogger(ABC):
    @abstractmethod
    def log(self, entry: AuditLog) -> None: ...
    @abstractmethod
    def list_logs(self, skip: int = 0, limit: int = 100) -> list[AuditLog]: ...
