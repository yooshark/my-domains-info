from typing import Any

import httpx
import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from app.application.domain_info import DomainInfoService
from app.core.enums import DomainTypes
from app.db.models.domain_info import DomainInfo


def make_domain(**overrides: Any) -> DomainInfo:
    return DomainInfo(
        id=overrides.get("id", 1),
        domain_name=overrides.get("domain_name", "example.com"),
        domain_type=overrides.get("domain_type", DomainTypes.ROOT),
        dns_settings=overrides.get("dns_settings", {"A": ["1.2.3.4"]}),
        ip_address=overrides.get("ip_address", "1.2.3.4"),
        geo_city=overrides.get("geo_city", "City"),
        geo_country=overrides.get("geo_country", "Country"),
        network_owner_name=overrides.get("network_owner_name", "Org"),
        is_active=overrides.get("is_active", True),
        is_anycast_node=overrides.get("is_anycast_node", False),
    )


class TestGetDomainsInfoRoute:
    async def test_returns_paginated_response(
        self,
        api_client: AsyncClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        domain = make_domain()

        async def fake_get_domains_info(
            self: DomainInfoService,
            *,
            limit: int,
            offset: int,
        ) -> tuple[int, list[DomainInfo]]:
            return 1, [domain]

        monkeypatch.setattr(
            DomainInfoService, "get_domains_info", fake_get_domains_info
        )

        resp = await api_client.get("/api/domain-info/?limit=25&offset=0")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["domain_name"] == "example.com"


class TestAddDomainRoute:
    async def test_add_domain_success(
        self,
        api_client: AsyncClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        domain = make_domain()

        async def fake_add_domain(
            self: DomainInfoService, domain_name: str
        ) -> list[DomainInfo]:
            return [domain]

        monkeypatch.setattr(DomainInfoService, "add_domain", fake_add_domain)

        resp = await api_client.post(
            "/api/domain-info/",
            json={"domain_name": "example.com"},
        )

        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert data[0]["domain_name"] == "example.com"

    async def test_add_domain_rethrows_http_exception(
        self,
        api_client: AsyncClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        async def fake_add_domain(
            self: DomainInfoService, domain_name: str
        ) -> list[DomainInfo]:
            raise HTTPException(status_code=400, detail="boom")

        monkeypatch.setattr(DomainInfoService, "add_domain", fake_add_domain)

        resp = await api_client.post(
            "/api/domain-info/",
            json={"domain_name": "example.com"},
        )

        assert resp.status_code == 400
        body = resp.json()
        assert body["detail"] == "boom"

    async def test_add_domain_wraps_httpx_status_error(
        self,
        api_client: AsyncClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        response = httpx.Response(400, json={"detail": "external error"})
        request = httpx.Request("GET", "http://test")

        async def fake_add_domain(
            self: DomainInfoService, domain_name: str
        ) -> list[DomainInfo]:
            raise httpx.HTTPStatusError("bad", request=request, response=response)

        monkeypatch.setattr(DomainInfoService, "add_domain", fake_add_domain)

        resp = await api_client.post(
            "/api/domain-info/",
            json={"domain_name": "example.com"},
        )

        assert resp.status_code == 400
        body = resp.json()
        assert body["detail"] == {"detail": "external error"}


class TestRefreshDomainsInfoRoute:
    async def test_refresh_domains_info_ok(
        self,
        api_client: AsyncClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        async def fake_refresh(self: DomainInfoService) -> dict[str, str]:
            return {"status": "ok"}

        monkeypatch.setattr(DomainInfoService, "refresh_domains_info", fake_refresh)

        resp = await api_client.post("/api/domain-info/refresh")

        assert resp.status_code == 200
        data = resp.json()
        assert data == {"status": "ok"}
