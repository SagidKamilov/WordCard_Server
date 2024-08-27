from typing import List

from src.model.user import User
from src.repository.user import UserRepository
from src.dto.user import UserAuth, UserCreate, UserCreateHashPassword, UserUpdate, UserUpdateHashedPassword, UserResponse
from src.security.hash_password import HashGenerator
from src.error.user.user_errors import UserAlreadyExists, UserIdNotExists, UserUsernameNotExists, UserWrongPassword


class UserService:
    def __init__(self, user_repo: UserRepository, hash_gen: HashGenerator):
        self.user_repo = user_repo
        self.hash_generator = hash_gen

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        duplicate = await self.check_duplicate(username=user_create.username)

        if duplicate:
            raise UserAlreadyExists(username=user_create.username)

        hashed_password: str = await self.hash_password(password=user_create.password)

        user = await self.user_repo.create_user(
            user_create=UserCreateHashPassword(
                name=user_create.name,
                username=user_create.username,
                hashed_password=hashed_password
            )
        )

        return UserResponse(
            id=user.id,
            username=user.username,
            name=user.name
        )

    async def get_user(self, user_id: int) -> UserResponse:
        user: User = await self.user_repo.get_user_by_id(user_id=user_id)

        if not user:
            raise UserIdNotExists(user_id=user_id)

        return UserResponse(
            id=user.id,
            username=user.username,
            name=user.name
        )

    async def get_users_of_category(self, category_id: int) -> List[UserResponse]:
        users = await self.user_repo.get_users_by_category_id(category_id=category_id)

        users_response = list(map(lambda user: UserResponse(id=user.id, username=user.username, name=user.name), users))

        return users_response

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user_exists: User = await self.user_repo.get_user_by_id(user_id=user_id)

        if not user_exists:
            raise UserIdNotExists(user_id=user_id)

        duplicate: bool = await self.check_duplicate(username=user_update.username)

        if duplicate:
            raise UserAlreadyExists(username=user_update.username)

        hashed_password: str = await self.hash_password(password=user_update.password)

        user: User = await self.user_repo.update_user_by_id(user=user_exists, user_update=UserUpdateHashedPassword(
            name=user_update.name,
            username=user_update.username,
            hashed_password=hashed_password
        ))

        return UserResponse(
            id=user.id,
            username=user.username,
            name=user.name
        )

    async def delete_user(self, user_id: int) -> int:
        user_exists: bool = await self.check_user_exists(user_id=user_id)

        if not user_exists:
            raise UserIdNotExists(user_id=user_id)

        result: int = await self.user_repo.delete_user_by_id(user_id=user_id)

        return result

    async def verify_user(self, user_auth: UserAuth) -> UserResponse:
        user: User = await self.user_repo.get_user_by_username(username=user_auth.username)

        if not user:
            raise UserUsernameNotExists(username=user_auth.username)

        result = await self.verify_password(password=user_auth.password, hash_password=user.hashed_password)

        if not result:
            raise UserWrongPassword()

        return UserResponse(
            id=user.id,
            username=user.username,
            name=user.name
        )

    async def hash_password(self, password: str) -> str:
        hashed_password = self.hash_generator.generate_hash_from_password(password=password)
        return hashed_password

    async def verify_password(self, password: str, hash_password: str) -> bool:
        result = self.hash_generator.verify_password(password=password, hashed_password=hash_password)
        return result

    async def check_duplicate(self, username: str) -> bool:
        user: User = await self.user_repo.get_user_by_username(username=username)

        return True if user else False

    async def check_user_exists(self, user_id: int) -> bool:
        user: User = await self.user_repo.get_user_by_id(user_id=user_id)

        return True if user else False
