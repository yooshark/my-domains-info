from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.enums import DomainTypes
from app.db.models.domain_info import DomainInfo
from app.db.repositories.base import BaseRepository


class DomainInfoRepository(BaseRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        super().__init__(session_factory, DomainInfo)

    async def get_by_domain_name(self, domain_name: str) -> DomainInfo | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model).where(DomainInfo.domain_name == domain_name)
            )
            return result.scalar_one_or_none()

    async def get_domain_names(self) -> list[tuple[int, str]]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model.id, self.model.domain_name)
            )
            return result.all()

    async def get_root_domain_names(self) -> list[tuple[int, str]]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model.domain_name).where(
                    self.model.domain_type == DomainTypes.ROOT
                )
            )
            return result.scalars().all()

    async def get_domains_info(
        self,
        limit: int,
        offset: int,
    ) -> tuple[int, list[DomainInfo]]:
        async with self.session_factory() as session:
            total = await session.scalar(select(func.count()).select_from(self.model))

            result = await session.execute(
                select(self.model).limit(limit).offset(offset)
            )
            return total, list(result.scalars())

    async def add_domain_info(self, data: dict[str, Any]) -> DomainInfo:
        obj = self.model(**data)
        async with self.session_factory() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

        return obj

    async def bulk_insert(self, data: list[dict[str, Any]]) -> list[DomainInfo]:
        objects = [self.model(**item) for item in data]
        async with self.session_factory() as session:
            session.add_all(objects)
            await session.commit()
            return objects

    async def update_domains_info(self, data: list[dict[str, Any]]) -> None:
        async with self.session_factory() as session:
            for item in data:
                await session.merge(self.model(**item))
            await session.commit()
