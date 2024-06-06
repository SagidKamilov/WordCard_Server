from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.user import User
from src.dto.user import UserCreateHashPassword, UserUpdateHashedPassword
from src.repository.base_repo import BaseRepository

from src.model.category import Category


class UserRepository(BaseRepository):
    async def create_user(self, user_create: UserCreateHashPassword) -> User:
        stmt = Insert(User).values(username=user_create.username, name=user_create.name,
                                   hashed_password=user_create.hashed_password)

        result = await self.db_session.execute(statement=stmt)
        user = result.scalar()

        await self.db_session.commit()

        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = Select(User).where(User.id == user_id)

        result = await self.db_session.execute(statement=stmt)
        user = result.scalar()

        if not user:
            return None

        return user

    async def get_users_by_category_id(self, category_id: int) -> List[User] | None:
        stmt = Select(User).join(Category).where(Category.id == category_id)

        users_list = await self.db_session.execute(stmt)
        if not users_list:
            return None

        users_list = [
            element.scalar()
            for element
            in users_list
        ]

        return users_list

    async def update_user_by_id(self, user_id: int, user_update: UserUpdateHashedPassword) -> User | None:
        user = await self.get_user_by_id(user_id=user_id)

        if not user:
            return None

        if user_update.username:
            user.username = user_update.username

        if user_update.name:
            user.name = user_update.name

        if user_update.hashed_password:
            user.hashed_password = user_update.hashed_password

        await self.db_session.commit()

        return user

    async def delete_user_by_id(self, user_id: int) -> User.id | None:
        user = await self.get_user_by_id(user_id=user_id)

        if not user:
            return None

        stmt = Delete(User).where(User.id == user_id).returning(User.id)
        result = await self.db_session.execute(statement=stmt)
        result_scalar = result.scalar()

        if not result_scalar:
            return None

        await self.db_session.commit()

        return result
