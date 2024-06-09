from fastapi import APIRouter

from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.user import router as user_router
from src.api.endpoints.category import router as category_router
from src.api.endpoints.word import router as word_router


main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(category_router)
main_router.include_router(word_router)
