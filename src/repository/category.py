from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.category import Category
from src.dto.category import CategoryCreate, CategoryUpdate
from src.repository.base_repo import BaseRepository

from src.model.user_category_list import UserCategoryList


class CategoryRepository(BaseRepository):
    async def create_category(self, user_id: int, category_create: CategoryCreate) -> Category:
        stmt = Insert(Category).values(owner_id=user_id, category_name=category_create.category_name).returning(Category)

        result = await self.db_session.execute(statement=stmt)
        category = result.scalar()

        await self.db_session.commit()

        return category

    async def get_category_by_id(self, category_id: int) -> Category | None:
        stmt = Select(Category).where(Category.id == category_id)

        result = await self.db_session.execute(statement=stmt)
        category = result.scalar()

        if not category:
            return None

        return category

    async def get_categories_by_user_id(self, user_id: int) -> List[Category]:
        stmt = Select(Category).where(Category.owner_id == user_id)

        categories = await self.db_session.execute(statement=stmt)

        categories_list = [
            element
            for element
            in categories.scalars()
        ]

        return categories_list

    async def get_all_general_category_categories(self, user_id: int) -> List[Category]:
        stmt = Select(Category).join(UserCategoryList).where(UserCategoryList.user_id == user_id)

        categories = await self.db_session.execute(statement=stmt)

        categories_list = [
            element
            for element
            in categories.scalars()
        ]

        return categories_list

    async def add_user_by_user_id(self, category_id: int, user_id: int) -> int:
        stmt = Insert(UserCategoryList).values(user_id=user_id, category_id=category_id)

        await self.db_session.execute(statement=stmt)
        await self.db_session.commit()

        return category_id

    async def remove_user_by_user_id(self, category_id: int, user_id: int) -> int:
        stmt = Delete(UserCategoryList).where(UserCategoryList.category_id == category_id).where(UserCategoryList.user_id==user_id)

        await self.db_session.execute(statement=stmt)
        await self.db_session.commit()

        return category_id

    async def update_category_by_id(self, category_id: int, category_update: CategoryUpdate) -> Category | None:
        stmt = Update(Category).where(Category.id == category_id)

        if category_update.category_name:
            stmt = stmt.values(category_name=category_update.category_name)

        stmt = stmt.returning(Category)
        result = await self.db_session.execute(statement=stmt)
        category = result.scalar()

        await self.db_session.commit()

        return category

    async def delete_category_by_id(self, category_id: int) -> int:
        stmt = Delete(Category).where(Category.id == category_id)

        await self.db_session.execute(statement=stmt)
        await self.db_session.commit()

        return category_id
