from typing import List

from src.repository.word import WordRepository
from src.model.word import Word
from src.dto.word import WordCreate, WordUpdate, WordResponse


class WordService:
    def __init__(self, word_repo: WordRepository):
        self.word_repo = word_repo

    async def create_user(self, word_service: WordCreate) -> WordResponse:



    async def verify_user(self, user_auth: UserAuth) -> UserResponse:
        user: User = await self.word_repo.get_user_by_email(user_email=user_auth.email)

        if not user:
            raise Exception(f"Пользователя с email `{user_auth.email}` не существует!")

        result = await self.verify_password(password=user_auth.password, hash_password=user.hash_password)

        if not result:
            raise Exception("Неверный пароль! Повторите попытку")

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            birthday=user.birthday
        )

    async def get_user(self, user_id: int) -> UserResponse:
        user: User = await self.word_repo.get_user_by_id(user_id=user_id)

        if not user:
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            birthday=user.birthday
        )

    async def get_users(self) -> List[UserResponse]:
        users = await self.word_repo.get_users()

        users_response_list = [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                birthday=user.birthday
            )
            for user
            in users
        ]

        return users_response_list

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        check_user_exist: bool = await self.check_user_exist(user_id=user_id)

        if not check_user_exist:
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        check_duplicate: bool = await self.check_duplicate(user_email=user_update.email)

        if check_duplicate:
            raise Exception(f"Email `{user_update.email}` занят!")

        hashed_password: str = await self.hash_password(password=user_update.password)

        user_update_hash_password = UserUpdate(
            username=user_update.username,
            password=hashed_password,
            email=user_update.email,
            birthday=user_update.birthday
        )

        user: User = await self.word_repo.update_user_by_id(user_id=user_id, user_update=user_update_hash_password)

        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            birthday=user.birthday
        )

    async def delete_user(self, user_id: int) -> str:
        check_user_exist: bool = await self.check_user_exist(user_id=user_id)

        if not check_user_exist:
            raise Exception(f"Пользователь с id = `{user_id}` не был найден!")

        result: str = await self.word_repo.delete_user_by_id(user_id=user_id)

        return result

    async def hash_password(self, password: str) -> str:
        hashed_password = self.hash_generator.generate_hash_from_password(password=password)
        return hashed_password

    async def verify_password(self, password: str, hash_password: str) -> bool:
        result = self.hash_generator.verify_password(password=password, hashed_password=hash_password)
        return result

    async def check_duplicate(self, user_email: str) -> bool:
        user: User = await self.word_repo.get_user_by_email(user_email=user_email)

        if user:
            return True
        else:
            return False

    async def check_user_exist(self, user_id: int) -> bool:
        user: User = await self.word_repo.get_user_by_id(user_id=user_id)

        if user:
            return True
        else:
            return False