from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.category import Category
from src.dto.category import CategoryCreate, CategoryUpdate
from src.repository.base_repo import BaseRepository

from src.model.user_category_list import UserCategoryList


class CategoryRepository(BaseRepository):
    async def create_category(self, user_id: int, category_create: CategoryCreate) -> Category:
        async with self.db_session() as db_session:
            category = Category(owner_id=user_id, category_name=category_create.category_name)

            db_session.add(category)
            await db_session.commit()
            await db_session.refresh(category)

            return category

    async def get_category_by_id(self, category_id: int) -> Category | None:
        async with self.db_session() as db_session:
            stmt = Select(Category).where(Category.id == category_id)

            result = await db_session.execute(statement=stmt)
            category = result.scalar()

            if not category:
                return None

            return category

    async def get_categories_by_user_id(self, user_id: int) -> List[Category]:
        async with self.db_session() as db_session:
            stmt = Select(Category).where(Category.owner_id == user_id)

            categories = await db_session.execute(statement=stmt)

            categories_list = [
                element
                for element
                in categories.scalars()
            ]

            return categories_list

    async def get_all_general_categories(self, user_id: int) -> List[Category]:
        async with self.db_session() as db_session:
            stmt = Select(Category).join(UserCategoryList).where(UserCategoryList.user_id == user_id)

            categories = await db_session.execute(statement=stmt)

            categories_list = [
                element
                for element
                in categories.scalars()
            ]

            return categories_list

    async def check_user_in_category_members(self, user_id: int, category_id: int) -> UserCategoryList:
        async with self.db_session() as db_session:
            stmt = Select(UserCategoryList).where(UserCategoryList.category_id == category_id).where(UserCategoryList.user_id == user_id)

            user_exists = await db_session.execute(stmt)

            return user_exists.scalar()

    async def add_user_by_user_id(self, category_id: int, user_id: int) -> int:
        async with self.db_session() as db_session:
            user_category_list = UserCategoryList(user_id=user_id, category_id=category_id)

            db_session.add(user_category_list)
            await db_session.commit()
            await db_session.refresh(user_category_list)

            return category_id # Здесь еще можно подумать, что возвращать

    async def remove_user_by_user_id(self, category_id: int, user_id: int) -> int:
        async with self.db_session() as db_session:
            stmt = Delete(UserCategoryList).where(UserCategoryList.category_id == category_id).where(UserCategoryList.user_id == user_id)

            await db_session.execute(statement=stmt)
            await db_session.commit()

            return category_id

    async def update_category_by_id(self, category: Category, category_update: CategoryUpdate) -> Category | None:
        async with self.db_session() as db_session:
            db_session.add(category)

            if category_update.category_name:
                category.category_name = category_update.category_name

            await db_session.commit()
            await db_session.refresh(category)

            return category

    async def delete_category_by_id(self, category_id: int) -> int:
        async with self.db_session() as db_session:
            stmt = Delete(Category).where(Category.id == category_id)

            await db_session.execute(statement=stmt)
            await db_session.commit()

            return category_id
