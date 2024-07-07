from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.user import User
from src.dto.user import UserCreateHashPassword, UserUpdateHashedPassword
from src.repository.base_repo import BaseRepository

from src.model.category import Category


class UserRepository(BaseRepository):
    async def create_user(self, user_create: UserCreateHashPassword) -> User:
        stmt = Insert(User).values(username=user_create.username, name=user_create.name,
                                   hashed_password=user_create.hashed_password).returning(User)

        result = await self.db_session.execute(statement=stmt)
        user = result.scalar()

        await self.db_session.commit()

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = Select(User).where(User.id == user_id)

        result = await self.db_session.execute(statement=stmt)
        user = result.scalar()

        return user

    async def get_user_by_username(self, username: str) -> User:
        stmt = Select(User).where(User.username == username)

        result = await self.db_session.execute(statement=stmt)
        user = result.scalar()

        return user

    async def get_users_by_category_id(self, category_id: int) -> List[User]:
        stmt = Select(User).join(Category).where(Category.id == category_id)

        users_list = await self.db_session.execute(stmt)

        users_list = [
            element
            for element
            in users_list.scalars()
        ]

        return users_list

    async def update_user_by_id(self, user_id: int, user_update: UserUpdateHashedPassword) -> User:
        stmt = Update(User).where(User.id == user_id)

        if user_update.username:
            stmt = stmt.values(username=user_update.username)

        if user_update.hashed_password:
            stmt = stmt.values(hashed_password=user_update.hashed_password)

        if user_update.name:
            stmt = stmt.values(name=user_update.name)

        stmt = stmt.returning(User)
        user = await self.db_session.execute(stmt)
        user = user.scalar()

        await self.db_session.commit()

        return user

    async def delete_user_by_id(self, user_id: int) -> int:
        stmt = Delete(User).where(User.id == user_id)

        await self.db_session.execute(statement=stmt)
        await self.db_session.commit()

        return user_id
