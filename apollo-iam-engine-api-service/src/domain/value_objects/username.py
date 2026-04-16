import re
from dataclasses import dataclass


_PATTERNS = [
    r"^[a-zA-Z0-9_.-]{2,64}$",           # user, usuario.nome, nome.sobrenome
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",   # email@email.com
]


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):
        if not any(re.match(p, self.value) for p in _PATTERNS):
            raise ValueError(f"Username inválido: {self.value!r}")

    def __str__(self):
        return self.value
