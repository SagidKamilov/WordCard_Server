from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, async_session: Type[AsyncSession]):
        self.db_session = async_session
