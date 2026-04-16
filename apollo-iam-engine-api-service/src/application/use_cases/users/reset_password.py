from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.exceptions.user_exceptions import UserNotFoundError


class ResetPasswordUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, user_id: str, new_password: str) -> None:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        user.hashed_password = self._hasher.hash(new_password)
        user.touch()
        self._users.save(user)
