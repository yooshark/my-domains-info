from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import Base

TModel = TypeVar("TModel", bound=Base)


class BaseRepository[TModel]:
    def __init__(self, session: AsyncSession, model: type[TModel]) -> None:
        self._session = session
        self.model = model
