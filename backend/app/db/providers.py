import contextlib
import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import DatabaseSettings

logger = logging.getLogger("app")


@contextlib.asynccontextmanager
async def create_engine(cnf: DatabaseSettings) -> AsyncIterator[AsyncEngine]:
    async_engine = create_async_engine(
        url=cnf.url,
        echo=cnf.ECHO,
        connect_args={"timeout": cnf.TIMEOUT},
        pool_pre_ping=True,
    )
    yield async_engine
    logger.debug("Disposing async engine...")
    await async_engine.dispose()
    logger.debug("Engine is disposed.")


async def make_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    async_session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    logger.debug("Async session maker initialized.")
    return async_session_factory
