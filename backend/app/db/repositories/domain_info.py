from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

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
            return result.scalars().first()

    async def get_domain_names(self) -> list[tuple[int, str]]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model.id, self.model.domain_name)
            )
            return result.all()

    async def get_domains_info(self) -> list[DomainInfo] | None:
        async with self.session_factory() as session:
            result = await session.execute(select(self.model))
            return list(result.scalars())

    async def add_domain_info(self, model_data: dict[str, Any]) -> DomainInfo:
        domain_info = self.model(**model_data)

        async with self.session_factory() as session:
            session.add(domain_info)
            await session.commit()
            await session.refresh(domain_info)

        return domain_info

    async def update_domains_info(self, data: list[dict[str, Any]]) -> None:
        async with self.session_factory() as session:
            await session.execute(update(self.model), data)
            await session.commit()
