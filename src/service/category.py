from typing import List

from src.model.category import Category
from src.repository.category import CategoryRepository
from src.dto.category import CategoryCreate, CategoryUpdate, CategoryResponse
from src.error.category.category_errors import CategoryNotExists, CategoryNotExistsAdditionalInfo


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def create_category(self, user_id: int, category_create: CategoryCreate) -> CategoryResponse:
        category = await self.category_repo.create_category(user_id=user_id, category_create=category_create)

        return CategoryResponse(
            id=category.id,
            category_name=category.category_name,
            owner_id=category.owner_id,
        )

    async def get_category(self, category_id: int) -> CategoryResponse:
        category_exists = await self.check_category_exist(category_id=category_id)

        if not category_exists:
            raise CategoryNotExists(category_id=category_id)

        category = await self.category_repo.get_category_by_id(category_id=category_id)

        return CategoryResponse(
            id=category.id,
            category_name=category.category_name,
            owner_id=category.owner_id
        )

    async def get_categories(self, user_id: int) -> List[CategoryResponse]:
        categories = await self.category_repo.get_categories_by_user_id(user_id=user_id)

        response_list = list(map(lambda category: CategoryResponse(id=category.id, category_name=category.category_name,
                                                                   owner_id=category.owner_id), categories))

        return response_list

    async def get_general_categories(self, user_id: int) -> List[CategoryResponse]:
        categories = await self.category_repo.get_all_general_categories(user_id=user_id)

        response_list = list(map(lambda category: CategoryResponse(id=category.id, category_name=category.category_name,
                                                                   owner_id=category.owner_id), categories))

        return response_list

    async def add_user_in_category(self, user_id: int, category_id: int) -> int:
        category_exists = await self.check_category_exist(category_id=category_id)

        if not category_exists:
            raise CategoryNotExistsAdditionalInfo(category_id=category_id, user_id=user_id)

        result_category_id = await self.category_repo.add_user_by_user_id(user_id=user_id, category_id=category_id)

        return result_category_id # Такой же момент, чтобы подумать

    async def remove_user_from_category(self, user_id: int, category_id: int) -> int:
        category_exists = await self.check_category_exist(category_id=category_id)

        if not category_exists:
            raise CategoryNotExistsAdditionalInfo(category_id=category_id, user_id=user_id)

        result_category_id = await self.category_repo.remove_user_by_user_id(user_id=user_id, category_id=category_id)

        return result_category_id

    async def update_category(self, category_id: int, category_update: CategoryUpdate) -> CategoryResponse:
        category: Category = await self.category_repo.get_category_by_id(category_id=category_id)

        if not category:
            raise CategoryNotExists(category_id=category_id)

        category = await self.category_repo.update_category_by_id(category=category, category_update=category_update)

        return CategoryResponse(
            id=category.id,
            category_name=category.category_name,
            owner_id=category.owner_id
        )

    async def delete_category(self, category_id: int) -> int:
        category_exists = await self.check_category_exist(category_id=category_id)

        if not category_exists:
            raise CategoryNotExists(category_id=category_id)

        result = await self.category_repo.delete_category_by_id(category_id=category_id)

        return result

    async def check_category_exist(self, category_id: int) -> bool:
        category: Category = await self.category_repo.get_category_by_id(category_id=category_id)

        return True if category else False
