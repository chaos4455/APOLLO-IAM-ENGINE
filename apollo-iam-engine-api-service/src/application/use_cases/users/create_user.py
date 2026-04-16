from src.application.dtos.user_dto import CreateUserDTO, UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.password_hasher import PasswordHasher
from src.domain.entities.user import User
from src.domain.value_objects.username import Username
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
import uuid


class CreateUserUseCase:
    def __init__(self, users: UserRepository, hasher: PasswordHasher):
        self._users = users
        self._hasher = hasher

    def execute(self, dto: CreateUserDTO) -> UserOutputDTO:
        Username(dto.username)  # validates
        if self._users.find_by_username(dto.username):
            raise UserAlreadyExistsError(f"Username {dto.username!r} já existe.")
        if dto.email and self._users.find_by_email(dto.email):
            raise UserAlreadyExistsError(f"E-mail {dto.email!r} já existe.")
        user = User(
            id=str(uuid.uuid4()),
            username=dto.username,
            email=dto.email,
            hashed_password=self._hasher.hash(dto.password),
            full_name=dto.full_name,
            is_active=dto.is_active,
            is_superuser=dto.is_superuser,
            group_id=dto.group_id,
            type_id=dto.type_id,
            level_id=dto.level_id,
        )
        saved = self._users.save(user)
        return _to_output(saved)


def _to_output(u: User) -> UserOutputDTO:
    return UserOutputDTO(
        id=u.id, username=u.username, email=u.email, full_name=u.full_name,
        is_active=u.is_active, is_superuser=u.is_superuser,
        group_id=u.group_id, type_id=u.type_id, level_id=u.level_id,
        roles=u.roles, created_at=str(u.created_at), updated_at=str(u.updated_at),
    )
