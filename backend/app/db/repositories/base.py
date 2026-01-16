from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models.base import Base

TModel = TypeVar("TModel", bound=Base)


class BaseRepository[TModel]:
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], model: type[TModel]
    ) -> None:
        self.session_factory = session_factory
        self.model = model
