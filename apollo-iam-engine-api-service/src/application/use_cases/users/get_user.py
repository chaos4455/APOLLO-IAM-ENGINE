from src.application.dtos.user_dto import UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError
from src.application.use_cases.users.create_user import _to_output


class GetUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, user_id: str) -> UserOutputDTO:
        user = self._users.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return _to_output(user)
