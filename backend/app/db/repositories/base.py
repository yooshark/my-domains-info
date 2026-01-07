from typing import TypeVar

from db.models.base import Base
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

TModel = TypeVar("TModel", bound=Base)
TSchema = TypeVar("TSchema", bound=BaseModel)


class BaseRepository:
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], model: type[TModel]
    ) -> None:
        self.session_factory = session_factory
        self.model = model
