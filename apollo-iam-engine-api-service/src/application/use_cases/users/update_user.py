from src.application.dtos.user_dto import UpdateUserDTO, UserOutputDTO
from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import UserNotFoundError


class UpdateUserUseCase:
    def __init__(self, users: UserRepository):
        self._users = users

    def execute(self, dto: UpdateUserDTO) -> UserOutputDTO:
        user = self._users.find_by_id(dto.user_id)
        if not user:
            raise UserNotFoundError(dto.user_id)
        if dto.email is not None: user.email = dto.email
        if dto.full_name is not None: user.full_name = dto.full_name
        if dto.is_active is not None: user.is_active = dto.is_active
        if dto.group_id is not None: user.group_id = dto.group_id
        if dto.type_id is not None: user.type_id = dto.type_id
        if dto.level_id is not None: user.level_id = dto.level_id
        user.touch()
        saved = self._users.save(user)
        from src.application.use_cases.users.create_user import _to_output
        return _to_output(saved)
