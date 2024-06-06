from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import user_container
from src.dto.user import UserCreate, UserAuth, UserResponse


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(path="/signin", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def sign_in(user_auth: UserAuth):
    try:
        user: UserResponse = await user_container().verify_user(user_auth=user_auth)

        return user
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error_detail))


@router.post(path="/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def sign_up(user_create: UserCreate):
    try:
        user: UserResponse = await user_container().create_user(user_create=user_create)

        return user
    except Exception as error_detail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error_detail))