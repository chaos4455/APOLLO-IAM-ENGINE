from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    """Senha em texto plano — sem restrição de tamanho ou complexidade."""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Senha não pode ser vazia.")

    def __str__(self):
        return self.value
