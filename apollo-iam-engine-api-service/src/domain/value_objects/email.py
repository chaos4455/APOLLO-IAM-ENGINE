import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", self.value):
            raise ValueError(f"E-mail inválido: {self.value!r}")

    def __str__(self):
        return self.value
