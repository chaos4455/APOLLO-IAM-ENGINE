from passlib.context import CryptContext
from src.domain.ports.password_hasher import PasswordHasher

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, plain: str) -> str:
        return _ctx.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return _ctx.verify(plain, hashed)
