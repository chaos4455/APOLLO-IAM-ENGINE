from sqlalchemy.orm import Session
from src.infrastructure.repositories.user_repository_impl import SqliteUserRepository
from src.infrastructure.security.password_hasher_impl import BcryptPasswordHasher
from src.application.use_cases.users.create_user import CreateUserUseCase
from src.application.use_cases.users.update_user import UpdateUserUseCase
from src.application.use_cases.users.delete_user import DeleteUserUseCase
from src.application.use_cases.users.get_user import GetUserUseCase
from src.application.use_cases.users.list_users import ListUsersUseCase
from src.application.use_cases.users.change_password import ChangePasswordUseCase
from src.application.use_cases.users.reset_password import ResetPasswordUseCase
from src.application.use_cases.users.toggle_user_status import ToggleUserStatusUseCase
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO, UserOutputDTO


class UserService:
    """Orquestra os casos de uso de usuários."""

    def __init__(self, db: Session):
        self._repo = SqliteUserRepository(db)
        self._hasher = BcryptPasswordHasher()

    def create(self, dto: CreateUserDTO) -> UserOutputDTO:
        return CreateUserUseCase(self._repo, self._hasher).execute(dto)

    def update(self, dto: UpdateUserDTO) -> UserOutputDTO:
        return UpdateUserUseCase(self._repo).execute(dto)

    def delete(self, user_id: str) -> None:
        DeleteUserUseCase(self._repo).execute(user_id)

    def get(self, user_id: str) -> UserOutputDTO:
        return GetUserUseCase(self._repo).execute(user_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[UserOutputDTO]:
        return ListUsersUseCase(self._repo).execute(skip, limit)

    def change_password(self, user_id: str, old: str, new: str) -> None:
        ChangePasswordUseCase(self._repo, self._hasher).execute(user_id, old, new)

    def reset_password(self, user_id: str, new: str) -> None:
        ResetPasswordUseCase(self._repo, self._hasher).execute(user_id, new)

    def toggle_status(self, user_id: str) -> bool:
        return ToggleUserStatusUseCase(self._repo).execute(user_id)
