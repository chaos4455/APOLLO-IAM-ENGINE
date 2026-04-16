from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class ToggleUserStatusUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> bool:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        user.is_active = not user.is_active
        user.touch()
        self._users.save(user)
        return user.is_active
