from fastapi import APIRouter, HTTPException, status

from src.controller.dependencies import user_container
from src.dto.user import UserCreate, UserAuth, UserResponse
from src.error.user.user_errors import UserAlreadyExists, UserUsernameNotExists, UserWrongPassword
from src.error.base_error import internal_server_message

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(path="/signin", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def sign_in(user_auth: UserAuth):
    try:
        user: UserResponse = await user_container().verify_user(user_auth=user_auth)

        return user
    except UserUsernameNotExists as wrong:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=wrong.message)
    except UserWrongPassword as wrong:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)


@router.post(path="/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def sign_up(user_create: UserCreate):
    try:
        user: UserResponse = await user_container().create_user(user_create=user_create)

        return user
    except UserAlreadyExists as wrong:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=wrong.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=internal_server_message)
