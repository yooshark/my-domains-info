from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import DomainTypes
from app.db.models.domain_info import DomainInfo
from app.db.repositories.base import BaseRepository


class DomainInfoRepository(BaseRepository[DomainInfo]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, DomainInfo)

    async def get_by_domain_name(self, domain_name: str) -> DomainInfo | None:
        stmt = select(self.model).where(DomainInfo.domain_name == domain_name)
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_domain_names(self) -> list[tuple[int, str]]:
        stmt = select(self.model.id, self.model.domain_name)
        result = await self._session.execute(stmt)
        return [(row.id, row.domain_name) for row in result.all()]

    async def get_root_domain_names(self) -> list[str]:
        stmt = select(self.model.domain_name).where(
            self.model.domain_type == DomainTypes.ROOT
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_domains_info(
        self,
        limit: int,
        offset: int,
    ) -> tuple[int | None, list[DomainInfo]]:
        total = await self._session.scalar(select(func.count()).select_from(self.model))
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return total, list(result.scalars())

    async def add_domain_info(self, data: dict[str, Any]) -> DomainInfo:
        obj = self.model(**data)
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def bulk_insert(self, data: list[dict[str, Any]]) -> list[DomainInfo]:
        objects = [self.model(**item) for item in data]
        self._session.add_all(objects)
        await self._session.flush()
        return objects

    async def update_domains_info(self, data: list[dict[str, Any]]) -> None:
        for item in data:
            await self._session.merge(self.model(**item))
        await self._session.flush()
