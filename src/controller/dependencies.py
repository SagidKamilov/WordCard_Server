from fastapi import Depends

from src.db.settings import async_session

from src.service.user import UserService
from src.repository.user import UserRepository
from src.security.hash_password import HashGenerator

from src.service.category import CategoryService
from src.repository.category import CategoryRepository

from src.service.word import WordService
from src.repository.word import WordRepository


def user_container() -> UserService:
    hash_generator = HashGenerator()
    user_repository = UserRepository(async_session=async_session)
    user_service = UserService(user_repo=user_repository, hash_gen=hash_generator)
    return user_service


def category_container() -> CategoryService:
    category_repository = CategoryRepository(async_session=async_session)
    category_service = CategoryService(category_repo=category_repository)
    return category_service


def word_container() -> WordService:
    word_repository = WordRepository(async_session=async_session)
    word_service = WordService(word_repo=word_repository)
    return word_service
