from src.db.settings import AsyncDatabase

from src.service.user import UserService
from src.repository.user import UserRepository
from src.security.hash_password import HashGenerator

from src.service.category import CategoryService
from src.repository.category import CategoryRepository

from src.service.word import WordService
from src.repository.word import WordRepository


async_database = AsyncDatabase()
async_database.initialize_engine()
async_database.initialize_session()


def user_container() -> UserService:
    async_session = async_database.get_session()
    hash_generator = HashGenerator()
    user_repository = UserRepository(async_db_session_obj=async_session())
    user_service = UserService(user_repo=user_repository, hash_gen=hash_generator)

    return user_service


def category_container() -> CategoryService:
    async_session = async_database.get_session()
    category_repository = CategoryRepository(async_db_session_obj=async_session())
    category_service = CategoryService(category_repo=category_repository)

    return category_service


def word_container() -> WordService:
    async_session = async_database.get_session()
    word_repository = WordRepository(async_db_session_obj=async_session())
    word_service = WordService(word_repo=word_repository)

    return word_service
