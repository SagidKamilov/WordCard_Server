from src.db.settings import AsyncDatabase

from src.service.user import UserService
from src.repository.user import UserRepository
from src.security.hash_password import HashGenerator


async_database = AsyncDatabase()
async_database.initialize_engine()
async_database.initialize_session()


def user_container() -> UserService:
    async_session = async_database.get_session()
    hash_generator = HashGenerator()
    user_repository = UserRepository(async_db_session_obj=async_session())
    user_service = UserService(user_repo=user_repository, hash_gen=hash_generator)

    return user_service

