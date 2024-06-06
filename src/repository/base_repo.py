from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, async_db_session_obj: AsyncSession):
        self.db_session = async_db_session_obj
