import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import DomainTypes
from app.db.repositories.domain_info import DomainInfoRepository


@pytest.fixture
def repo(db_session: AsyncSession) -> DomainInfoRepository:
    return DomainInfoRepository(session=db_session)


async def test_add_domain_info(repo: DomainInfoRepository) -> None:
    data = {"domain_name": "example.com", "domain_type": DomainTypes.ROOT}

    obj = await repo.add_domain_info(data)

    assert obj.id is not None
    assert obj.domain_name == "example.com"


async def test_get_by_domain_name_found(repo: DomainInfoRepository) -> None:
    await repo.add_domain_info({"domain_name": "example.com"})

    obj = await repo.get_by_domain_name("example.com")

    assert obj is not None
    assert obj.domain_name == "example.com"


async def test_get_domain_names(repo: DomainInfoRepository) -> None:
    await repo.add_domain_info({"domain_name": "a.com"})
    await repo.add_domain_info({"domain_name": "b.com"})

    result = await repo.get_domain_names()

    names = [name for _, name in result]
    assert "a.com" in names
    assert "b.com" in names


async def test_get_root_domain_names(repo: DomainInfoRepository) -> None:
    await repo.add_domain_info(
        {"domain_name": "root.com", "domain_type": DomainTypes.ROOT}
    )
    await repo.add_domain_info(
        {"domain_name": "sub.com", "domain_type": DomainTypes.SUBDOMAIN}
    )

    roots = await repo.get_root_domain_names()

    assert roots == ["root.com"]


async def test_get_domains_info_paginated(repo: DomainInfoRepository) -> None:
    for i in range(5):
        await repo.add_domain_info({"domain_name": f"site{i}.com"})

    total, items = await repo.get_domains_info(limit=2, offset=0)

    assert total == 5
    assert len(items) == 2


async def test_bulk_insert(repo: DomainInfoRepository) -> None:
    data = [
        {"domain_name": "a.com"},
        {"domain_name": "b.com"},
    ]

    objs = await repo.bulk_insert(data)

    assert len(objs) == 2


async def test_update_domains_info(repo: DomainInfoRepository) -> None:
    obj = await repo.add_domain_info({"domain_name": "update.com"})

    await repo.update_domains_info([{"id": obj.id, "domain_name": "updated.com"}])

    updated = await repo.get_by_domain_name("updated.com")

    assert updated is not None
