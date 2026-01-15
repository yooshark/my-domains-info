from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.domain_info import DomainInfoService
from app.core.enums import DomainTypes
from app.db.models.domain_info import DomainInfo


@pytest.fixture
def repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def crt_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ipwhois_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def ipinfo_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def service(
    repo: AsyncMock,
    crt_client: AsyncMock,
    ipwhois_client: AsyncMock,
    ipinfo_client: AsyncMock,
) -> DomainInfoService:
    return DomainInfoService(
        repo=repo,
        crt_sh_cl=crt_client,
        ip_who_is_cl=ipwhois_client,
        ip_info_cl=ipinfo_client,
    )


class TestResolveIp:
    async def test_resolve_ip_uses_socket_gethostbyname(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        called_with: dict[str, Any] = {}

        def fake_gethostbyname(host: str) -> str:
            called_with["host"] = host
            return "1.2.3.4"

        async def fake_to_thread(fn, *args, **kwargs):  # type: ignore
            return fn(*args, **kwargs)

        monkeypatch.setattr("socket.gethostbyname", fake_gethostbyname)
        monkeypatch.setattr("asyncio.to_thread", fake_to_thread)

        result = await DomainInfoService.resolve_ip("example.com")
        assert result == "1.2.3.4"
        assert called_with["host"] == "example.com"


class TestGetDomainType:
    async def test_root_domain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class FakeExtract:
            subdomain = ""

        async def fake_to_thread(fn, *args, **kwargs):  # type: ignore
            return FakeExtract()

        monkeypatch.setattr("tldextract.extract", MagicMock())
        monkeypatch.setattr("asyncio.to_thread", fake_to_thread)

        result = await DomainInfoService.get_domain_type("example.com")
        assert result == DomainTypes.ROOT

    async def test_subdomain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class FakeExtract:
            subdomain = "www"

        async def fake_to_thread(fn, *args, **kwargs):  # type: ignore
            return FakeExtract()

        monkeypatch.setattr("tldextract.extract", MagicMock())
        monkeypatch.setattr("asyncio.to_thread", fake_to_thread)

        result = await DomainInfoService.get_domain_type("www.example.com")
        assert result == DomainTypes.SUBDOMAIN


class TestGetDnsSettings:
    async def test_dns_settings_success(
        self, monkeypatch: pytest.MonkeyPatch, service: DomainInfoService
    ) -> None:
        class FakeAnswer:
            def to_text(self) -> str:
                return "1.2.3.4"

        def fake_resolve(domain: str, record: str):  # type: ignore
            assert domain == "example.com"
            assert record == "A"
            return [FakeAnswer()]

        async def fake_to_thread(fn, *args, **kwargs):  # type: ignore
            return fake_resolve(*args, **kwargs)

        monkeypatch.setattr("dns.resolver.resolve", fake_resolve)
        monkeypatch.setattr("asyncio.to_thread", fake_to_thread)
        # limit record types to A only for deterministic test
        service.DNS_RECORD_TYPES = ["A"]

        result = await service.get_dns_settings("example.com")
        assert result == {"A": ["1.2.3.4"]}

    async def test_dns_settings_error_logged_and_skipped(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        def fake_resolve(domain: str, record: str):  # type: ignore
            raise RuntimeError("boom")

        async def fake_to_thread(fn, *args, **kwargs):  # type: ignore
            return fake_resolve(*args, **kwargs)

        monkeypatch.setattr("dns.resolver.resolve", fake_resolve)
        monkeypatch.setattr("asyncio.to_thread", fake_to_thread)
        service.DNS_RECORD_TYPES = ["A"]

        with caplog.at_level("ERROR"):
            result = await service.get_dns_settings("example.com")

        assert result == {}
        assert any("Failed to resolve" in msg for msg in caplog.messages)


class TestGetTargetDomains:
    async def test_get_target_domains_filters_and_deduplicates(
        self,
        service: DomainInfoService,
        crt_client: AsyncMock,
    ) -> None:
        service.crt_sh_cl = crt_client
        crt_client.get_subdomains.return_value = [
            {"name_value": "a.example.com\nb.other.com"},
            {"name_value": "example.com"},
        ]

        result = await service.get_target_domains("example.com")
        assert set(result) == {"example.com", "a.example.com"}


class TestCollectDomainInfo:
    async def test_collect_domain_info_aggregates_clients(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        ipwhois_client: AsyncMock,
        ipinfo_client: AsyncMock,
    ) -> None:
        async def fake_resolve_ip(host: str) -> str:
            return "1.2.3.4"

        async def fake_get_domain_type(domain: str) -> DomainTypes:
            return DomainTypes.ROOT

        service.ip_who_is_cl = ipwhois_client
        service.ip_info_cl = ipinfo_client

        ipwhois_client.get_ip_info.return_value = {
            "city": "City",
            "country": "Country",
            "connection": {"org": "Org"},
            "success": True,
        }
        ipinfo_client.get_ip_info.return_value = {"anycast": True}

        async def fake_get_dns_settings(domain: str) -> dict[str, list[str]]:
            return {"A": ["1.2.3.4"]}

        monkeypatch.setattr(service, "resolve_ip", fake_resolve_ip)
        monkeypatch.setattr(service, "get_domain_type", fake_get_domain_type)
        monkeypatch.setattr(service, "get_dns_settings", fake_get_dns_settings)

        data = {"domain_name": "example.com"}
        result = await service.collect_domain_info(data)

        assert result["ip_address"] == "1.2.3.4"
        assert result["domain_type"] == DomainTypes.ROOT
        assert result["geo_city"] == "City"
        assert result["geo_country"] == "Country"
        assert result["network_owner_name"] == "Org"
        assert result["is_active"] is True
        assert result["is_anycast_node"] is True
        assert result["dns_settings"] == {"A": ["1.2.3.4"]}


class TestHandleDomainName:
    async def test_handle_domain_name_filters_failed_tasks(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        repo: AsyncMock,
    ) -> None:
        domains = ["a.example.com", "b.example.com"]

        async def fake_get_target_domains(domain: str) -> list[str]:
            return domains

        async def fake_collect_domain_info_ok(data: dict[str, Any]) -> dict[str, Any]:
            if data["domain_name"] == "a.example.com":
                return {"domain_name": "a.example.com"}
            raise RuntimeError("boom")

        monkeypatch.setattr(service, "get_target_domains", fake_get_target_domains)
        monkeypatch.setattr(service, "collect_domain_info", fake_collect_domain_info_ok)

        fake_domain = DomainInfo(domain_name="a.example.com")
        fake_domain_2 = DomainInfo(domain_name="b.example.com")
        repo.bulk_insert.return_value = [fake_domain, fake_domain_2]
        service.repo = repo

        result = await service.handle_domain_name("example.com")
        assert result == [fake_domain, fake_domain_2]
        repo.bulk_insert.assert_awaited_once()
        # only one valid result
        args, _ = repo.bulk_insert.await_args
        assert args[0] == [{"domain_name": "a.example.com"}]


class TestAddDomain:
    async def test_add_domain_delegates_to_handle(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        repo: AsyncMock,
    ) -> None:
        repo.get_by_domain_name.return_value = None
        service.repo = repo

        async def fake_handle(domain_name: str) -> list[DomainInfo]:
            return [DomainInfo(domain_name=domain_name)]

        monkeypatch.setattr(service, "handle_domain_name", fake_handle)

        result = await service.add_domain("example.com")

        assert len(result) == 1
        assert result[0].domain_name == "example.com"
        repo.get_by_domain_name.assert_awaited_once_with("example.com")


class TestGetDomainsInfo:
    async def test_get_domains_info_delegates_to_repo(
        self, service: DomainInfoService, repo: AsyncMock
    ) -> None:
        fake_domains = [DomainInfo(domain_name="a"), DomainInfo(domain_name="b")]
        service.repo = repo
        repo.get_domains_info.return_value = (10, fake_domains)
        result = await service.get_domains_info(limit=25, offset=0)
        assert result == (10, fake_domains)
        repo.get_domains_info.assert_awaited_once_with(limit=25, offset=0)


class TestRefreshDomainsInfo:
    async def test_no_root_domains_returns_ok(
        self, service: DomainInfoService, repo: AsyncMock
    ) -> None:
        service.repo = repo
        repo.get_root_domain_names.return_value = []
        resp = await service.refresh_domains_info()
        assert resp == {"status": "ok"}
        repo.get_domain_names.assert_not_called()

    async def test_refresh_domains_all_exceptions(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        repo: AsyncMock,
    ) -> None:
        service.repo = repo
        repo.get_root_domain_names.return_value = ["example.com"]
        repo.get_domain_names.return_value = [(1, "example.com")]

        async def fake_get_target(domain: str) -> list[str]:  # noqa: ARG001
            raise RuntimeError("boom")

        monkeypatch.setattr(service, "get_target_domains", fake_get_target)
        resp = await service.refresh_domains_info()
        assert resp == {"status": "ok"}
        repo.update_domains_info.assert_not_called()

    async def test_refresh_domains_updates_when_valid_results(
        self,
        monkeypatch: pytest.MonkeyPatch,
        service: DomainInfoService,
        repo: AsyncMock,
    ) -> None:
        service.repo = repo
        repo.get_root_domain_names.return_value = ["example.com"]
        repo.get_domain_names.return_value = [(1, "example.com")]

        async def fake_get_target(domain: str) -> list[str]:  # noqa: ARG001
            return ["example.com"]

        async def fake_collect(data: dict[str, Any]) -> dict[str, Any]:
            return {"domain_name": data["domain_name"], "id": 1}

        monkeypatch.setattr(service, "get_target_domains", fake_get_target)
        monkeypatch.setattr(service, "collect_domain_info", fake_collect)

        resp = await service.refresh_domains_info()
        assert resp == {"status": "ok"}
        repo.update_domains_info.assert_awaited_once()
