from typing import List, Type

from sqlalchemy import Insert, Select, Update, Delete

from src.model.user import User
from src.dto.user import UserCreateHashPassword, UserUpdateHashedPassword
from src.repository.base_repo import BaseRepository

from src.model.category import Category


class UserRepository(BaseRepository):
    async def create_user(self, user_create: UserCreateHashPassword) -> User:
        async with self.db_session() as db_session:
            user = User(username=user_create.username, name=user_create.name,
                        hashed_password=user_create.hashed_password)

            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

            return user

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.db_session() as db_session:
            stmt = Select(User).where(User.id == user_id)

            result = await db_session.execute(statement=stmt)
            user = result.scalar()

            return user

    async def get_user_by_username(self, username: str) -> User:
        async with self.db_session() as db_session:
            stmt = Select(User).where(User.username == username)

            result = await db_session.execute(statement=stmt)
            user = result.scalar()

            return user

    async def get_users_by_category_id(self, category_id: int) -> List[User]:
        async with self.db_session() as db_session:
            stmt = Select(User).join(Category).where(Category.id == category_id)

            users_list = await db_session.execute(stmt)

            users_list = [
                element
                for element
                in users_list.scalars()
            ]

            return users_list

    async def update_user_by_id(self, user: User, user_update: UserUpdateHashedPassword) -> User:
        async with self.db_session() as db_session:
            db_session.add(user)

            if user_update.username:
                user.username = user_update.username

            if user_update.hashed_password:
                user.hashed_password = user_update.hashed_password

            if user_update.name:
                user.name = user_update.name

            await db_session.commit()
            await db_session.refresh(user)

            return user

    async def delete_user_by_id(self, user_id: int) -> int:
        async with self.db_session() as db_session:
            stmt = Delete(User).where(User.id == user_id)

            await db_session.execute(statement=stmt)
            await db_session.commit()

            return user_id
