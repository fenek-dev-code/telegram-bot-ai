from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .core.config import config as conf

engine = create_async_engine(
    url=conf.DATABASE_URL,
    echo=conf.DATABASE_ECHO,
    max_overflow=conf.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=conf.DATABASE_POOL_PRE_PING,
    pool_recycle=conf.DATABASE_POOL_RECYCLE,
)

sessioon_factory = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessioon_factory() as session:
        yield session


base = declarative_base()


class Base(base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
