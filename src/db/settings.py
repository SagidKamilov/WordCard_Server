# ---------------------------------------------------------
# This file describes the basic settings of DB
# ---------------------------------------------------------

from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine

from src.config import settings


class AsyncDatabase:
    def __init__(self):
        self.url = f"postgresql+{settings.POSTGRES_SCHEMA}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        self.async_engine = None
        self.async_session = None

    def initialize_engine(self):
        self.async_engine = create_async_engine(url=self.url, pool_size=20, max_overflow=0)

    def initialize_session(self):
        self.async_session = async_sessionmaker(bind=self.async_engine, expire_on_commit=False)

    def get_engine(self) -> Type[AsyncEngine]:
        return self.async_engine

    def get_session(self) -> Type[AsyncSession]:
        return self.async_session
