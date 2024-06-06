from typing import List

from src.model.user import User
from src.repository.user import UserRepository
from src.dto.user import UserAuth, UserCreate, UserCreateHashPassword, UserUpdate, UserUpdateHashedPassword, UserResponse
from src.security.hash_password import HashGenerator


class UserService:
    def __init__(self, user_repo: UserRepository, hash_gen: HashGenerator):
        self.user_repo = user_repo
        self.hash_generator = hash_gen

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        check_duplicate = await self.check_duplicate(username=user_create.username)

        if check_duplicate:
            raise Exception(f"Пользователь с именем {user_create.username} уже занят")

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
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        return UserResponse(
            id=user.id,
            username=user.username,
            name=user.name
        )

    async def get_users_of_category(self, category_id: int) -> List[UserResponse]:
        users = await self.user_repo.get_users_by_category_id(category_id=category_id)

        users_response = [
            UserResponse(
                id=element.id,
                username=element.username,
                name=element.name
            )
            for element
            in users
        ]

        return users_response

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        check_user_exist: bool = await self.check_user_exist(user_id=user_id)

        if not check_user_exist:
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        check_duplicate: bool = await self.check_duplicate(username=user_update.username)

        if check_duplicate:
            raise Exception(f"Логин `{user_update.username}` уже занят!")

        hashed_password: str = await self.hash_password(password=user_update.password)

        user: User = await self.user_repo.update_user_by_id(user_id=user_id, user_update=UserUpdateHashedPassword(
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
        check_user_exist: bool = await self.check_user_exist(user_id=user_id)

        if not check_user_exist:
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        result: int = await self.user_repo.delete_user_by_id(user_id=user_id)

        return result

    async def verify_user(self, user_auth: UserAuth) -> UserResponse:
        user: User = await self.user_repo.get_user_by_username(username=user_auth.username)

        if not user:
            raise Exception(f"Пользователя с username `{user_auth.username}` не существует!")

        result = await self.verify_password(password=user_auth.password, hash_password=user.hashed_password)

        if not result:
            raise Exception("Неверный пароль! Повторите попытку")

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

        if user:
            return True
        else:
            return False

    async def check_user_exist(self, user_id: int) -> bool:
        user: User = await self.user_repo.get_user_by_id(user_id=user_id)

        if user:
            return True
        else:
            return False
