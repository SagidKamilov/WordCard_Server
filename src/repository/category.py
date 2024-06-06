from typing import List

from sqlalchemy import Insert, Select, Update, Delete

from src.model.category import Category
from src.dto.category import CategoryCreate, CategoryUpdate
from src.repository.base_repo import BaseRepository

from src.model.user_category_list import UserCategoryList


class CategoryRepository(BaseRepository):
    async def create_category(self, category_create: CategoryCreate) -> Category:
        stmt = Insert(Category).values(category_name=category_create.category_name)

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

    async def add_user_by_user_id(self, category_id: int, user_id: int) -> UserCategoryList.id | None:
        stmt = Insert(UserCategoryList).values(user_id=user_id, category_id=category_id).returning(UserCategoryList.id)

        result = await self.db_session.execute(statement=stmt)
        scalar_result = result.scalar()

        if not scalar_result:
            return None

        return result

    async def remove_user_by_user_id(self, category_id: int, user_id: int) -> UserCategoryList.id | None:
        stmt = Delete(UserCategoryList).where(category_id=category_id, user_id=user_id)

        result = await self.db_session.execute(statement=stmt)
        scalar_result = result.scalar()

        if not scalar_result:
            return None

        return result

    async def update_category_by_id(self, category_id: int, category_update: CategoryUpdate) -> Category | None:
        category = await self.get_category_by_id(category_id=category_id)

        if not category:
            return None

        if category_update.category_name:
            category.category_name = category_update.category_name

        await self.db_session.commit()

        return category

    async def delete_category_by_id(self, category_id: int) -> Category.id | None:
        category = await self.get_category_by_id(category_id=category_id)

        if not category:
            return None

        # stmt = Delete(Category).where(Category.id == category_id).returning(User.id)
        stmt = Delete(category).returning(Category.id)
        result = await self.db_session.execute(statement=stmt)
        result_scalar = result.scalar()

        if not result_scalar:
            return None

        await self.db_session.commit()

        return result
