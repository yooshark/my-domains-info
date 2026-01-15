import httpx
import pytest

from app.infrastructure.base import BaseRequestsClient


class TestClient(BaseRequestsClient):
    base_url = "http://test"
    timeout = 5


async def test_get_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(self, method, path, params):  # noqa: ARG001
        class Resp:
            def raise_for_status(self) -> None: ...

            def json(self) -> dict[str, bool]:
                return {"ok": True}

        return Resp()

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

    client = TestClient()
    resp = await client.get("ping")

    assert resp == {"ok": True}


async def test_get_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(self, method, path, params):  # noqa: ARG001
        raise httpx.HTTPStatusError(
            "boom",
            request=httpx.Request("GET", path),
            response=httpx.Response(400),
        )

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

    client = TestClient()

    with pytest.raises(httpx.HTTPStatusError):
        await client.get("fail")


async def test_get_ip_info(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(self, method, path, params):  # noqa: ARG001
        class Resp:
            def raise_for_status(self) -> None: ...

            def json(self) -> dict[str, str]:
                return {"ip": "1.2.3.4"}

        return Resp()

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

    client = TestClient()
    resp = await client.get_ip_info("1.2.3.4")

    assert resp == {"ip": "1.2.3.4"}
