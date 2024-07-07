# ---------------------------------------------------------
# This file describes the basic settings of DB
# ---------------------------------------------------------

from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

url = f"postgresql+{settings.POSTGRES_SCHEMA}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
async_engine = create_async_engine(url=url, pool_size=20, max_overflow=0)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
