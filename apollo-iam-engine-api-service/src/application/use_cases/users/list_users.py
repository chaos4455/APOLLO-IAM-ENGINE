from src.application.dtos.user_dto import UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.application.use_cases.users.create_user import _to_output


class ListUsersUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, skip: int = 0, limit: int = 100) -> list[UserOutputDTO]:
        return [_to_output(u) for u in self._users.list_all(skip, limit)]
