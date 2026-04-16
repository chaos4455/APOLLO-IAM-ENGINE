from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class DeleteUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> None:
        if not self._users.find_by_id(user_id):
            raise UserNotFoundError(user_id)
        self._users.delete(user_id)
