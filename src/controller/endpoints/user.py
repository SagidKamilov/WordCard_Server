from typing import List

from fastapi import APIRouter, HTTPException, status

from src.controller.dependencies import user_container
from src.dto.user import UserUpdate, UserResponse
from src.error.user.user_errors import UserAlreadyExists, UserIdNotExists
from src.error.base_error import internal_server_message


router = APIRouter(prefix="/user", tags=["Действия над пользователем"])


@router.get(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user: UserResponse = await user_container().get_user(user_id=user_id)

        return user
    except UserIdNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.get(path="/{category_id}/users", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_users_of_categories(category_id: int):
    users: List[UserResponse] = await user_container().get_users_of_category(category_id=category_id)

    return users


@router.put(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    try:
        user: UserResponse = await user_container().update_user(user_id=user_id, user_update=user_update)

        return user
    except UserIdNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except UserAlreadyExists as wrong:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.delete(path="/{user_id}", status_code=status.HTTP_200_OK, response_model=int)
async def delete_user(user_id: int):
    try:
        result: int = await user_container().delete_user(user_id=user_id)

        return result
    except UserIdNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)
