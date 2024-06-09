from typing import List

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import category_container
from src.dto.category import CategoryCreate, CategoryUpdate, CategoryResponse


router = APIRouter(prefix="", tags=["Действия над категориями"])


@router.post(path="/category/{user_id}", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(user_id: int, category_create: CategoryCreate):
    try:
        category = await category_container().create_category(user_id=user_id, category_create=category_create)

        return category
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.get(path="/category/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category(category_id: int):
    try:
        category = await category_container().get_category(category_id=category_id)

        return category
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.get(path="/{user_id}/categories", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def get_categories(user_id: int):
    try:
        categories = await category_container().get_categories(user_id=user_id)

        return categories
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.get(path="/{user_id}/general/categories", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def get_categories(user_id: int):
    try:
        categories = await category_container().get_general_categories(user_id=user_id)

        return categories
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.post(path="/category/{category_id}/user/{user_id}", status_code=status.HTTP_200_OK, response_model=int)
async def category_add_user(category_id: int, user_id: int):
    try:
        result = await category_container().add_user_in_category(user_id=user_id, category_id=category_id)

        return result
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.delete(path="/category/{category_id}/user/{user_id}", status_code=status.HTTP_200_OK, response_model=int)
async def category_add_user(category_id: int, user_id: int):
    try:
        result = await category_container().remove_user_from_category(user_id=user_id, category_id=category_id)

        return result
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.put(path="/category/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def update_category(category_id: int, category_update: CategoryUpdate):
    try:
        category = await category_container().update_category(category_id=category_id, category_update=category_update)

        return category
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.delete(path="/category/{category_id}", status_code=status.HTTP_200_OK, response_model=int)
async def delete_category(category_id: int):
    try:
        result: int = await category_container().delete_category(category_id=category_id)

        return result
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))
